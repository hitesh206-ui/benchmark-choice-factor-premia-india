"""Download NSE report files from the /api/reports endpoint.

This downloader is designed for URLs like:

https://www.nseindia.com/api/reports?...&date=07-Jan-2026&type=equities&mode=single

The script changes only the date parameter and saves one ZIP per date.

Usage example:

    python scripts/download_nse_reports_api.py \
      --start 2026-01-01 \
      --end 2026-01-31 \
      --output-dir data/raw/udiff_bhavcopy
"""

from __future__ import annotations

import argparse
from pathlib import Path
import time
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import pandas as pd
import requests

BASE_URL = "https://www.nseindia.com/api/reports?archives=%5B%7B%22name%22%3A%22CM-UDiFF%20Common%20Bhavcopy%20Final%20(zip)%22%2C%22type%22%3A%22daily-reports%22%2C%22category%22%3A%22capital-market%22%2C%22section%22%3A%22equities%22%7D%5D&date=07-Jan-2026&type=equities&mode=single"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download NSE UDiFF bhavcopy files from /api/reports.")
    parser.add_argument("--start", required=True, help="Start date in YYYY-MM-DD format.")
    parser.add_argument("--end", required=True, help="End date in YYYY-MM-DD format.")
    parser.add_argument("--output-dir", default="data/raw/udiff_bhavcopy")
    parser.add_argument("--sleep", type=float, default=2.0, help="Seconds to wait between requests.")
    parser.add_argument("--include-weekends", action="store_true")
    return parser.parse_args()


def make_url(base_url: str, date_string: str) -> str:
    """Replace the date query parameter in the NSE reports API URL."""
    parsed = urlparse(base_url)
    query = parse_qs(parsed.query)
    query["date"] = [date_string]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def make_session() -> requests.Session:
    """Create a browser-like session for NSE requests."""
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/zip,application/octet-stream,*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.nseindia.com/all-reports",
        }
    )
    try:
        session.get("https://www.nseindia.com", timeout=20)
    except requests.RequestException:
        pass
    return session


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
        nse_date = date.strftime("%d-%b-%Y")
        yyyymmdd = date.strftime("%Y%m%d")
        output_path = output_dir / f"BhavCopy_NSE_CM_0_0_0_{yyyymmdd}_F_0000.csv.zip"

        if output_path.exists() and output_path.stat().st_size > 0:
            print(f"SKIP existing: {output_path.name}")
            continue

        url = make_url(BASE_URL, nse_date)
        try:
            response = session.get(url, timeout=60)
            if response.status_code == 200 and response.content and response.content[:2] == b"PK":
                output_path.write_bytes(response.content)
                print(f"OK {nse_date}: {output_path.name}")
                success += 1
            else:
                print(f"FAIL {nse_date}: HTTP {response.status_code}, bytes={len(response.content)}")
                failed.append(nse_date)
        except requests.RequestException as exc:
            print(f"ERROR {nse_date}: {exc}")
            failed.append(nse_date)

        time.sleep(args.sleep)

    print(f"Downloaded {success} files.")
    if failed:
        print("Failed dates:")
        for item in failed:
            print(item)


if __name__ == "__main__":
    main()
