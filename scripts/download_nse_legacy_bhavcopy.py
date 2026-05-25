"""Download legacy NSE CM bhavcopy ZIP files.

Legacy NSE CM bhavcopy files commonly use file names like:

    cm01JAN2021bhav.csv.zip

and were used before the UDiFF transition.

The archive URL pattern can change, so this script tries the common NSE archive
location. If NSE changes access rules, download one old bhavcopy manually and
adjust BASE_URL_TEMPLATE.

Example:

    python scripts/download_nse_legacy_bhavcopy.py \
      --start 2021-01-01 \
      --end 2024-07-05 \
      --output-dir data/raw/legacy_bhavcopy
"""

from __future__ import annotations

import argparse
from pathlib import Path
import time

import pandas as pd
import requests

BASE_URL_TEMPLATE = "https://archives.nseindia.com/content/historical/EQUITIES/{yyyy}/{mon}/cm{dd}{mon}{yyyy}bhav.csv.zip"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download legacy NSE CM bhavcopy ZIP files.")
    parser.add_argument("--start", required=True, help="Start date in YYYY-MM-DD format.")
    parser.add_argument("--end", required=True, help="End date in YYYY-MM-DD format.")
    parser.add_argument("--output-dir", default="data/raw/legacy_bhavcopy")
    parser.add_argument("--sleep", type=float, default=1.0)
    parser.add_argument("--include-weekends", action="store_true")
    return parser.parse_args()


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/zip,application/octet-stream,*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.nseindia.com/all-reports",
        }
    )
    return session


def make_url(date: pd.Timestamp) -> str:
    dd = date.strftime("%d")
    mon = date.strftime("%b").upper()
    yyyy = date.strftime("%Y")
    return BASE_URL_TEMPLATE.format(dd=dd, mon=mon, yyyy=yyyy)


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    dates = pd.date_range(args.start, args.end, freq="D")
    if not args.include_weekends:
        dates = dates[dates.weekday < 5]

    session = make_session()
    success = 0
    failed: list[str] = []

    for date in dates:
        dd = date.strftime("%d")
        mon = date.strftime("%b").upper()
        yyyy = date.strftime("%Y")
        file_name = f"cm{dd}{mon}{yyyy}bhav.csv.zip"
        output_path = output_dir / file_name

        if output_path.exists() and output_path.stat().st_size > 0:
            print(f"SKIP existing: {file_name}")
            continue

        url = make_url(date)
        try:
            response = session.get(url, timeout=60)
            if response.status_code == 200 and response.content and response.content[:2] == b"PK":
                output_path.write_bytes(response.content)
                print(f"OK {date.strftime('%d-%b-%Y')}: {file_name}")
                success += 1
            else:
                print(f"FAIL {date.strftime('%d-%b-%Y')}: HTTP {response.status_code}, bytes={len(response.content)}")
                failed.append(date.strftime("%d-%b-%Y"))
        except requests.RequestException as exc:
            print(f"ERROR {date.strftime('%d-%b-%Y')}: {exc}")
            failed.append(date.strftime("%d-%b-%Y"))

        time.sleep(args.sleep)

    print(f"Downloaded {success} files.")
    if failed:
        print("Failed dates:")
        for item in failed:
            print(item)


if __name__ == "__main__":
    main()
