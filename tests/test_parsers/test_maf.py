"""Tests for MAF parser."""

from src.parsers.maf import parse_maf
from tests.conftest import SAMPLE_MAF

import pytest


def test_parse_maf_basic():
    records = parse_maf(SAMPLE_MAF)
    assert len(records) == 3

    kras = records[0]
    assert kras.key.chrom == "12"
    assert kras.key.pos == 25398284
    assert kras.key.ref == "C"
    assert kras.key.alt == "A"
    assert kras.vaf == pytest.approx(225 / 500)
    assert kras.depth == 500
    assert kras.gene == "KRAS"
    assert kras.protein_change == "p.G12V"
    assert kras.transcript == "NM_004985"


def test_parse_maf_tp53():
    records = parse_maf(SAMPLE_MAF)
    tp53 = records[1]
    assert tp53.gene == "TP53"
    assert tp53.vaf == pytest.approx(90 / 300)
    assert tp53.depth == 300
    assert tp53.protein_change == "p.R248W"


def test_parse_maf_empty():
    records = parse_maf("")
    assert records == []


def test_parse_maf_missing_columns():
    content = "Hugo_Symbol\tChromosome\nKRAS\t12\n"
    with pytest.raises(ValueError, match="Missing required MAF columns"):
        parse_maf(content)


def test_parse_maf_with_comments():
    content = "# Comment line\n" + SAMPLE_MAF
    records = parse_maf(content)
    assert len(records) == 3
