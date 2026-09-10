# Changelog

## V4 batch reliability update

- Preserved all 41 court/bench definitions and the existing Playwright-only Chrome,
  Edge, and Chromium fallback order.
- Added selection of one to six courts per batch. All selected sites open first in
  separate browser contexts; one console confirmation starts sequential processing.
- Retained manual CAPTCHA and manual date/search submission. No CAPTCHA automation,
  OCR, or circumvention was added.
- Centralized the four existing result engines (`ecourts`, `delhi`, `himachal`, and
  `generic`) behind shared download, validation, pagination, logging, and reporting.
- Tightened mixed-row filtering so eCourts downloads only links specifically labelled
  Judgment/Judgement (including Copy of Judgment/Judgement).
- Added batch-wide successful-URL duplicate protection without suppressing CSV rows or
  blocking a retry after a failed download.
- Added bounded retries, authenticated Playwright-context HTTP requests, `.part` files,
  PDF header/end-marker checks, and browser download/popup fallback.
- Added optional `MIN_PDF_PAGES` filtering with PyMuPDF; its default of `1` avoids page
  parsing during ordinary runs.
- Added repeated/empty-page detection and a 100-page hard safety limit.
- Expanded per-court text and CSV reports, a final batch summary, and per-court debug
  screenshot/HTML/error artifacts when result processing fails.
- Shortened and sanitized filenames for Windows and retained the existing output folder
  hierarchy.

