"""Tests for TSV/CSV parser."""

from src.parsers.tsv import parse_tsv
from tests.conftest import SAMPLE_TSV, SAMPLE_CSV

import pytest


def test_parse_tsv_basic():
    records = parse_tsv(SAMPLE_TSV)
    assert len(records) == 2

    kras = records[0]
    assert kras.key.chrom == "12"
    assert kras.key.pos == 25398284
    assert kras.key.ref == "C"
    assert kras.key.alt == "A"
    assert kras.vaf == pytest.approx(0.45)
    assert kras.depth == 500
    assert kras.gene == "KRAS"
    assert kras.protein_change == "p.G12V"


def test_parse_csv():
    records = parse_tsv(SAMPLE_CSV, delimiter=",")
    assert len(records) == 2
    assert records[0].gene == "KRAS"
    assert records[1].gene == "TP53"


def test_parse_tsv_with_counts():
    content = """\
Chrom\tPos\tRef\tAlt\tRef_Count\tAlt_Count\tGene
12\t25398284\tC\tA\t275\t225\tKRAS
"""
    records = parse_tsv(content)
    assert len(records) == 1
    assert records[0].vaf == pytest.approx(225 / 500)
    assert records[0].gene == "KRAS"


def test_parse_tsv_missing_required():
    content = "Gene\tVAF\nKRAS\t0.5\n"
    with pytest.raises(ValueError, match="Required column"):
        parse_tsv(content)


def test_parse_tsv_empty():
    records = parse_tsv("")
    assert records == []


def test_chrom_normalization():
    records = parse_tsv(SAMPLE_TSV)
    assert records[0].key.chrom == "12"  # chr12 → 12
    assert records[1].key.chrom == "17"  # chr17 → 17
