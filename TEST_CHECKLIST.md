# V4 Test Checklist

Test with a small one-day result set before attempting a large batch.

## First smoke test

1. Run `python High_Court_Judgment_Downloader_v4.py` on Windows.
2. Select one known-working eCourts bench.
3. Enter both dates and the CAPTCHA manually, submit, wait for the table, and press
   Enter once in the console.
4. Confirm only Judgment/Judgement links are downloaded; ordinary and interim order
   links in mixed rows must remain untouched.
5. Confirm PDFs open normally and appear beneath
   `Downloads\High_Court_Judgments\Court_Name\DD-MM-YYYY`.
6. Check that `Download_Report.txt` totals match `Download_Log.csv` and that every
   detected judgment link has one CSV row.

## Batch and reliability tests

- Select two benches on the same eCourts domain. Confirm both pages open before the
  single Enter prompt and that their cookies/CAPTCHAs remain independent.
- Confirm downloads finish court-by-court rather than concurrently.
- Re-run the same search and confirm valid files receive `ALREADY_DOWNLOADED`.
- Use a result set containing the same document URL twice and confirm the later row is
  retained in CSV as `DUPLICATE_SKIPPED`.
- Exercise multiple pages. Confirm each page downloads fully before Next, and disabled,
  empty, or repeated Next pages stop safely.
- Temporarily set `MIN_PDF_PAGES = 4`; confirm shorter documents are removed and logged
  as `SKIPPED_SHORT_PDF`. Restore it to `1` for maximum normal speed.
- Deliberately close one court page in a multi-court batch. Confirm its debug folder is
  created and later courts continue.
- Smoke-test each special engine: Delhi, Himachal Pradesh, and one `generic` court.

## Packaging

1. Run `build_exe.bat` from a normal Command Prompt.
2. Launch the generated onedir executable under
   `dist\High_Court_Judgment_Downloader_V4`.
3. Confirm the console remains visible and installed Chrome is chosen first.

