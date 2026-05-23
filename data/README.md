# Data Folder

This folder is for local research data only.

## Folder purpose

```text
data/raw/        Original files downloaded from public sources
data/interim/    Partially cleaned files
data/processed/  Final research-ready datasets
```

## Important rule

Large data files are ignored by Git and should generally not be committed to this repository.

The project should remain reproducible through:

1. documented data sources,
2. collection instructions,
3. cleaning scripts,
4. processing scripts,
5. variable definitions.

## Expected local files later

Possible local files may include:

```text
data/raw/prices.csv
data/raw/index_constituents.csv
data/raw/market_cap.csv
data/raw/book_value.csv
data/processed/monthly_panel.csv
```

These file names are placeholders and may change once the exact public data sources are finalized.
