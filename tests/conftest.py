"""Shared test fixtures for MaxOvertime."""


SAMPLE_VCF = """\
##fileformat=VCFv4.2
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
##FORMAT=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SAMPLE1
chr12	25398284	.	C	A	100	PASS	DP=500;ANN=A|missense_variant|MODERATE|KRAS|ENSG00000133703|transcript|NM_004985.5|protein_coding|2/6|c.35G>T|p.Gly12Val||	GT:AD:DP:AF	0/1:275,225:500:0.45
chr17	7577121	.	G	A	200	PASS	DP=300	GT:AD:DP:AF	0/1:210,90:300:0.30
"""

SAMPLE_MAF = """\
Hugo_Symbol	Chromosome	Start_Position	End_Position	Reference_Allele	Tumor_Seq_Allele2	Variant_Classification	HGVSp_Short	Transcript_ID	t_alt_count	t_ref_count	t_depth
KRAS	12	25398284	25398284	C	A	Missense_Mutation	p.G12V	NM_004985	225	275	500
TP53	17	7577121	7577121	G	A	Missense_Mutation	p.R248W	NM_000546	90	210	300
IDH1	2	209113112	209113112	G	A	Missense_Mutation	p.R132H	NM_005896	25	475	500
"""

SAMPLE_TSV = """\
Gene	Chromosome	Position	Ref	Alt	VAF	Depth	Transcript	Protein_Change
KRAS	chr12	25398284	C	A	0.45	500	NM_004985	p.G12V
TP53	chr17	7577121	G	A	0.30	300	NM_000546	p.R248W
"""

SAMPLE_CSV = """\
Gene,Chromosome,Position,Ref,Alt,VAF,Depth,Transcript,Protein_Change
KRAS,chr12,25398284,C,A,0.45,500,NM_004985,p.G12V
TP53,chr17,7577121,G,A,0.30,300,NM_000546,p.R248W
"""
