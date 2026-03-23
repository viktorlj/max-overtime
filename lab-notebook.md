# Lab Notebook — MaxOvertime

## 2026-02-23: v2 Rebuild Complete

### Summary
Rebuilt MaxOvertime from scratch using Plotly Dash + dash-bootstrap-components (FLATLY theme). Replaced the 2019 Flask app with a modern single-page architecture.

### What was done
1. **Phase 1 — Foundation**: Created pyproject.toml, run.py entry point, data models (VariantKey, VariantRecord), i18n translation system (EN/SV), Dash app factory
2. **Phase 2 — Parsers**: Implemented TSV/CSV, MAF, and VCF parsers with flexible column detection. 17 unit tests, all passing.
3. **Phase 3 — Processing**: Merge module (cross-timepoint variant matching on chrom/pos/ref/alt) and export module (PDF via kaleido, Excel via xlsxwriter, TSV)
4. **Phase 4 — UI Components**: Navbar with language toggle, dynamic upload section with pattern-matching callbacks, interactive DataTable with row selection, plot section with download buttons
5. **Phase 5 — Callbacks**: Language toggle, dynamic timepoint add/remove, processing pipeline (parse→merge→store), plot rendering with variant filtering, export downloads
6. **Phase 6 — Polish**: Custom CSS, logo copied to assets/, updated .gitignore

### Key design decisions
- Client-side state via `dcc.Store` (no server files)
- polars for all data operations
- Manual VCF parsing with optional cyvcf2
- Simple dict-based i18n with `t(key, lang)` helper

### Test results
- 17/17 parser unit tests pass
- App factory creates successfully with 10 callbacks
- End-to-end pipeline (TSV parse → merge → Excel/TSV export) verified
- JSON serialization roundtrip for dcc.Store confirmed working

### New project structure
```
MaxOvertime/
├── pyproject.toml, run.py
├── assets/ (logo, CSS)
├── src/parsers/ (common, vcf, maf, tsv)
├── src/processing/ (merge, export)
├── src/i18n/ (translations)
├── app/ (factory, layout, components/, callbacks/)
└── tests/test_parsers/
```
