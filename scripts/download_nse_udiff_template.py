"""Download NSE UDiFF bhavcopy files using a URL template.

This script is for cases where the NSE download URL follows a repeatable date
pattern and the user has copied the real download URL from the browser.

Example usage:

    python scripts/download_nse_udiff_template.py \
      --url-template "https://example.com/BhavCopy_NSE_CM_0_0_0_{yyyymmdd}_F_0000.csv.zip" \
      --start 2026-01-01 \
      --end 2026-01-31 \
      --output-dir data/raw/udiff_bhavcopy

Replace the example URL with the real NSE URL copied from the browser download.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import time

import pandas as pd
import requests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download NSE UDiFF bhavcopy files by URL template.")
    parser.add_argument("--url-template", required=True, help="URL containing {yyyymmdd} placeholder.")
    parser.add_argument("--start", required=True, help="Start date in YYYY-MM-DD format.")
    parser.add_argument("--end", required=True, help="End date in YYYY-MM-DD format.")
    parser.add_argument("--output-dir", default="data/raw/udiff_bhavcopy")
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds to wait between requests.")
    parser.add_argument("--include-weekends", action="store_true", help="Try weekend dates too.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    dates = pd.date_range(args.start, args.end, freq="D")
    if not args.include_weekends:
        dates = dates[dates.weekday < 5]

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/zip,text/csv,*/*",
        }
    )

    success = 0
    failed = []
    for date in dates:
        yyyymmdd = date.strftime("%Y%m%d")
        url = args.url_template.format(yyyymmdd=yyyymmdd)
        output_path = output_dir / f"BhavCopy_NSE_CM_0_0_0_{yyyymmdd}_F_0000.csv.zip"

        if output_path.exists() and output_path.stat().st_size > 0:
            print(f"SKIP existing: {output_path.name}")
            continue

        try:
            response = session.get(url, timeout=30)
            if response.status_code == 200 and response.content:
                output_path.write_bytes(response.content)
                print(f"OK {yyyymmdd}: {output_path}")
                success += 1
            else:
                print(f"FAIL {yyyymmdd}: HTTP {response.status_code}")
                failed.append(yyyymmdd)
        except Exception as exc:
            print(f"ERROR {yyyymmdd}: {exc}")
            failed.append(yyyymmdd)
        time.sleep(args.sleep)

    print(f"Downloaded {success} files.")
    if failed:
        print("Failed dates:")
        for item in failed:
            print(item)


if __name__ == "__main__":
    main()
