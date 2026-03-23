"""TSV/CSV parser with flexible column mapping."""

from __future__ import annotations

import io

import polars as pl

from src.parsers.common import VariantKey, VariantRecord

# Alias mapping: canonical name → list of recognized column names (lowercased)
_ALIASES: dict[str, list[str]] = {
    "chrom": ["chrom", "chromosome", "chr", "#chrom", "#chr"],
    "pos": ["pos", "position", "start", "start_position"],
    "ref": ["ref", "reference", "ref_allele", "reference_allele"],
    "alt": ["alt", "alternate", "alt_allele", "alternate_allele", "tumor_seq_allele2"],
    "vaf": ["vaf", "af", "allele_frequency", "variant_allele_frequency", "t_vaf"],
    "depth": ["depth", "dp", "total_depth", "coverage", "t_depth"],
    "gene": ["gene", "gene_symbol", "hugo_symbol", "gene_name"],
    "transcript": ["transcript", "transcript_id", "feature"],
    "protein_change": [
        "protein_change",
        "hgvsp",
        "hgvsp_short",
        "amino_acid_change",
        "aachange",
        "protein_variant",
    ],
    "filter": ["filter", "filter_status"],
    "ref_count": ["ref_count", "t_ref_count", "ref_depth"],
    "alt_count": ["alt_count", "t_alt_count", "alt_depth"],
}


def _resolve_columns(header_names: list[str]) -> dict[str, str | None]:
    """Map canonical field names to actual column names found in the header.

    Parameters
    ----------
    header_names : list[str]
        Column names from the file header.

    Returns
    -------
    dict[str, str | None]
        Canonical name → actual column name (or None if not found).
    """
    lower_to_original = {h.lower().strip(): h for h in header_names}
    mapping: dict[str, str | None] = {}
    for canonical, aliases in _ALIASES.items():
        mapping[canonical] = None
        for alias in aliases:
            if alias in lower_to_original:
                mapping[canonical] = lower_to_original[alias]
                break
    return mapping


def parse_tsv(content: str, delimiter: str = "\t") -> list[VariantRecord]:
    """Parse a TSV or CSV file into VariantRecords.

    Parameters
    ----------
    content : str
        Full file content.
    delimiter : str
        Column delimiter (tab or comma).

    Returns
    -------
    list[VariantRecord]
        Parsed variants.

    Raises
    ------
    ValueError
        If required columns (chrom, pos, ref, alt) are missing.
    """
    # Skip comment lines
    lines = content.split("\n")
    data_lines = [line for line in lines if not line.startswith("#") or line.startswith("#CHROM") or line.startswith("#Chr")]
    # If we stripped the header comment prefix, put it back
    cleaned = "\n".join(data_lines)

    if not cleaned.strip():
        return []

    sep = delimiter
    df = pl.read_csv(io.StringIO(cleaned), separator=sep, infer_schema_length=0)

    col_map = _resolve_columns(df.columns)

    # Validate required columns
    for required in ("chrom", "pos", "ref", "alt"):
        if col_map[required] is None:
            raise ValueError(
                f"Required column '{required}' not found. "
                f"Columns present: {df.columns}"
            )

    records: list[VariantRecord] = []
    for row in df.iter_rows(named=True):
        chrom = str(row[col_map["chrom"]])
        pos = int(row[col_map["pos"]])
        ref = str(row[col_map["ref"]])
        alt = str(row[col_map["alt"]])

        # VAF: direct column or compute from counts
        vaf: float | None = None
        if col_map["vaf"] is not None:
            raw = row[col_map["vaf"]]
            if raw is not None and str(raw).strip():
                try:
                    vaf = float(raw)
                except ValueError:
                    vaf = None
        elif col_map["alt_count"] is not None and col_map["ref_count"] is not None:
            try:
                alt_c = float(row[col_map["alt_count"]])
                ref_c = float(row[col_map["ref_count"]])
                total = alt_c + ref_c
                vaf = alt_c / total if total > 0 else None
            except (ValueError, TypeError):
                vaf = None

        # Depth
        depth: int | None = None
        if col_map["depth"] is not None:
            raw = row[col_map["depth"]]
            if raw is not None and str(raw).strip():
                try:
                    depth = int(float(raw))
                except ValueError:
                    depth = None

        gene = str(row[col_map["gene"]]) if col_map["gene"] and row.get(col_map["gene"]) else ""
        transcript = str(row[col_map["transcript"]]) if col_map["transcript"] and row.get(col_map["transcript"]) else ""
        protein_change = str(row[col_map["protein_change"]]) if col_map["protein_change"] and row.get(col_map["protein_change"]) else ""
        filter_status = str(row[col_map["filter"]]) if col_map["filter"] and row.get(col_map["filter"]) else ""

        records.append(
            VariantRecord(
                key=VariantKey(chrom=chrom, pos=pos, ref=ref, alt=alt),
                vaf=vaf,
                depth=depth,
                gene=gene,
                transcript=transcript,
                protein_change=protein_change,
                filter_status=filter_status,
            )
        )

    return records
