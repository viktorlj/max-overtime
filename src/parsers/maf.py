"""MAF (Mutation Annotation Format) parser."""

from __future__ import annotations

import io

import polars as pl

from src.parsers.common import VariantKey, VariantRecord


def parse_maf(content: str) -> list[VariantRecord]:
    """Parse a MAF file into VariantRecords.

    Parameters
    ----------
    content : str
        Full MAF file content.

    Returns
    -------
    list[VariantRecord]
        Parsed variants.

    Raises
    ------
    ValueError
        If required MAF columns are missing.
    """
    # Skip comment lines (lines starting with #)
    lines = content.split("\n")
    data_lines = [line for line in lines if not line.startswith("#")]
    cleaned = "\n".join(data_lines)

    if not cleaned.strip():
        return []

    df = pl.read_csv(io.StringIO(cleaned), separator="\t", infer_schema_length=0)

    # Validate required columns
    required = {"Chromosome", "Start_Position", "Reference_Allele", "Tumor_Seq_Allele2"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required MAF columns: {missing}")

    records: list[VariantRecord] = []
    for row in df.iter_rows(named=True):
        chrom = str(row["Chromosome"])
        pos = int(row["Start_Position"])
        ref = str(row["Reference_Allele"])
        alt = str(row["Tumor_Seq_Allele2"])

        # VAF from t_alt_count / (t_alt_count + t_ref_count)
        vaf: float | None = None
        if "t_alt_count" in df.columns and "t_ref_count" in df.columns:
            try:
                alt_c = float(row["t_alt_count"])
                ref_c = float(row["t_ref_count"])
                total = alt_c + ref_c
                vaf = alt_c / total if total > 0 else None
            except (ValueError, TypeError):
                vaf = None

        # Depth from t_depth or sum of counts
        depth: int | None = None
        if "t_depth" in df.columns:
            try:
                depth = int(float(row["t_depth"]))
            except (ValueError, TypeError):
                depth = None
        elif vaf is not None and "t_alt_count" in df.columns and "t_ref_count" in df.columns:
            try:
                depth = int(float(row["t_alt_count"])) + int(float(row["t_ref_count"]))
            except (ValueError, TypeError):
                depth = None

        gene = str(row.get("Hugo_Symbol", "")) or ""
        transcript = str(row.get("Transcript_ID", "")) or ""

        # Protein change: prefer HGVSp_Short, fallback to HGVSp
        protein_change = ""
        for col in ("HGVSp_Short", "HGVSp"):
            if col in df.columns and row.get(col):
                protein_change = str(row[col])
                break

        filter_status = str(row.get("FILTER", "")) or ""

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
