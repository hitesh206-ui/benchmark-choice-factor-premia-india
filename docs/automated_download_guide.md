# Automated NSE Bhavcopy Download Guide

NSE's website lets users select only one archive date at a time. For research, manually downloading each date is too slow. The practical alternative is to automate downloads after identifying the real download URL pattern.

## Option 1: URL-template downloader

Use this if the download link has a repeatable date pattern.

### Step 1: Download one file manually

Download one UDiFF bhavcopy ZIP manually from the NSE All Reports page.

Example file name:

```text
BhavCopy_NSE_CM_0_0_0_20260101_F_0000.csv.zip
```

### Step 2: Copy the download URL

In Chrome or Edge:

1. Press `Ctrl + J` to open Downloads.
2. Find the downloaded bhavcopy file.
3. Right-click the source link or file entry.
4. Choose `Copy link address` if available.
5. Paste the link somewhere temporarily.

### Step 3: Replace the date with placeholder

If the copied link contains the date, replace the date with:

```text
{yyyymmdd}
```

Example template:

```text
https://example.com/BhavCopy_NSE_CM_0_0_0_{yyyymmdd}_F_0000.csv.zip
```

### Step 4: Run the downloader

```bash
python scripts/download_nse_udiff_template.py \
  --url-template "PASTE_REAL_URL_TEMPLATE_HERE" \
  --start 2026-01-01 \
  --end 2026-01-31 \
  --output-dir data/raw/udiff_bhavcopy
```

The script skips weekends by default.

## Option 2: Browser automation

If NSE blocks direct URL-template downloads, use browser automation such as Selenium or Playwright. This approach opens the page like a normal user, changes the date, and clicks the download button.

This is slower than direct URLs, but much faster than manual clicking.

## Recommended workflow

1. Try the URL-template downloader first.
2. If it fails because NSE blocks direct requests, switch to browser automation.
3. Start with one month.
4. After one month works, download one full year.
5. After one year works, expand to the full study period.

## Data integrity checks

After downloading, check:

- number of ZIP files downloaded
- file sizes greater than zero
- dates covered
- whether the files unzip correctly
- whether EQ rows are present

## Important warning

Respect NSE website terms, rate limits, and server load. Use sleep delays between requests and avoid aggressive scraping.
