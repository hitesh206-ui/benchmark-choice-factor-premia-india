.PHONY: install validate-panel validate-factors build-panel build-factors analyze clean

install:
	pip install -r requirements.txt

build-panel:
	python scripts/build_monthly_panel.py --input data/raw/prices.csv --output data/processed/monthly_panel.csv

validate-panel:
	python scripts/validate_monthly_panel.py --input data/processed/monthly_panel.csv --output outputs/tables/monthly_panel_validation.json

build-factors:
	python scripts/build_factor_returns.py --input data/processed/monthly_panel.csv --output outputs/factor_returns/factor_returns_equal_weighted.csv

validate-factors:
	python scripts/validate_factor_returns.py --input outputs/factor_returns/factor_returns_equal_weighted.csv --output outputs/tables/factor_returns_validation.json

analyze:
	python scripts/analyze_factor_returns.py --input outputs/factor_returns/factor_returns_equal_weighted.csv --output outputs/tables/factor_summary_equal_weighted.csv

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.json outputs/factor_returns/*.csv outputs/figures/*.png
