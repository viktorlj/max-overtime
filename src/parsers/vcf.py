"""VCF parser with multiple VAF extraction strategies."""

from __future__ import annotations

from src.parsers.common import VariantKey, VariantRecord


def _parse_info(info_str: str) -> dict[str, str]:
    """Parse a VCF INFO field into a dict."""
    result: dict[str, str] = {}
    for entry in info_str.split(";"):
        if "=" in entry:
            k, v = entry.split("=", 1)
            result[k] = v
        else:
            result[entry] = ""
    return result


def _extract_vaf_and_depth(
    fmt_fields: list[str],
    sample_values: list[str],
    info: dict[str, str],
) -> tuple[float | None, int | None]:
    """Extract VAF and depth from FORMAT/SAMPLE fields with fallbacks.

    Priority for VAF: AF field → compute from AD → compute from DP4
    Priority for depth: FORMAT DP → INFO DP
    """
    fmt_map = {}
    for i, key in enumerate(fmt_fields):
        if i < len(sample_values):
            fmt_map[key] = sample_values[i]

    vaf: float | None = None
    depth: int | None = None

    # Try AF directly (common in somatic VCFs)
    if "AF" in fmt_map:
        try:
            val = fmt_map["AF"]
            # Multi-allelic: take first alt
            vaf = float(val.split(",")[0])
        except (ValueError, IndexError):
            pass

    # Try computing from AD (allelic depths: ref,alt1,alt2,...)
    if vaf is None and "AD" in fmt_map:
        try:
            parts = fmt_map["AD"].split(",")
            ref_depth = int(parts[0])
            alt_depth = int(parts[1])
            total = ref_depth + alt_depth
            if total > 0:
                vaf = alt_depth / total
            depth = total
        except (ValueError, IndexError):
            pass

    # Depth from FORMAT DP
    if "DP" in fmt_map:
        try:
            depth = int(fmt_map["DP"])
        except ValueError:
            pass

    # Depth fallback: INFO DP
    if depth is None and "DP" in info:
        try:
            depth = int(info["DP"])
        except ValueError:
            pass

    # VAF fallback: if we have DP from FORMAT and AD ref count
    if vaf is None and depth is not None and depth > 0 and "AD" in fmt_map:
        try:
            parts = fmt_map["AD"].split(",")
            alt_depth = int(parts[1])
            vaf = alt_depth / depth
        except (ValueError, IndexError):
            pass

    return vaf, depth


def _extract_gene_info(info: dict[str, str]) -> tuple[str, str, str]:
    """Try to extract gene, transcript, protein_change from INFO fields (e.g. ANN/CSQ)."""
    gene = ""
    transcript = ""
    protein_change = ""

    # SnpEff ANN field
    ann = info.get("ANN", "")
    if ann:
        # ANN format: Allele|Annotation|...|Gene_Name|Gene_ID|Feature_Type|Feature_ID|...|HGVS.p|...
        first_ann = ann.split(",")[0]
        parts = first_ann.split("|")
        if len(parts) > 3:
            gene = parts[3]
        if len(parts) > 6:
            transcript = parts[6]
        if len(parts) > 11:
            protein_change = parts[11]

    # VEP CSQ field
    if not gene:
        csq = info.get("CSQ", "")
        if csq:
            first_csq = csq.split(",")[0]
            parts = first_csq.split("|")
            # VEP default: Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|...
            if len(parts) > 3:
                gene = parts[3]
            if len(parts) > 6:
                transcript = parts[6]

    return gene, transcript, protein_change


def parse_vcf(content: str) -> list[VariantRecord]:
    """Parse a VCF file into VariantRecords.

    Parameters
    ----------
    content : str
        Full VCF file content.

    Returns
    -------
    list[VariantRecord]
        Parsed variants.
    """
    records: list[VariantRecord] = []
    header_cols: list[str] = []

    for line in content.split("\n"):
        line = line.rstrip()

        # Skip meta-information lines
        if line.startswith("##"):
            continue

        # Header line
        if line.startswith("#CHROM") or line.startswith("#chrom"):
            header_cols = line.lstrip("#").split("\t")
            continue

        if not line:
            continue

        fields = line.split("\t")
        if len(fields) < 8:
            continue

        chrom = fields[0]
        try:
            pos = int(fields[1])
        except ValueError:
            continue
        ref = fields[3]
        alt_field = fields[4]

        filter_status = fields[6] if len(fields) > 6 else ""
        info_str = fields[7] if len(fields) > 7 else ""
        info = _parse_info(info_str)

        # Handle multi-allelic: split into separate records
        alts = alt_field.split(",")

        for alt_idx, alt in enumerate(alts):
            alt = alt.strip()
            if alt == "." or alt == "*":
                continue

            # Extract FORMAT + first sample
            vaf: float | None = None
            depth: int | None = None

            if len(fields) > 9:
                fmt_fields = fields[8].split(":")
                sample_values = fields[9].split(":")
                vaf, depth = _extract_vaf_and_depth(fmt_fields, sample_values, info)

            gene, transcript, protein_change = _extract_gene_info(info)

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
