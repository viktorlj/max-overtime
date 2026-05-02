# Max Overtime

Track variant allele frequency (VAF) changes across multiple timepoints. Upload variant call files from sequential samples, and Max Overtime matches variants by genomic coordinates, plots VAF trajectories over time, and exports results for reporting or downstream analysis.

Built for monitoring clonal evolution, treatment response, and disease progression in cancer genomics.

## Features

- **Multi-format input** -- VCF, MAF, TSV, and CSV with flexible column name recognition
- **Unlimited timepoints** -- compare two or more sequential samples
- **Interactive VAF plot** -- Plotly line chart with hover details (gene, VAF, depth, protein change)
- **Variant table** -- select/deselect rows to control which variants appear in the plot
- **Export** -- PDF (publication-quality vector), Excel (wide-format), TSV (long-format)
- **Bilingual UI** -- English and Swedish

## Quickstart

Requires Python 3.11+.

```bash
git clone https://github.com/viktorlj/max-overtime.git
cd max-overtime
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
python run.py
```

Open http://127.0.0.1:8050 in your browser.

### Optional: VCF support via cyvcf2

```bash
uv pip install -e ".[vcf]"
```

## Usage

1. Enter a **Sample ID**
2. Set a **date** and **upload a variant file** for each timepoint (minimum 2)
3. Click **Run Analysis**
4. Use the variant table to select which variants to plot
5. Export results as PDF, Excel, or TSV

## Caveats

1. **For research use and clinical decision support only.** Not a standalone diagnostic device. Outputs may be incomplete or incorrect and must be reviewed by qualified experts in the full clinical, laboratory, and histopathological context. The authors assume no responsibility for clinical decisions or other consequences of use.
2. Input files, variant normalization, and sequencing depth should be reviewed before interpreting longitudinal VAF changes.

## Supported file formats

| Format | Extension | VAF source |
|--------|-----------|------------|
| VCF | `.vcf` | FORMAT fields: AF, AD, or DP |
| MAF | `.maf` | `t_alt_count` / `t_ref_count` |
| TSV/CSV | `.tsv`, `.csv` | `vaf` column or `alt_count` / `ref_count` |

TSV/CSV files must contain columns for chromosome, position, reference allele, and alternate allele. Column names are matched flexibly (e.g. `chrom`, `chromosome`, `chr`, `#chrom` all work).

## Project structure

```
app/                  Dash application
  callbacks/          Callback modules (upload, processing, plot, export, ...)
  components/         UI components (navbar, upload section, plot, table, ...)
  layout.py           Main layout
src/                  Core logic (no Dash dependency)
  parsers/            VCF, MAF, TSV parsers
  processing/         Merge and export functions
  i18n/               Translations (EN/SV)
tests/                pytest suite
assets/               CSS
run.py                Entry point
```

## Running tests

```bash
source .venv/bin/activate
pytest
```

## Tech stack

- [Dash](https://dash.plotly.com/) + [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- [Plotly](https://plotly.com/python/) for interactive charts
- [Polars](https://pola.rs/) for data processing
- [Kaleido](https://github.com/plotly/Kaleido) for PDF export

## License

MIT
