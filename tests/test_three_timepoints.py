"""End-to-end test: 3-timepoint AML patient scenario.

Simulated patient:
    - Timepoint 1 (2024-01-10): Diagnosis — DNMT3A, NPM1, FLT3, IDH2 clonal; TP53 sub-clonal
    - Timepoint 2 (2024-04-22): Post-induction — FLT3/IDH2 cleared; DNMT3A persistent (pre-leukemic); TP53 rising
    - Timepoint 3 (2024-09-15): Relapse — NPM1 returns; FLT3 gone; TP53 dominant; KRAS new clone

Expected VAF trajectories:
    DNMT3A p.R882H   — 46% → 44% → 47%  (pre-leukemic, stable)
    NPM1   p.W288fs  — 41% →  8% → 38%  (responds then relapses)
    FLT3   p.D835Y   — 32% →  2% →  0%  (cleared by treatment)
    IDH2   p.R140Q   — 24% →  5% →  3%  (cleared by treatment)
    TP53   p.R248W   —  5% → 12% → 35%  (resistant clone expanding)
    KRAS   p.G12D    —  0% →  0% → 15%  (new at relapse)
"""

from pathlib import Path

import polars as pl
import pytest

from src.parsers.common import parse_file
from src.processing.merge import merge_timepoints
from src.processing.export import export_excel, export_tsv

DATA_DIR = Path(__file__).parent / "data"

TIMEPOINTS = [
    ("Timepoint 1", "2024-01-10", DATA_DIR / "tp1_diagnosis.tsv"),
    ("Timepoint 2", "2024-04-22", DATA_DIR / "tp2_post_induction.tsv"),
    ("Timepoint 3", "2024-09-15", DATA_DIR / "tp3_relapse.tsv"),
]


@pytest.fixture
def merged_df() -> pl.DataFrame:
    tp_data = []
    for label, date, path in TIMEPOINTS:
        content = path.read_text()
        records = parse_file(path.name, content)
        tp_data.append((label, date, records))
    return merge_timepoints(tp_data)


def test_parse_all_timepoints():
    for label, _, path in TIMEPOINTS:
        content = path.read_text()
        records = parse_file(path.name, content)
        assert len(records) == 6, f"{label}: expected 6 variants, got {len(records)}"


def test_merged_shape(merged_df: pl.DataFrame):
    # 6 variants × 3 timepoints = 18 rows
    assert merged_df.shape == (18, 12)


def test_merged_columns(merged_df: pl.DataFrame):
    expected = {
        "chrom", "pos", "ref", "alt", "gene", "transcript",
        "protein_change", "variant_label", "timepoint_label", "date",
        "vaf", "depth",
    }
    assert set(merged_df.columns) == expected


def test_all_timepoints_present(merged_df: pl.DataFrame):
    labels = merged_df["timepoint_label"].unique().sort().to_list()
    assert labels == ["Timepoint 1", "Timepoint 2", "Timepoint 3"]


def test_all_variants_present(merged_df: pl.DataFrame):
    genes = merged_df["gene"].unique().sort().to_list()
    assert genes == ["DNMT3A", "FLT3", "IDH2", "KRAS", "NPM1", "TP53"]


def test_dnmt3a_stable(merged_df: pl.DataFrame):
    """DNMT3A should be stable across all timepoints (pre-leukemic clone)."""
    vafs = (
        merged_df
        .filter(pl.col("gene") == "DNMT3A")
        .sort("date")["vaf"]
        .to_list()
    )
    assert vafs == pytest.approx([0.46, 0.44, 0.47])


def test_flt3_clears(merged_df: pl.DataFrame):
    """FLT3 should drop to 0 by timepoint 3."""
    vafs = (
        merged_df
        .filter(pl.col("gene") == "FLT3")
        .sort("date")["vaf"]
        .to_list()
    )
    assert vafs == pytest.approx([0.32, 0.02, 0.0])


def test_tp53_expanding(merged_df: pl.DataFrame):
    """TP53 resistant clone should be expanding over time."""
    vafs = (
        merged_df
        .filter(pl.col("gene") == "TP53")
        .sort("date")["vaf"]
        .to_list()
    )
    assert vafs[0] < vafs[1] < vafs[2]


def test_kras_new_at_relapse(merged_df: pl.DataFrame):
    """KRAS appears only at relapse (0 at TP1 and TP2)."""
    vafs = (
        merged_df
        .filter(pl.col("gene") == "KRAS")
        .sort("date")["vaf"]
        .to_list()
    )
    assert vafs[0] == pytest.approx(0.0)
    assert vafs[1] == pytest.approx(0.0)
    assert vafs[2] == pytest.approx(0.15)


def test_variant_labels(merged_df: pl.DataFrame):
    labels = merged_df["variant_label"].unique().sort().to_list()
    assert "DNMT3A p.R882H" in labels
    assert "TP53 p.R248W" in labels
    assert "KRAS p.G12D" in labels


def test_export_excel(merged_df: pl.DataFrame):
    xlsx = export_excel(merged_df, "AML_Patient_001")
    assert len(xlsx) > 0
    # Should be a valid XLSX (starts with PK zip signature)
    assert xlsx[:2] == b"PK"


def test_export_tsv(merged_df: pl.DataFrame):
    tsv_bytes = export_tsv(merged_df)
    tsv_str = tsv_bytes.decode()
    lines = tsv_str.strip().split("\n")
    assert len(lines) == 19  # 1 header + 18 data rows


def test_json_roundtrip(merged_df: pl.DataFrame):
    """Simulate dcc.Store serialization."""
    json_str = merged_df.write_json()
    restored = pl.read_json(json_str.encode())
    assert restored.shape == merged_df.shape
    assert restored.columns == merged_df.columns
