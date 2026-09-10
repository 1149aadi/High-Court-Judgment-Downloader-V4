# High Court Judgment Downloader V4

A Python + Playwright utility for downloading judgment PDFs from supported Indian High Court / eCourts pages.

## Important

This repository incrementally extends the **working V4 baseline** with a conservative
multi-court batch workflow. Act detection is intentionally not included.

## Main Features

- Playwright-based browser automation
- Manual CAPTCHA workflow
- Selection of one to six High Court/bench entries per batch
- Isolated browser context per selected court
- Open-all-first, then sequential court processing after one confirmation
- Judgment-only PDF downloading
- Pagination handling
- Existing PDF skip logic
- Successful-URL duplicate protection and bounded download retries
- Optional minimum PDF page count (`MIN_PDF_PAGES`, default `1`)
- Court/date-wise output folders
- Download report generation
- CSV download log
- Chrome first, Edge fallback
- Windows-compatible workflow
- Can be packaged as a Windows `.exe` using PyInstaller

## CAPTCHA

CAPTCHA is completed manually by the user.

This project does not attempt to bypass, solve, OCR, or circumvent CAPTCHA.

## Requirements

- Windows 10/11 recommended
- Python 3.10+
- Google Chrome or Microsoft Edge
- Playwright and PyMuPDF (page parsing is used only when `MIN_PDF_PAGES > 1`)

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

Run the Python version:

```bash
py High_Court_Judgment_Downloader_v4.py
```

## Build Windows EXE

Run:

```text
build_exe.bat
```

The build uses PyInstaller `--onedir` with the console visible because the application requires manual CAPTCHA confirmation and shows live progress.

## Output

Judgments are saved under the user's Downloads folder in:

```text
High_Court_Judgments/
```

with separate court/date folders and run reports.

## Notes

- Use responsibly and avoid excessive automated requests to public court servers.
- Court websites can change their HTML, URLs, selectors, or session behavior over time.
- This repository is intended as the stable V4 baseline for future development.

## License

MIT License. See `LICENSE`.
