# secfsdstools E2E scaffold (free, public SEC FSD)

Caches SEC Financial Statement Data Sets under `~/secfsdstools` (parquet + SQLite). No paid APIs.

## Quick start
```bash
conda env create -f environment.yml
conda activate secfsd
make update              # ~2–4+ GB on first run
make index               # demo index search & filings
CIK=320193 make single   # Apple 2022 10-K by ADSH (example inside)
CIK=320193 make company  # all Apple 10-K raw joins
CIK=320193 make present  # BS/IS/CF (current & previous period)
CIK=320193 make standard # standardized comparable BS/IS/CF
