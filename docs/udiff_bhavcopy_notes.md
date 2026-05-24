# NSE UDiFF Bhavcopy Notes

The uploaded sample file was:

```text
BhavCopy_NSE_CM_0_0_0_20260101_F_0000.csv.zip
```

It contains one CSV file with the new NSE CM UDiFF bhavcopy format.

## Observed raw columns

Important columns include:

```text
TradDt
BizDt
Sgmt
Src
FinInstrmTp
FinInstrmId
ISIN
TckrSymb
SctySrs
FinInstrmNm
OpnPric
HghPric
LwPric
ClsPric
LastPric
PrvsClsgPric
TtlTradgVol
TtlTrfVal
TtlNbOfTxsExctd
NewBrdLotQty
```

## Standardized project columns

The repo maps them to:

```text
date
business_date
segment
source
instrument_type
instrument_id
isin
symbol
series
security_name
open
high
low
close
last
prev_close
volume
traded_value
num_trades
board_lot_qty
```

## Uploaded sample summary

The 01-Jan-2026 file contained:

```text
all rows: 3,227
EQ rows: 2,383
unique EQ symbols: 2,383
```

For factor research, keep only:

```text
series = EQ
```

## Why this format is important

This is much better than downloading stock-by-stock files because one daily UDiFF bhavcopy file contains thousands of securities for that trading day.

## Next data target

Download a full month of UDiFF bhavcopy ZIP files, preferably all trading days in one month, and upload them as a single ZIP folder.

Recommended first month:

```text
January 2026
```

Once a full month works, expand to a full year and then to the full study period.
