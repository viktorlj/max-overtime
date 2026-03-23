"""Cross-timepoint variant matching and merging."""

from __future__ import annotations

import polars as pl

from src.parsers.common import VariantKey, VariantRecord


def _build_variant_label(record: VariantRecord) -> str:
    """Create a human-readable label like 'KRAS p.G12V' or 'chr12:25398284 C>A'."""
    parts: list[str] = []
    if record.gene:
        parts.append(record.gene)
    if record.protein_change:
        parts.append(record.protein_change)
    if not parts:
        k = record.key
        parts.append(f"{k.chrom}:{k.pos} {k.ref}>{k.alt}")
    return " ".join(parts)


def merge_timepoints(
    timepoint_data: list[tuple[str, str | None, list[VariantRecord]]],
) -> pl.DataFrame:
    """Merge variant records across timepoints into a long-format DataFrame.

    Parameters
    ----------
    timepoint_data : list[tuple[str, str | None, list[VariantRecord]]]
        Each entry is (timepoint_label, date_string_or_None, list_of_records).
        The timepoint_label is like "Timepoint 1" and date_string is "2024-01-15".

    Returns
    -------
    pl.DataFrame
        Long-format DataFrame with columns: chrom, pos, ref, alt, gene, transcript,
        protein_change, variant_label, timepoint_label, date, vaf, depth.
    """
    # Collect all unique variant keys with best metadata
    key_meta: dict[VariantKey, VariantRecord] = {}
    for _label, _date, records in timepoint_data:
        for rec in records:
            if rec.key not in key_meta:
                key_meta[rec.key] = rec
            else:
                # Prefer records that have gene/protein info
                existing = key_meta[rec.key]
                if not existing.gene and rec.gene:
                    key_meta[rec.key] = rec

    # Build label map
    label_map: dict[VariantKey, str] = {}
    for key, rec in key_meta.items():
        label_map[key] = _build_variant_label(rec)

    # Build lookup per timepoint: key → record
    rows: list[dict] = []
    for tp_label, date_str, records in timepoint_data:
        tp_lookup = {rec.key: rec for rec in records}

        for key in key_meta:
            meta = key_meta[key]
            rec = tp_lookup.get(key)

            rows.append(
                {
                    "chrom": key.chrom,
                    "pos": key.pos,
                    "ref": key.ref,
                    "alt": key.alt,
                    "gene": meta.gene,
                    "transcript": meta.transcript,
                    "protein_change": meta.protein_change,
                    "variant_label": label_map[key],
                    "timepoint_label": tp_label,
                    "date": date_str or "",
                    "vaf": rec.vaf if rec else None,
                    "depth": rec.depth if rec else None,
                }
            )

    if not rows:
        return pl.DataFrame(
            schema={
                "chrom": pl.Utf8,
                "pos": pl.Int64,
                "ref": pl.Utf8,
                "alt": pl.Utf8,
                "gene": pl.Utf8,
                "transcript": pl.Utf8,
                "protein_change": pl.Utf8,
                "variant_label": pl.Utf8,
                "timepoint_label": pl.Utf8,
                "date": pl.Utf8,
                "vaf": pl.Float64,
                "depth": pl.Int64,
            }
        )

    return pl.DataFrame(rows)
