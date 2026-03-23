# MaxOvertime v2 — Project Plan

## Objective
Rebuild the MaxOvertime web app from a Flask/Skeleton/Swedish-only app to a modern Plotly Dash application with bilingual support (EN/SV), single-file-per-timepoint input, and multiple format support (VCF, MAF, TSV/CSV).

## Current Status
**v2 rebuild complete.** All core functionality implemented and tested. The app initializes successfully with 10 callbacks registered. Parser unit tests (17/17) pass. End-to-end pipeline (parse → merge → export) verified.

## Active Tasks
- [ ] Manual browser testing with real variant files
- [ ] Clean up old Flask files once v2 is validated

## Key Findings
- polars `write_json`/`read_json` roundtrip works well for dcc.Store serialization
- Pattern-matching callbacks (`MATCH`/`ALL`) used for dynamic timepoint management
- Three VAF extraction strategies for VCF (AF field, AD computation, DP+AD fallback)

## Open Questions
- Should we add cyvcf2 as hard dependency or keep it optional?
- PDF export with kaleido needs testing on the deployment server

## Data Inventory
- No data files in the repo — all data is uploaded client-side at runtime
