"""Tests for VCF parser."""

from src.parsers.vcf import parse_vcf
from tests.conftest import SAMPLE_VCF

import pytest


def test_parse_vcf_basic():
    records = parse_vcf(SAMPLE_VCF)
    assert len(records) == 2

    kras = records[0]
    assert kras.key.chrom == "12"
    assert kras.key.pos == 25398284
    assert kras.key.ref == "C"
    assert kras.key.alt == "A"
    assert kras.vaf == pytest.approx(0.45)
    assert kras.depth == 500
    assert kras.gene == "KRAS"
    assert kras.filter_status == "PASS"


def test_parse_vcf_second_variant():
    records = parse_vcf(SAMPLE_VCF)
    tp53 = records[1]
    assert tp53.key.chrom == "17"
    assert tp53.vaf == pytest.approx(0.30)
    assert tp53.depth == 300


def test_parse_vcf_ad_fallback():
    """VAF computed from AD when AF is missing."""
    content = """\
##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SAMPLE
1	100	.	A	T	50	PASS	DP=200	GT:AD:DP	0/1:120,80:200
"""
    records = parse_vcf(content)
    assert len(records) == 1
    assert records[0].vaf == pytest.approx(80 / 200)
    assert records[0].depth == 200


def test_parse_vcf_multiallelic():
    content = """\
##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SAMPLE
1	100	.	A	T,C	50	PASS	DP=200	GT:AF	0/1:0.3,0.1
"""
    records = parse_vcf(content)
    assert len(records) == 2
    assert records[0].key.alt == "T"
    assert records[1].key.alt == "C"


def test_parse_vcf_empty():
    records = parse_vcf("")
    assert records == []


def test_parse_vcf_skip_star_alt():
    content = """\
##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SAMPLE
1	100	.	A	*	50	PASS	DP=200	GT:DP	0/1:200
"""
    records = parse_vcf(content)
    assert records == []
