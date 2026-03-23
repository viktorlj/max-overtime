"""Core data model and dispatch for variant file parsing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VariantKey:
    """Unique identifier for a genomic variant, used for cross-timepoint matching."""

    chrom: str
    pos: int
    ref: str
    alt: str

    def __post_init__(self) -> None:
        # Normalize chrom on creation
        object.__setattr__(self, "chrom", normalize_chrom(self.chrom))


@dataclass
class VariantRecord:
    """A single variant observation at one timepoint."""

    key: VariantKey
    vaf: float | None = None
    depth: int | None = None
    gene: str = ""
    transcript: str = ""
    protein_change: str = ""
    filter_status: str = ""


def normalize_chrom(chrom: str) -> str:
    """Strip 'chr' prefix and uppercase.

    Parameters
    ----------
    chrom : str
        Chromosome string, e.g. 'chr1', 'Chr17', '22'.

    Returns
    -------
    str
        Normalized chromosome, e.g. '1', '17', '22'.
    """
    s = chrom.strip().upper()
    if s.startswith("CHR"):
        s = s[3:]
    return s


def detect_format(filename: str, content: str | None = None) -> str:
    """Detect file format from extension and optional content sniffing.

    Parameters
    ----------
    filename : str
        Original filename including extension.
    content : str | None
        Optional file content for sniffing.

    Returns
    -------
    str
        One of 'vcf', 'maf', 'tsv', 'csv'.

    Raises
    ------
    ValueError
        If format cannot be determined.
    """
    name = filename.lower()

    if name.endswith(".vcf") or name.endswith(".vcf.gz"):
        return "vcf"
    if name.endswith(".maf") or name.endswith(".maf.txt"):
        return "maf"
    if name.endswith(".csv"):
        return "csv"
    if name.endswith(".tsv") or name.endswith(".txt"):
        # Sniff content to disambiguate TSV vs MAF
        if content:
            header = content.split("\n")[0] if "\n" in content else content
            maf_cols = {"Hugo_Symbol", "Chromosome", "Start_Position"}
            if maf_cols.issubset(set(header.split("\t"))):
                return "maf"
        return "tsv"

    if content:
        first_line = content.lstrip().split("\n")[0]
        if first_line.startswith("##fileformat=VCF"):
            return "vcf"
        maf_cols = {"Hugo_Symbol", "Chromosome", "Start_Position"}
        if maf_cols.issubset(set(first_line.split("\t"))):
            return "maf"

    raise ValueError(f"Cannot determine format for '{filename}'")


def parse_file(filename: str, content: str) -> list[VariantRecord]:
    """Parse a variant file and return a list of VariantRecords.

    Parameters
    ----------
    filename : str
        Original filename (used for format detection).
    content : str
        Full file content as string.

    Returns
    -------
    list[VariantRecord]
        Parsed variants.
    """
    fmt = detect_format(filename, content)

    if fmt == "vcf":
        from src.parsers.vcf import parse_vcf

        return parse_vcf(content)
    elif fmt == "maf":
        from src.parsers.maf import parse_maf

        return parse_maf(content)
    else:
        from src.parsers.tsv import parse_tsv

        return parse_tsv(content, delimiter="," if fmt == "csv" else "\t")
