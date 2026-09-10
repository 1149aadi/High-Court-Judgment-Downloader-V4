from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from pathlib import Path
from datetime import datetime
import csv
import re
import time


APP_TITLE = "HIGH COURT JUDGMENT DOWNLOADER - V4"


# ============================================================
# COURT CONFIGURATION
# ============================================================

COURTS = {
    "1": {
        "name": 'Andhra Pradesh High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=2&dist_cd=1&court_code=1&stateNm=Andhra%20Pradesh',
        "folder": 'Andhra_Pradesh_High_Court',
    },

    "2": {
        "name": 'Chhattisgarh High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=18&dist_cd=1&court_code=1&stateNm=Chhattisgarh',
        "folder": 'Chhattisgarh_High_Court',
    },

    "3": {
        "name": 'Calcutta High Court - Original Side',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=16&dist_cd=1&court_code=1&stateNm=Calcutta',
        "folder": 'Calcutta_HC_Original_Side',
    },

    "4": {
        "name": 'Calcutta High Court - Appellate Side',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=16&dist_cd=1&court_code=3&stateNm=Calcutta',
        "folder": 'Calcutta_HC_Appellate_Side',
    },

    "5": {
        "name": 'Calcutta High Court - Jalpaiguri Circuit Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=16&dist_cd=1&court_code=2&stateNm=Calcutta',
        "folder": 'Calcutta_HC_Jalpaiguri_Bench',
    },

    "6": {
        "name": 'Calcutta High Court - Port Blair Circuit Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=16&dist_cd=1&court_code=4&stateNm=Calcutta',
        "folder": 'Calcutta_HC_Port_Blair_Bench',
    },

    "7": {
        "name": 'Madras High Court - Chennai',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=10&dist_cd=1&court_code=1&stateNm=Madras',
        "folder": 'Madras_HC_Chennai',
    },

    "8": {
        "name": 'Madras High Court - Madurai Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=10&dist_cd=1&court_code=2&stateNm=Madras',
        "folder": 'Madras_HC_Madurai',
    },

    "9": {
        "name": 'Kerala High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=4&dist_cd=1&court_code=1&stateNm=Kerala',
        "folder": 'Kerala_High_Court',
    },

    "10": {
        "name": 'Punjab & Haryana High Court',
        "engine": 'generic',
        "url": 'https://new.phhc.gov.in/judgement/free-text-search',
        "folder": 'Punjab_Haryana_High_Court',
    },

    "11": {
        "name": 'Patna High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=8&dist_cd=1&court_code=1&stateNm=Patna',
        "folder": 'Patna_High_Court',
    },

    "12": {
        "name": 'Orissa High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=11&dist_cd=1&court_code=1&stateNm=Odisha',
        "folder": 'Orissa_High_Court',
    },

    "13": {
        "name": 'Meghalaya High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=21&dist_cd=1&court_code=1&stateNm=Meghalaya',
        "folder": 'Meghalaya_High_Court',
    },

    "14": {
        "name": 'Manipur High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=25&dist_cd=1&court_code=1&stateNm=Manipur',
        "folder": 'Manipur_High_Court',
    },

    "15": {
        "name": 'Madhya Pradesh High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=7&dist_cd=1&court_code=1&stateNm=Madhya%20Pradesh',
        "folder": 'Madhya_Pradesh_High_Court',
    },

    "16": {
        "name": 'Telangana High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=29&dist_cd=1&court_code=1&stateNm=Telangana',
        "folder": 'Telangana_High_Court',
    },

    "17": {
        "name": 'Tripura High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=20&dist_cd=1&court_code=1&stateNm=Tripura',
        "folder": 'Tripura_High_Court',
    },

    "18": {
        "name": 'Rajasthan High Court - Jodhpur',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=9&dist_cd=1&court_code=2&stateNm=Rajasthan',
        "folder": 'Rajasthan_HC_Jodhpur',
    },

    "19": {
        "name": 'Rajasthan High Court - Jaipur',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=9&dist_cd=1&court_code=1&stateNm=Rajasthan',
        "folder": 'Rajasthan_HC_Jaipur',
    },

    "20": {
        "name": 'Karnataka High Court - Bengaluru',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=3&dist_cd=1&court_code=1&stateNm=Karnataka',
        "folder": 'Karnataka_HC_Bengaluru',
    },

    "21": {
        "name": 'Karnataka High Court - Dharwad Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=3&dist_cd=1&court_code=2&stateNm=Karnataka',
        "folder": 'Karnataka_HC_Dharwad',
    },

    "22": {
        "name": 'Karnataka High Court - Kalaburagi Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=3&dist_cd=1&court_code=3&stateNm=Karnataka',
        "folder": 'Karnataka_HC_Kalaburagi',
    },

    "23": {
        "name": 'Jharkhand High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=7&dist_cd=1&court_code=1&stateNm=Jharkhand',
        "folder": 'Jharkhand_High_Court',
    },

    "24": {
        "name": 'Jammu & Kashmir High Court - Jammu Wing',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=12&dist_cd=1&court_code=1&stateNm=Jammu%20and%20Kashmir',
        "folder": 'Jammu_Kashmir_HC_Jammu',
    },

    "25": {
        "name": 'Jammu & Kashmir High Court - Srinagar Wing',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=12&dist_cd=1&court_code=2&stateNm=Jammu%20and%20Kashmir',
        "folder": 'Jammu_Kashmir_HC_Srinagar',
    },

    "26": {
        "name": 'Gauhati High Court - Principal Seat',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=6&dist_cd=1&court_code=1&stateNm=Assam',
        "folder": 'Gauhati_HC_Principal_Seat',
    },

    "27": {
        "name": 'Gauhati High Court - Aizawl Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=6&dist_cd=1&court_code=3&stateNm=Assam',
        "folder": 'Gauhati_HC_Aizawl',
    },

    "28": {
        "name": 'Gauhati High Court - Kohima Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=6&dist_cd=1&court_code=2&stateNm=Assam',
        "folder": 'Gauhati_HC_Kohima',
    },

    "29": {
        "name": 'Gauhati High Court - Itanagar Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=6&dist_cd=1&court_code=4&stateNm=Assam',
        "folder": 'Gauhati_HC_Itanagar',
    },

    "30": {
        "name": 'Himachal Pradesh High Court',
        "engine": 'himachal',
        "url": 'https://highcourt.hp.gov.in/',
        "folder": 'Himachal_Pradesh_High_Court',
    },

    "31": {
        "name": 'Gujarat High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=17&dist_cd=1&court_code=1&stateNm=Gujarat',
        "folder": 'Gujarat_High_Court',
    },

    "32": {
        "name": 'Uttarakhand High Court',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=15&dist_cd=1&court_code=1&stateNm=Uttarakhand',
        "folder": 'Uttarakhand_High_Court',
    },

    "33": {
        "name": 'Sikkim High Court - Date Wise Judgments',
        "engine": 'generic',
        "url": 'https://hcs.gov.in/hcs/hcourt/hg_judgement_date_search',
        "folder": 'Sikkim_High_Court',
    },

    "34": {
        "name": 'Allahabad High Court - All Benches (eLegalix)',
        "engine": 'generic',
        "url": 'https://elegalix.allahabadhighcourt.in/elegalix/WebJudgmentDateSearch.do',
        "folder": 'Allahabad_High_Court_All_Benches',
    },

    "35": {
        "name": 'Delhi High Court - Date Wise Judgments',
        "engine": 'delhi',
        "url": 'https://delhihighcourt.nic.in/app/judgement-dates-wise',
        "folder": 'Delhi_High_Court',
    },

    "36": {
        "name": 'Bombay High Court - Original Side',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=1&dist_cd=1&court_code=2&stateNm=Bombay',
        "folder": 'Bombay_HC_Original_Side',
    },

    "37": {
        "name": 'Bombay High Court - Appellate Side',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=1&dist_cd=1&court_code=1&stateNm=Bombay',
        "folder": 'Bombay_HC_Appellate_Side',
    },

    "38": {
        "name": 'Bombay High Court - Aurangabad Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=1&dist_cd=1&court_code=3&stateNm=Bombay',
        "folder": 'Bombay_HC_Aurangabad',
    },

    "39": {
        "name": 'Bombay High Court - Kolhapur Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=1&dist_cd=1&court_code=7&stateNm=Bombay',
        "folder": 'Bombay_HC_Kolhapur',
    },

    "40": {
        "name": 'Bombay High Court - Nagpur Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=1&dist_cd=1&court_code=4&stateNm=Bombay',
        "folder": 'Bombay_HC_Nagpur',
    },

    "41": {
        "name": 'Bombay High Court - Goa Bench',
        "engine": 'ecourts',
        "url": 'https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?state_cd=1&dist_cd=1&court_code=5&stateNm=Bombay',
        "folder": 'Bombay_HC_Goa',
    },

}


# ============================================================
# CONFIGURATION
# ============================================================

MIN_PDF_PAGES = 1              # Set to 4 (for example) to keep 4+ page PDFs.
DOWNLOAD_DELAY = 0.5            # Polite delay between sequential downloads.
MAX_RETRIES = 3
RETRY_DELAYS = (1.0, 2.5, 5.0)
MAX_RESULT_PAGES = 100
MIN_VALID_PDF_BYTES = 500
RESULT_WAIT_MS = 15_000

# Status values are deliberately machine-friendly for CSV consumers.
DOWNLOADED = "DOWNLOADED"
ALREADY_DOWNLOADED = "ALREADY_DOWNLOADED"
DUPLICATE_SKIPPED = "DUPLICATE_SKIPPED"
SKIPPED_SHORT_PDF = "SKIPPED_SHORT_PDF"
FAILED = "FAILED"

LOG_FIELDS = [
    "Court", "Selected From Date", "Selected To Date", "Result Page",
    "Court Serial Number", "Case Number", "Order/Judgment Date", "PDF URL",
    "File Name", "Page Count", "Status", "Error Message",
]


# ============================================================
# FILE, DATE, PDF AND REPORT HELPERS
# ============================================================

def output_root():
    downloads = Path.home() / "Downloads"
    root = (downloads if downloads.exists() else Path.cwd()) / "High_Court_Judgments"
    root.mkdir(parents=True, exist_ok=True)
    return root


def clean_filename(text, max_len=55):
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", text or "")
    text = re.sub(r"\s+", "_", text).strip(" ._")
    return (text or "Judgment")[:max_len].rstrip(" ._")


def normalize_date_for_folder(value):
    return clean_filename((value or "Selected_Date").replace("/", "-"), 40)


def make_download_folder(court, from_date, to_date):
    date_part = normalize_date_for_folder(from_date)
    if from_date != to_date:
        date_part += "_to_" + normalize_date_for_folder(to_date)
    folder = output_root() / court["folder"] / date_part
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def selected_date_text(from_date, to_date):
    return from_date if from_date == to_date else f"{from_date} to {to_date}"


def get_search_dates(page):
    values = []
    for selector in ('input[type="text"]', 'input[type="date"]'):
        try:
            inputs = page.locator(selector)
            for index in range(inputs.count()):
                try:
                    value = inputs.nth(index).input_value().strip()
                    if re.fullmatch(r"\d{1,2}[/-]\d{1,2}[/-]\d{4}", value):
                        values.append(value.replace("/", "-"))
                    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                        yyyy, mm, dd = value.split("-")
                        values.append(f"{dd}-{mm}-{yyyy}")
                except Exception:
                    pass
        except Exception:
            pass
    values = list(dict.fromkeys(values))
    if len(values) >= 2:
        return values[0], values[1]
    if values:
        return values[0], values[0]
    return "Selected_Date", "Selected_Date"


def canonical_url(url):
    """Normalize only URL parts that do not change the requested document."""
    from urllib.parse import urldefrag
    return urldefrag((url or "").strip())[0]


def valid_pdf_file(path):
    try:
        if not path.is_file() or path.stat().st_size <= MIN_VALID_PDF_BYTES:
            return False
        with path.open("rb") as handle:
            if handle.read(5) != b"%PDF-":
                return False
            handle.seek(max(0, path.stat().st_size - 2048))
            return b"%%EOF" in handle.read()
    except OSError:
        return False


def pdf_page_count(path):
    if MIN_PDF_PAGES <= 1:
        return ""
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError(
            "PyMuPDF is required when MIN_PDF_PAGES is greater than 1."
        ) from exc
    with fitz.open(path) as document:
        if not document.is_pdf or document.needs_pass:
            raise ValueError("PDF is invalid, encrypted, or cannot be read")
        return document.page_count


def safe_unlink(path):
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass


def new_stats(court):
    return {
        "court": court["name"], "pages": 0, "rows": 0, "judgments": 0,
        "links": 0, "downloaded": 0, "existing": 0, "duplicates": 0,
        "short": 0, "failed": 0, "unique": 0, "folder": "", "error": "",
    }


def write_reports(folder, court, from_date, to_date, stats, log_rows):
    log_path = folder / "Download_Log.csv"
    with log_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_FIELDS)
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in LOG_FIELDS} for row in log_rows)

    lines = [
        "=" * 78, "HIGH COURT JUDGMENT DOWNLOAD REPORT", "=" * 78,
        f"Court                    : {court['name']}",
        f"Selected From Date       : {from_date}",
        f"Selected To Date         : {to_date}",
        f"Pages Processed          : {stats['pages']}",
        f"Website Rows Checked     : {stats['rows']}",
        f"Judgment Rows Found      : {stats['judgments']}",
        f"Judgment PDF Links Found : {stats['links']}",
        f"Downloaded Successfully  : {stats['downloaded']}",
        f"Already Downloaded       : {stats['existing']}",
        f"Duplicate URLs Skipped   : {stats['duplicates']}",
        f"Short PDFs Skipped       : {stats['short']}",
        f"Failed                   : {stats['failed']}",
        f"Unique PDFs Available    : {stats['unique']}",
        f"Output Folder            : {folder}", "=" * 78,
    ]
    report_path = folder / "Download_Report.txt"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path, log_path


def save_debug_artifacts(session, from_date, exc):
    date_part = normalize_date_for_folder(from_date)
    folder = Path.cwd() / "errors" / session["court"]["folder"] / date_part
    folder.mkdir(parents=True, exist_ok=True)
    page = session.get("page")
    try:
        page.screenshot(path=str(folder / "screenshot.png"), full_page=True)
    except Exception:
        pass
    try:
        (folder / "page_source.html").write_text(page.content(), encoding="utf-8")
    except Exception:
        pass
    (folder / "error.txt").write_text(
        f"{datetime.now().isoformat()}\n{type(exc).__name__}: {exc}\n",
        encoding="utf-8",
    )
    return folder


# ============================================================
# BROWSER AND SESSION PREPARATION
# ============================================================

def launch_browser(playwright):
    attempts = [
        ("Google Chrome", {"channel": "chrome", "headless": False}),
        ("Microsoft Edge", {"channel": "msedge", "headless": False}),
        ("Playwright Chromium", {"headless": False}),
    ]
    errors = []
    for label, options in attempts:
        try:
            print(f"Trying browser: {label}...")
            browser = playwright.chromium.launch(**options)
            print(f"Browser opened: {label}")
            return browser
        except Exception as exc:
            errors.append(f"{label}: {exc}")
    raise RuntimeError("No usable browser found. " + " | ".join(errors))


def open_court_session(browser, court):
    # Every court gets an isolated cookie jar and API request context.
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    try:
        page.goto(court["url"], wait_until="domcontentloaded", timeout=60_000)
    except Exception:
        context.close()
        raise
    return {"court": court, "context": context, "page": page}


def print_manual_instructions(sessions):
    print("\n" + "=" * 78)
    print("ALL SELECTED COURT PAGES ARE OPEN IN ISOLATED SESSIONS")
    print("=" * 78)
    for number, session in enumerate(sessions, 1):
        print(f"{number}. {session['court']['name']}")
    print("\nIn EACH browser window/page:")
    print("  1. Enter FROM DATE and TO DATE.")
    print("  2. Enter the CAPTCHA/security code manually (if shown).")
    print("  3. Select any bench/type required by that special court.")
    print("  4. Click GO/SUBMIT/Search and wait until results are visible.")
    print("\nReturn here only after ALL selected pages show their results.")


# ============================================================
# RESULT DETECTION (existing court structures retained)
# ============================================================

def is_judgment(text):
    text = re.sub(r"\s+", " ", (text or "").lower()).strip()
    return any(term in text for term in (
        "copy of judgement", "copy of judgment", "judgement", "judgment"
    ))


def is_ecourts_judgment_link(link, cell_text, link_count):
    try:
        metadata = " ".join((
            link.inner_text() or "", link.get_attribute("title") or "",
            link.get_attribute("aria-label") or "", link.get_attribute("href") or "",
            link.get_attribute("onclick") or "",
        ))
        return is_judgment(metadata) or (link_count == 1 and is_judgment(cell_text))
    except Exception:
        return False


def get_ecourts_records(page):
    records, row_count, judgment_rows = [], 0, 0
    rows = page.locator("table tbody tr")
    for row_index in range(rows.count()):
        try:
            cells = rows.nth(row_index).locator("td")
            if cells.count() < 4:
                continue
            match = re.search(r"\d+", cells.nth(0).inner_text().strip())
            if not match:
                continue
            row_count += 1
            serial = int(match.group())
            case_number = re.sub(r"\s+", " ", cells.nth(1).inner_text().strip()) or f"Case_{serial}"
            order_date = re.sub(r"\s+", " ", cells.nth(2).inner_text().strip())
            document_cell = cells.nth(3)
            cell_text = re.sub(r"\s+", " ", document_cell.inner_text().strip())
            links = document_cell.locator("a[href]")
            matched = 0
            for link_index in range(links.count()):
                link = links.nth(link_index)
                if not is_ecourts_judgment_link(link, cell_text, links.count()):
                    continue
                matched += 1
                href = (link.get_attribute("href") or "").strip()
                records.append({
                    "serial": serial, "case_number": case_number, "date": order_date,
                    "href": href, "url": urljoin(page.url, href) if href else "",
                    "row_index": row_index, "link_index": link_index,
                    "link_selector": "td:nth-child(4) a[href]",
                    "document_index": matched,
                })
            judgment_rows += bool(matched)
        except Exception as exc:
            print(f"Row {row_index + 1} could not be read: {exc}")
    return records, row_count, judgment_rows


def get_delhi_records(page):
    records, row_count, judgment_rows = [], 0, 0
    rows = page.locator("table tbody tr")
    for row_index in range(rows.count()):
        cells = rows.nth(row_index).locator("td")
        if cells.count() < 2:
            continue
        row_count += 1
        match = re.search(r"\d+", cells.nth(0).inner_text().strip())
        serial = int(match.group()) if match else row_index + 1
        case_number = re.sub(r"\s+", " ", cells.nth(1).inner_text().strip()) or f"Judgment_{serial}"
        links = rows.nth(row_index).locator('a[href*="showFileJudgment"]')
        matched = 0
        for link_index in range(links.count()):
            href = (links.nth(link_index).get_attribute("href") or "").strip()
            if not href:
                continue
            matched += 1
            records.append({"serial": serial, "case_number": case_number, "date": "",
                            "href": href, "url": urljoin(page.url, href),
                            "row_index": row_index, "link_index": link_index,
                            "link_selector": 'a[href*="showFileJudgment"]',
                            "document_index": matched})
        judgment_rows += bool(matched)
    return records, row_count, judgment_rows


def generic_link_is_judgment(link, row_text=""):
    try:
        combined = " ".join((link.get_attribute(name) or "") for name in
                            ("href", "title", "aria-label", "onclick"))
        combined += " " + (link.inner_text() or "")
        low = combined.lower()
        strong = ("showfilejudgment", "showjudgment", "showjudgement", "viewjudgment",
                  "viewjudgement", "judgmentpdf", "judgementpdf", "viewojpdf",
                  "webshowjudgment", "downloadjudgment", "downloadjudgement")
        if any(token in low for token in strong):
            return True
        # A plain PDF is eligible only when its own label or its result row says judgment.
        return ".pdf" in low and (is_judgment(combined) or is_judgment(row_text))
    except Exception:
        return False


def get_generic_records(page):
    records, row_count, judgment_rows = [], 0, 0
    rows = page.locator("table tbody tr")
    for row_index in range(rows.count()):
        try:
            row = rows.nth(row_index)
            cells, row_text = row.locator("td"), re.sub(r"\s+", " ", row.inner_text().strip())
            if not row_text or cells.count() == 0:
                continue
            row_count += 1
            match = re.search(r"\d+", cells.nth(0).inner_text().strip())
            serial = int(match.group()) if match else row_count
            case_number = (re.sub(r"\s+", " ", cells.nth(1).inner_text().strip())
                           if cells.count() > 1 else row_text) or f"Judgment_{serial}"
            links, matched = row.locator("a[href]"), 0
            for link_index in range(links.count()):
                link = links.nth(link_index)
                if not generic_link_is_judgment(link, row_text):
                    continue
                matched += 1
                href = (link.get_attribute("href") or "").strip()
                records.append({"serial": serial, "case_number": case_number, "date": "",
                                "href": href, "url": urljoin(page.url, href) if href else "",
                                "row_index": row_index, "link_index": link_index,
                                "link_selector": "a[href]",
                                "document_index": matched})
            judgment_rows += bool(matched)
        except Exception:
            continue
    if records:
        return records, row_count, judgment_rows
    # Non-table official result lists used by some special courts.
    links = page.locator("a[href]")
    for link_index in range(links.count()):
        link = links.nth(link_index)
        if not generic_link_is_judgment(link):
            continue
        href = (link.get_attribute("href") or "").strip()
        label = re.sub(r"\s+", " ", (link.inner_text() or "").strip())
        low = f"{href} {label}".lower()
        if any(token in low for token in ("annualreport", "newsletter", "rules.pdf", "calendar.pdf")):
            continue
        serial = len(records) + 1
        records.append({"serial": serial, "case_number": label or f"Judgment_{serial}",
                        "date": "", "href": href, "url": urljoin(page.url, href),
                        "global_link_index": link_index, "document_index": 1})
    return records, len(records), len(records)


def get_himachal_records(page):
    # Himachal's special result page exposes viewOJPDF links, often outside tables.
    return get_generic_records(page)


def read_records(engine, page):
    readers = {"ecourts": get_ecourts_records, "delhi": get_delhi_records,
               "generic": get_generic_records, "himachal": get_himachal_records}
    if engine not in readers:
        raise ValueError(f"No result reader for engine: {engine}")
    return readers[engine](page)


def page_signature(records):
    return tuple((canonical_url(item.get("url")), item.get("serial"),
                  item.get("case_number")) for item in records[:20])


# ============================================================
# DOWNLOAD AND PAGINATION
# ============================================================

def direct_download(context, url, filepath, referer):
    last_error = ""
    temp_path = filepath.with_suffix(filepath.suffix + ".part")
    safe_unlink(temp_path)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = context.request.get(url, headers={"Referer": referer,
                "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.8"},
                timeout=60_000)
            if not response.ok:
                raise RuntimeError(f"HTTP {response.status}")
            body = response.body()
            if len(body) <= MIN_VALID_PDF_BYTES or body[:5] != b"%PDF-":
                content_type = response.headers.get("content-type", "unknown")
                raise ValueError(f"response is not a valid PDF ({content_type}, {len(body)} bytes)")
            temp_path.write_bytes(body)
            if not valid_pdf_file(temp_path):
                raise ValueError("saved file failed PDF signature/size validation")
            temp_path.replace(filepath)
            return True, ""
        except Exception as exc:
            last_error = f"Attempt {attempt}/{MAX_RETRIES}: {exc}"
            safe_unlink(temp_path)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAYS[min(attempt - 1, len(RETRY_DELAYS) - 1)])
    return False, last_error


def locate_link(page, item):
    try:
        if "global_link_index" in item:
            return page.locator("a[href]").nth(item["global_link_index"])
        selector = item.get("link_selector", "a[href]")
        return page.locator("table tbody tr").nth(item["row_index"]).locator(selector).nth(item["link_index"])
    except Exception:
        return None


def browser_download_fallback(page, item, filepath):
    link = locate_link(page, item)
    if link is None:
        return False, "could not relocate result link"
    try:
        with page.expect_download(timeout=12_000) as info:
            link.click()
        info.value.save_as(str(filepath))
        if valid_pdf_file(filepath):
            return True, ""
        safe_unlink(filepath)
        return False, "browser download was not a valid PDF"
    except Exception as download_error:
        try:
            old_pages = set(page.context.pages)
            link.click()
            page.wait_for_timeout(800)
            popups = [candidate for candidate in page.context.pages if candidate not in old_pages]
            if popups:
                popup = popups[-1]
                result = direct_download(page.context, popup.url, filepath, page.url)
                popup.close()
                return result
        except Exception as popup_error:
            return False, f"download event: {download_error}; popup: {popup_error}"
        return False, f"browser download failed: {download_error}"


def download_item(page, context, item, filepath):
    url = canonical_url(item.get("url"))
    if url and item.get("href") not in ("#", "") and not item.get("href", "").lower().startswith("javascript:"):
        success, error = direct_download(context, url, filepath, page.url)
        if success:
            return True, error
        print(f"    Direct request failed ({error}); trying browser click...")
    return browser_download_fallback(page, item, filepath)


def next_control(page):
    selectors = ('a:has-text("Next")', 'button:has-text("Next")',
                 'a[title*="Next" i]', 'a[aria-label*="Next" i]')
    for selector in selectors:
        try:
            candidates = page.locator(selector)
            for index in range(candidates.count() - 1, -1, -1):
                candidate = candidates.nth(index)
                if candidate.is_visible():
                    return candidate
        except Exception:
            pass
    return None


def control_disabled(control):
    try:
        own = (control.get_attribute("class") or "").lower()
        aria = (control.get_attribute("aria-disabled") or "").lower()
        disabled = control.get_attribute("disabled") is not None
        parent = (control.locator("xpath=..").get_attribute("class") or "").lower()
        return disabled or aria == "true" or "disabled" in own or "disabled" in parent
    except Exception:
        return False


def go_next_page(page, engine, old_signature):
    control = next_control(page)
    if control is None or control_disabled(control):
        print("Next is missing or disabled. Pagination complete.")
        return False
    try:
        control.click()
        try:
            page.wait_for_load_state("domcontentloaded", timeout=RESULT_WAIT_MS)
        except Exception:
            pass
        deadline = time.monotonic() + RESULT_WAIT_MS / 1000
        while time.monotonic() < deadline:
            records, _, _ = read_records(engine, page)
            signature = page_signature(records)
            if signature and signature != old_signature:
                return True
            page.wait_for_timeout(300)
        print("Next page was empty or contained the same records. Stopping.")
        return False
    except Exception as exc:
        print(f"Next page failed: {exc}")
        return False


def make_filename(item):
    case = clean_filename(item["case_number"], 45)
    suffix = f"_J{item['document_index']}" if item.get("document_index", 1) > 1 else ""
    return f"{item['serial']:03d}_{case}{suffix}_Judgment.pdf"


def log_entry(court, dates, page_number, item, filename, page_count, status, error):
    return {
        "Court": court["name"], "Selected From Date": dates[0],
        "Selected To Date": dates[1], "Result Page": page_number,
        "Court Serial Number": item["serial"], "Case Number": item["case_number"],
        "Order/Judgment Date": item.get("date", ""), "PDF URL": item.get("url", ""),
        "File Name": filename, "Page Count": page_count, "Status": status,
        "Error Message": error,
    }


def process_session(session, completed_urls):
    court, context, page = session["court"], session["context"], session["page"]
    stats, logs = new_stats(court), []
    dates = get_search_dates(page)
    folder = make_download_folder(court, *dates)
    stats["folder"] = str(folder)
    seen_pages = set()
    page_number = 1

    print("\n" + "=" * 78)
    print(f"PROCESSING {court['name'].upper()}")
    print(f"Selected dates: {selected_date_text(*dates)}")
    print(f"Output: {folder}")
    print("=" * 78)

    while page_number <= MAX_RESULT_PAGES:
        records, row_count, judgment_rows = read_records(court["engine"], page)
        signature = page_signature(records)
        if not records or not signature:
            if page_number == 1:
                raise RuntimeError("No judgment result links detected after manual submission")
            break
        if signature in seen_pages:
            print("Repeated result-page signature detected. Stopping safely.")
            break
        seen_pages.add(signature)
        stats["pages"] += 1
        stats["rows"] += row_count
        stats["judgments"] += judgment_rows
        stats["links"] += len(records)
        print(f"Page {page_number}: {row_count} rows, {len(records)} judgment PDF link(s)")

        for item in records:
            filename = make_filename(item)
            filepath = folder / filename
            url_key = canonical_url(item.get("url"))
            page_count, error = "", ""
            if valid_pdf_file(filepath):
                try:
                    page_count = pdf_page_count(filepath)
                    if page_count != "" and page_count < MIN_PDF_PAGES:
                        safe_unlink(filepath)
                        status = SKIPPED_SHORT_PDF
                        stats["short"] += 1
                    else:
                        status = ALREADY_DOWNLOADED
                        stats["existing"] += 1
                except Exception as exc:
                    safe_unlink(filepath)
                    status, error = FAILED, f"Existing PDF page validation: {exc}"
                    stats["failed"] += 1
            elif url_key and url_key in completed_urls:
                status = DUPLICATE_SKIPPED
                stats["duplicates"] += 1
            else:
                safe_unlink(filepath)  # Remove stale/partial/corrupt existing output.
                success, error = download_item(page, context, item, filepath)
                if not success:
                    status = FAILED
                    stats["failed"] += 1
                else:
                    try:
                        page_count = pdf_page_count(filepath)
                        if page_count != "" and page_count < MIN_PDF_PAGES:
                            safe_unlink(filepath)
                            status = SKIPPED_SHORT_PDF
                            stats["short"] += 1
                        else:
                            status = DOWNLOADED
                            stats["downloaded"] += 1
                            if url_key:
                                completed_urls.add(url_key)
                    except Exception as exc:
                        safe_unlink(filepath)
                        status, error = FAILED, f"PDF page validation: {exc}"
                        stats["failed"] += 1
                time.sleep(DOWNLOAD_DELAY)
            logs.append(log_entry(court, dates, page_number, item, filename,
                                  page_count, status, error))
            print(f"  {item['serial']:03d} {status}: {filename}")

        if not go_next_page(page, court["engine"], signature):
            break
        page_number += 1

    stats["unique"] = stats["downloaded"] + stats["existing"]
    write_reports(folder, court, *dates, stats, logs)
    return stats


# ============================================================
# MENU, ERROR ISOLATION AND BATCH SUMMARY
# ============================================================

def show_menu():
    print("\n" + "=" * 78)
    print(APP_TITLE.center(78))
    print("=" * 78)
    for key, court in COURTS.items():
        print(f"{key:>2}. {court['name']}")
    print(" 0. Exit")
    print("=" * 78)


def parse_selection(value):
    tokens = [token for token in re.split(r"[ ,]+", value.strip()) if token]
    if tokens == ["0"]:
        return []
    if not 1 <= len(tokens) <= 6:
        raise ValueError("Select between 1 and 6 court numbers")
    if len(set(tokens)) != len(tokens):
        raise ValueError("Select each court only once")
    unknown = [token for token in tokens if token not in COURTS]
    if unknown:
        raise ValueError("Unknown court number(s): " + ", ".join(unknown))
    return [COURTS[token] for token in tokens]


def print_batch_summary(results):
    print("\n# " + "=" * 60 + " BATCH SUMMARY")
    print(f"Date: {datetime.now():%d-%m-%Y}")
    print(f"Selected Courts: {len(results)}\n")
    for number, stats in enumerate(results, 1):
        print(f"{number}. {stats['court']}")
        if stats["error"]:
            print(f"   ERROR: {stats['error']}")
        print(f"   Judgments: {stats['links']}")
        print(f"   Downloaded: {stats['downloaded']}")
        print(f"   Existing: {stats['existing']}")
        print(f"   Duplicates: {stats['duplicates']}")
        print(f"   Short PDFs: {stats['short']}")
        print(f"   Failed: {stats['failed']}")
    print("\nTOTAL")
    print(f"Courts processed: {len(results)}")
    for label, key in (("Judgments found", "links"), ("Downloaded", "downloaded"),
                       ("Existing", "existing"), ("Duplicates", "duplicates"),
                       ("Short PDFs", "short"), ("Failed", "failed")):
        print(f"{label}: {sum(item[key] for item in results)}")


def run_batch(browser, courts):
    sessions, results, completed_urls = [], [], set()
    # Open everything first. Failure to open one court does not discard the others.
    for court in courts:
        try:
            print(f"Opening isolated session: {court['name']}")
            sessions.append(open_court_session(browser, court))
        except Exception as exc:
            stats = new_stats(court)
            stats["error"], stats["failed"] = str(exc), 1
            results.append(stats)
            print(f"Could not open {court['name']}: {exc}")
    if sessions:
        print_manual_instructions(sessions)
        input("\nAfter ALL result tables/lists are visible, press ENTER ONCE... ")
    for session in sessions:
        court = session["court"]
        try:
            results.append(process_session(session, completed_urls))
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            dates = get_search_dates(session["page"])
            debug_folder = save_debug_artifacts(session, dates[0], exc)
            stats = new_stats(court)
            stats["error"], stats["failed"] = str(exc), 1
            folder = make_download_folder(court, *dates)
            stats["folder"] = str(folder)
            write_reports(folder, court, *dates, stats, [])
            results.append(stats)
            print(f"ERROR in {court['name']}: {exc}")
            print(f"Debug files saved to: {debug_folder}")
        finally:
            try:
                session["context"].close()
            except Exception:
                pass
    print_batch_summary(results)


def main():
    print(f"\n{APP_TITLE}")
    print(f"Downloads will be saved under:\n{output_root()}")
    print("CAPTCHA remains entirely manual; this program never solves or bypasses it.")
    with sync_playwright() as playwright:
        browser = launch_browser(playwright)
        try:
            while True:
                show_menu()
                try:
                    courts = parse_selection(input("Select 1-6 court numbers (comma/space separated), or 0: "))
                except ValueError as exc:
                    print(f"Invalid selection: {exc}")
                    continue
                if not courts:
                    break
                try:
                    run_batch(browser, courts)
                except KeyboardInterrupt:
                    print("\nBatch cancelled; open contexts will close with the browser.")
                if input("\nReturn to court menu? (Y/N): ").strip().lower() not in ("", "y", "yes"):
                    break
        finally:
            browser.close()
    print("\nFinished.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nFatal error: {exc}")
        input("\nPress ENTER to close...")
