from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from pathlib import Path
from datetime import datetime
import csv
import os
import re
import sys
import time


APP_TITLE = "HIGH COURT JUDGMENT DOWNLOADER - V4"
BASE_ECOURTS = "https://hcservices.ecourts.gov.in"
DOWNLOAD_DELAY = 0.5
MAX_RETRIES = 3


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
# FILE / PATH HELPERS
# ============================================================

def output_root():
    downloads = Path.home() / "Downloads"

    if downloads.exists():
        root = downloads / "High_Court_Judgments"
    else:
        root = Path.cwd() / "High_Court_Judgments"

    root.mkdir(parents=True, exist_ok=True)
    return root


def clean_filename(text, max_len=90):
    text = re.sub(r'[<>:"/\\|?*]', "_", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    text = text.rstrip(". ")

    if not text:
        text = "Judgment"

    return text[:max_len]


def normalize_date_for_folder(value):
    value = (value or "Selected_Date").strip()
    value = value.replace("/", "-").replace("\\", "-")
    value = clean_filename(value, max_len=40)
    return value


def make_download_folder(court, from_date, to_date):
    if from_date == to_date:
        date_part = normalize_date_for_folder(from_date)
    else:
        date_part = (
            f"{normalize_date_for_folder(from_date)}"
            f"_to_{normalize_date_for_folder(to_date)}"
        )

    folder = output_root() / court["folder"] / date_part
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def selected_date_text(from_date, to_date):
    if from_date == to_date:
        return from_date
    return f"{from_date} to {to_date}"


def print_selected_dates(from_date, to_date):
    print()
    print("=" * 78)
    print("SELECTED DOWNLOAD DATE")
    print("=" * 78)
    print(f"From Date          : {from_date}")
    print(f"To Date            : {to_date}")
    print(
        f"Downloading Data   : "
        f"{selected_date_text(from_date, to_date)}"
    )
    print("=" * 78)


def write_download_log(folder, rows):
    log_path = folder / "Download_Log.csv"

    fieldnames = [
        "Court",
        "Selected From Date",
        "Selected To Date",
        "Page",
        "Court Serial",
        "Case Number",
        "File Name",
        "Status",
    ]

    with open(
        log_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )
        writer.writeheader()

        for row in rows:
            writer.writerow({
                key: row.get(key, "")
                for key in fieldnames
            })

    return log_path


def write_run_report(
    folder,
    court_name,
    from_date,
    to_date,
    pages,
    rows_checked,
    judgments_found,
    downloaded,
    existing,
    failed,
    log_rows,
):
    report_path = folder / "Download_Report.txt"
    log_path = write_download_log(
        folder,
        log_rows
    )

    now = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    lines = [
        "=" * 78,
        "HIGH COURT JUDGMENT DOWNLOAD REPORT",
        "=" * 78,
        f"Court              : {court_name}",
        f"Selected From Date : {from_date}",
        f"Selected To Date   : {to_date}",
        (
            "Downloaded Date(s) : "
            f"{selected_date_text(from_date, to_date)}"
        ),
        f"Run Completed At   : {now}",
        "",
        f"Pages Processed    : {pages}",
        f"Rows Checked       : {rows_checked}",
        f"Judgments Found    : {judgments_found}",
        f"Downloaded Now     : {downloaded}",
        f"Already Existing   : {existing}",
        f"Failed             : {failed}",
        (
            "PDFs Available     : "
            f"{downloaded + existing}"
        ),
        "",
        f"Download Folder    : {folder}",
        f"CSV Download Log   : {log_path.name}",
        "=" * 78,
    ]

    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    master_history = output_root() / "Master_Download_History.csv"
    history_exists = master_history.exists()

    with open(
        master_history,
        "a",
        newline="",
        encoding="utf-8-sig"
    ) as history_file:
        fieldnames = [
            "Run Completed At",
            "Court",
            "Selected From Date",
            "Selected To Date",
            "Pages Processed",
            "Rows Checked",
            "Judgments Found",
            "Downloaded Now",
            "Already Existing",
            "Failed",
            "PDFs Available",
            "Folder",
        ]

        writer = csv.DictWriter(
            history_file,
            fieldnames=fieldnames
        )

        if not history_exists:
            writer.writeheader()

        writer.writerow({
            "Run Completed At": now,
            "Court": court_name,
            "Selected From Date": from_date,
            "Selected To Date": to_date,
            "Pages Processed": pages,
            "Rows Checked": rows_checked,
            "Judgments Found": judgments_found,
            "Downloaded Now": downloaded,
            "Already Existing": existing,
            "Failed": failed,
            "PDFs Available": downloaded + existing,
            "Folder": str(folder),
        })

    return report_path, log_path


# ============================================================
# BROWSER
# ============================================================

def launch_browser(playwright):
    """
    Prefer installed Chrome to keep the EXE small.
    Fall back to Edge, then Playwright Chromium if available.
    """
    launch_attempts = [
        ("Google Chrome", {"channel": "chrome", "headless": False}),
        ("Microsoft Edge", {"channel": "msedge", "headless": False}),
        ("Playwright Chromium", {"headless": False}),
    ]

    errors = []

    for label, kwargs in launch_attempts:
        try:
            print(f"Trying browser: {label}...")
            browser = playwright.chromium.launch(**kwargs)
            print(f"Browser opened: {label}")
            return browser
        except Exception as exc:
            errors.append(f"{label}: {exc}")

    print()
    print("=" * 78)
    print("NO SUPPORTED BROWSER COULD BE OPENED")
    print("=" * 78)
    print("Install Google Chrome or Microsoft Edge.")
    print()
    print("Details:")
    for error in errors:
        print(" -", error)
    raise RuntimeError("No usable Chrome/Edge/Chromium browser found.")


# ============================================================
# DATE DETECTION
# ============================================================

def get_search_dates(page):
    date_values = []

    selectors = [
        'input[type="text"]',
        'input[type="date"]',
    ]

    for selector in selectors:
        try:
            inputs = page.locator(selector)

            for i in range(inputs.count()):
                try:
                    value = inputs.nth(i).input_value().strip()

                    if re.fullmatch(
                        r"\d{1,2}[/-]\d{1,2}[/-]\d{4}",
                        value
                    ):
                        date_values.append(value)

                    elif re.fullmatch(
                        r"\d{4}-\d{2}-\d{2}",
                        value
                    ):
                        yyyy, mm, dd = value.split("-")
                        date_values.append(f"{dd}-{mm}-{yyyy}")

                except Exception:
                    pass
        except Exception:
            pass

    # Preserve order while removing exact repeats.
    cleaned = []
    for value in date_values:
        if value not in cleaned:
            cleaned.append(value)

    if len(cleaned) >= 2:
        return cleaned[0], cleaned[1]

    if len(cleaned) == 1:
        return cleaned[0], cleaned[0]

    return "Selected_Date", "Selected_Date"


def resolve_search_dates(page):
    from_date, to_date = get_search_dates(page)

    if from_date != "Selected_Date":
        return from_date, to_date

    print()
    print("The website uses date controls that could not be read automatically.")
    print("Enter the SAME dates you selected in the browser so the folder/report is correct.")

    from_date = input("Selected FROM DATE (DD-MM-YYYY): ").strip() or "Selected_Date"
    to_date = input("Selected TO DATE   (press ENTER if same): ").strip() or from_date

    return from_date, to_date


# ============================================================
# DOWNLOAD HELPERS
# ============================================================

def direct_download(context, url, filepath, referer):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"    Attempt {attempt}/{MAX_RETRIES}")

            response = context.request.get(
                url,
                headers={
                    "Referer": referer,
                    "Accept": (
                        "application/pdf,"
                        "application/octet-stream;q=0.9,"
                        "*/*;q=0.8"
                    ),
                },
                timeout=60000,
            )

            print(f"    HTTP: {response.status}")

            if not response.ok:
                page_wait_seconds(1.5)
                continue

            content = response.body()
            print(f"    Received: {len(content):,} bytes")

            if b"%PDF" not in content[:4096]:
                content_type = response.headers.get("content-type", "")
                print(f"    Not a PDF response. Type: {content_type}")
                page_wait_seconds(1.5)
                continue

            with open(filepath, "wb") as file:
                file.write(content)

            if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
                return True

        except Exception as exc:
            print(f"    Direct download error: {exc}")

        page_wait_seconds(1.5)

    return False


def page_wait_seconds(seconds):
    # Kept tiny and outside active page interactions.
    time.sleep(seconds)


# ============================================================
# ECOURTS ENGINE
# ============================================================

def is_judgment(text):
    text = (text or "").lower().strip()

    terms = [
        "copy of judgement",
        "copy of judgment",
        "judgement",
        "judgment",
    ]

    return any(term in text for term in terms)


def is_ecourts_judgment_link(link, order_cell_text, total_links):
    """
    Use link-specific metadata first.

    We intentionally do NOT mark every link in a cell as a judgment just
    because the whole cell contains the word 'Judgement'. This avoids
    downloading 'Order on Exhibit' links in mixed rows.
    """
    try:
        link_text = (link.inner_text() or "").strip()
        title = (link.get_attribute("title") or "").strip()
        aria = (link.get_attribute("aria-label") or "").strip()
        href = (link.get_attribute("href") or "").strip()
        onclick = (link.get_attribute("onclick") or "").strip()

        specific = f"{link_text} {title} {aria} {href} {onclick}"

        if is_judgment(specific):
            return True

        # If there is exactly one link in the cell, the cell label can safely
        # identify that one link.
        if total_links == 1 and is_judgment(order_cell_text):
            return True

    except Exception:
        pass

    return False


def get_ecourts_records(page):
    records = []
    rows = page.locator("table tbody tr")

    html_rows = rows.count()
    actual_rows = 0

    print(f"HTML table rows detected: {html_rows}")

    for i in range(html_rows):
        row = rows.nth(i)

        try:
            cells = row.locator("td")

            if cells.count() < 4:
                continue

            serial_text = cells.nth(0).inner_text().strip()
            serial_match = re.search(r"\d+", serial_text)

            if not serial_match:
                continue

            serial = int(serial_match.group())
            actual_rows += 1

            case_number = re.sub(
                r"\s+",
                " ",
                cells.nth(1).inner_text().strip()
            )

            if not case_number:
                case_number = f"Case_{serial}"

            order_date = cells.nth(2).inner_text().strip()

            order_cell = cells.nth(3)
            order_cell_text = re.sub(
                r"\s+",
                " ",
                order_cell.inner_text().strip()
            )

            links = order_cell.locator("a[href]")
            total_links = links.count()
            judgment_index = 0

            print()
            print(f"Row {serial}")
            print(f"  Case : {case_number}")
            print(f"  Date : {order_date}")
            print(f"  Type : {order_cell_text}")

            for j in range(total_links):
                link = links.nth(j)

                if not is_ecourts_judgment_link(
                    link,
                    order_cell_text,
                    total_links
                ):
                    continue

                judgment_index += 1

                records.append({
                    "serial": serial,
                    "case_number": case_number,
                    "order_date": order_date,
                    "judgment_index": judgment_index,
                    "href": (link.get_attribute("href") or "").strip(),
                })

            if judgment_index:
                print(f"  ✓ Judgment link(s): {judgment_index}")
            else:
                print("  SKIP -> No judgment link")

        except Exception as exc:
            print(f"Row {i + 1} error: {exc}")

    return records, actual_rows


def find_ecourts_judgment_link(page, serial, judgment_number):
    rows = page.locator("table tbody tr")

    for i in range(rows.count()):
        row = rows.nth(i)
        cells = row.locator("td")

        if cells.count() < 4:
            continue

        serial_text = cells.nth(0).inner_text().strip()
        serial_match = re.search(r"\d+", serial_text)

        if not serial_match:
            continue

        if int(serial_match.group()) != serial:
            continue

        order_cell = cells.nth(3)
        order_cell_text = order_cell.inner_text().strip()
        links = order_cell.locator("a[href]")
        total_links = links.count()

        current = 0

        for j in range(total_links):
            link = links.nth(j)

            if is_ecourts_judgment_link(
                link,
                order_cell_text,
                total_links
            ):
                current += 1

                if current == judgment_number:
                    return link

    return None


def click_download_ecourts(page, item, filepath):
    link = find_ecourts_judgment_link(
        page,
        item["serial"],
        item["judgment_index"]
    )

    if link is None:
        print("    Could not relocate the judgment link.")
        return False

    # Normal download event.
    try:
        with page.expect_download(timeout=10000) as info:
            link.click()

        download = info.value
        download.save_as(str(filepath))

        return filepath.exists() and filepath.stat().st_size > 500

    except Exception:
        pass

    # Popup / new tab.
    try:
        old_pages = set(page.context.pages)

        link.click()
        page.wait_for_timeout(2000)

        new_pages = [
            item_page
            for item_page in page.context.pages
            if item_page not in old_pages
        ]

        if new_pages:
            popup = new_pages[-1]
            popup.wait_for_timeout(1000)
            popup_url = popup.url

            print(f"    Popup URL: {popup_url}")

            success = False

            if popup_url:
                success = direct_download(
                    page.context,
                    popup_url,
                    filepath,
                    page.url
                )

            try:
                popup.close()
            except Exception:
                pass

            return success

    except Exception as exc:
        print(f"    Popup download error: {exc}")

    return False


def download_ecourts_item(page, context, item, filepath):
    href = (item["href"] or "").strip()

    if (
        href
        and href != "#"
        and not href.lower().startswith("javascript:")
    ):
        full_url = urljoin(page.url, href)
        print(f"    URL: {full_url}")

        if direct_download(
            context,
            full_url,
            filepath,
            page.url
        ):
            return True

    print("    Trying browser-click method...")

    return click_download_ecourts(
        page,
        item,
        filepath
    )


def first_result_serial(page):
    try:
        rows = page.locator("table tbody tr")

        for i in range(rows.count()):
            cells = rows.nth(i).locator("td")

            if cells.count() < 4:
                continue

            text = cells.nth(0).inner_text().strip()
            match = re.search(r"\d+", text)

            if match:
                return int(match.group())

    except Exception:
        pass

    return None


def ecourts_page_has_data(page):
    """
    True only when the current eCourts page has at least one real result row.
    """
    try:
        rows = page.locator("table tbody tr")

        for i in range(rows.count()):
            cells = rows.nth(i).locator("td")

            if cells.count() < 4:
                continue

            serial_text = (
                cells.nth(0)
                .inner_text()
                .strip()
            )

            if re.search(r"\d+", serial_text):
                return True

    except Exception:
        pass

    return False


def delhi_page_has_data(page):
    """
    True only when the Delhi result page contains at least one judgment PDF.
    """
    try:
        return (
            page.locator(
                'a[href*="showFileJudgment"]'
            ).count()
            > 0
        )
    except Exception:
        return False


def go_next_page(page, data_validator=None):
    selectors = [
        'a:has-text("Next")',
        'button:has-text("Next")',
        'a[title*="Next"]',
        'a[aria-label*="Next"]',
    ]

    next_button = None

    for selector in selectors:
        candidates = page.locator(selector)

        if candidates.count() > 0:
            next_button = candidates.last
            break

    if next_button is None:
        print("No Next page control found. Stopping.")
        return False

    try:
        own_class = (
            next_button.get_attribute("class")
            or ""
        ).lower()

        aria_disabled = (
            next_button.get_attribute(
                "aria-disabled"
            )
            or ""
        ).lower()

        parent_class = ""

        try:
            parent_class = (
                next_button
                .locator("xpath=..")
                .get_attribute("class")
                or ""
            ).lower()
        except Exception:
            pass

        if (
            "disabled" in own_class
            or "disabled" in parent_class
            or aria_disabled == "true"
        ):
            print("Next page is disabled. Stopping.")
            return False

    except Exception:
        pass

    old_serial = first_result_serial(page)
    old_url = page.url

    print()
    print("Next page control is available.")
    print("Opening next page and checking whether it contains data...")

    try:
        next_button.click()
        page.wait_for_timeout(1500)

        try:
            page.wait_for_load_state(
                "domcontentloaded",
                timeout=15000
            )
        except Exception:
            pass

        page_changed = False

        for _ in range(20):
            new_serial = first_result_serial(page)

            if (
                old_serial is not None
                and new_serial is not None
                and new_serial != old_serial
            ):
                page_changed = True
                break

            if page.url != old_url:
                page_changed = True
                break

            page.wait_for_timeout(300)

        if not page_changed:
            print(
                "Next page did not load a different result page. "
                "Stopping."
            )
            return False

        # Critical new check requested by the user:
        # a Next page must actually contain result data.
        if data_validator is not None:
            page.wait_for_timeout(500)

            if not data_validator(page):
                print()
                print(
                    "Next page opened, but NO RESULT DATA "
                    "was found on it."
                )
                print("Stopping pagination.")
                return False

        print("Next page contains result data.")
        return True

    except Exception as exc:
        print(f"Next page error: {exc}")
        return False


def process_ecourts(court, browser):
    context = browser.new_context(
        accept_downloads=True
    )
    page = context.new_page()

    print()
    print("=" * 78)
    print(court["name"].upper())
    print("=" * 78)
    print(
        "Opening official eCourts "
        "Order Date page..."
    )

    page.goto(
        court["url"],
        wait_until="domcontentloaded",
        timeout=60000
    )

    print()
    print("In the browser:")
    print("  1. Enter FROM DATE")
    print("  2. Enter TO DATE")
    print("  3. Enter CAPTCHA")
    print("  4. Click GO / SUBMIT")
    print("  5. Wait for the result table")
    print()

    input(
        "After results appear, "
        "press ENTER here... "
    )

    from_date, to_date = (
        resolve_search_dates(page)
    )

    print_selected_dates(
        from_date,
        to_date
    )

    folder = make_download_folder(
        court,
        from_date,
        to_date
    )

    print()
    print(f"Save folder: {folder}")

    page_number = 1
    rows_checked = 0
    judgments_found = 0
    downloaded = 0
    existing = 0
    failed = 0
    log_rows = []

    while True:
        print()
        print("-" * 78)
        print(f"RESULT PAGE {page_number}")
        print("-" * 78)

        records, page_rows = (
            get_ecourts_records(page)
        )

        # If somehow an empty page is reached, stop.
        if page_rows == 0:
            print(
                "No result rows found on this page. "
                "Stopping."
            )
            break

        rows_checked += page_rows
        judgments_found += len(records)

        print()
        print(
            f"Court rows on this page : "
            f"{page_rows}"
        )
        print(
            f"Judgments on this page  : "
            f"{len(records)}"
        )
        print(
            "Downloading THIS PAGE first..."
        )

        for item in records:
            serial = item["serial"]
            case_name = clean_filename(
                item["case_number"],
                max_len=90
            )

            if item["judgment_index"] > 1:
                filename = (
                    f"{serial:03d}_"
                    f"J{item['judgment_index']}_"
                    f"{case_name}_Judgment.pdf"
                )
            else:
                filename = (
                    f"{serial:03d}_"
                    f"{case_name}_Judgment.pdf"
                )

            filepath = folder / filename

            print()
            print(f"Court S.No. : {serial}")
            print(
                f"Case        : "
                f"{item['case_number']}"
            )
            print(f"File        : {filename}")

            status = ""

            if (
                filepath.exists()
                and filepath.stat().st_size > 500
            ):
                existing += 1
                status = "ALREADY DOWNLOADED"
                print(
                    "Status      : "
                    "ALREADY DOWNLOADED"
                )
            else:
                success = download_ecourts_item(
                    page,
                    context,
                    item,
                    filepath
                )

                if success:
                    downloaded += 1
                    status = "DOWNLOADED"
                    print(
                        "Status      : "
                        "✓ DOWNLOADED"
                    )
                else:
                    failed += 1
                    status = "FAILED"
                    print(
                        "Status      : "
                        "✗ FAILED"
                    )

                page.wait_for_timeout(
                    int(
                        DOWNLOAD_DELAY
                        * 1000
                    )
                )

            log_rows.append({
                "Court": court["name"],
                "Selected From Date": from_date,
                "Selected To Date": to_date,
                "Page": page_number,
                "Court Serial": serial,
                "Case Number": item["case_number"],
                "File Name": filename,
                "Status": status,
            })

        print()
        print(
            f"Page {page_number} completed."
        )
        print(
            "All available judgments on "
            "this page were handled first."
        )
        print(
            "Now checking whether the Next "
            "page exists AND contains data..."
        )

        if not go_next_page(
            page,
            ecourts_page_has_data
        ):
            break

        page_number += 1

        if page_number > 100:
            print(
                "Pagination safety "
                "limit reached."
            )
            break

    report_path, log_path = write_run_report(
        folder=folder,
        court_name=court["name"],
        from_date=from_date,
        to_date=to_date,
        pages=page_number,
        rows_checked=rows_checked,
        judgments_found=judgments_found,
        downloaded=downloaded,
        existing=existing,
        failed=failed,
        log_rows=log_rows,
    )

    print()
    print("=" * 78)
    print("FINAL REPORT")
    print("=" * 78)
    print(
        f"Court              : "
        f"{court['name']}"
    )
    print(
        f"Selected From Date : "
        f"{from_date}"
    )
    print(
        f"Selected To Date   : "
        f"{to_date}"
    )
    print(
        f"Downloaded Date(s) : "
        f"{selected_date_text(from_date, to_date)}"
    )
    print(
        f"Pages Processed    : "
        f"{page_number}"
    )
    print(
        f"Rows Checked       : "
        f"{rows_checked}"
    )
    print(
        f"Judgments Found    : "
        f"{judgments_found}"
    )
    print(
        f"Downloaded Now     : "
        f"{downloaded}"
    )
    print(
        f"Already Existing   : "
        f"{existing}"
    )
    print(
        f"Failed             : "
        f"{failed}"
    )
    print(
        f"PDFs Available     : "
        f"{downloaded + existing}"
    )
    print(
        f"Folder             : "
        f"{folder}"
    )
    print(
        f"Text Report        : "
        f"{report_path.name}"
    )
    print(
        f"CSV Log            : "
        f"{log_path.name}"
    )
    print("=" * 78)

    context.close()


# ============================================================
# DELHI ENGINE
# ============================================================

def get_delhi_records(page):
    records = []

    try:
        rows = page.locator("table tbody tr")
    except Exception:
        return records

    for i in range(rows.count()):
        row = rows.nth(i)
        cells = row.locator("td")

        if cells.count() < 2:
            continue

        serial = i + 1

        try:
            serial_text = cells.nth(0).inner_text().strip()
            match = re.search(r"\d+", serial_text)
            if match:
                serial = int(match.group())
        except Exception:
            pass

        case_number = f"Judgment_{serial}"

        try:
            case_number = re.sub(
                r"\s+",
                " ",
                cells.nth(1).inner_text().strip()
            ) or case_number
        except Exception:
            pass

        pdf_links = row.locator(
            'a[href*="showFileJudgment"]'
        )

        judgment_index = 0

        for j in range(pdf_links.count()):
            link = pdf_links.nth(j)
            href = (link.get_attribute("href") or "").strip()

            if not href:
                continue

            if ".pdf" not in href.lower():
                continue

            judgment_index += 1

            records.append({
                "serial": serial,
                "case_number": case_number,
                "judgment_index": judgment_index,
                "url": urljoin(page.url, href),
            })

    return records


def process_delhi(court, browser):
    context = browser.new_context(
        accept_downloads=True
    )
    page = context.new_page()

    print()
    print("=" * 78)
    print(court["name"].upper())
    print("=" * 78)

    page.goto(
        court["url"],
        wait_until="domcontentloaded",
        timeout=60000
    )

    print()
    print("In the browser:")
    print("  1. Enter FROM DATE")
    print("  2. Enter TO DATE")
    print("  3. Enter CAPTCHA")
    print("  4. Submit")
    print("  5. Wait for judgment results")
    print()

    input(
        "After results appear, "
        "press ENTER here... "
    )

    from_date, to_date = (
        resolve_search_dates(page)
    )

    print_selected_dates(
        from_date,
        to_date
    )

    folder = make_download_folder(
        court,
        from_date,
        to_date
    )

    downloaded = 0
    existing = 0
    failed = 0
    found = 0
    rows_checked = 0
    page_number = 1
    log_rows = []

    while True:
        records = get_delhi_records(page)

        if not records:
            print(
                "No judgment data found on "
                "this page. Stopping."
            )
            break

        found += len(records)
        rows_checked += len(records)

        print()
        print(
            f"Delhi result page "
            f"{page_number}"
        )
        print(
            f"PDF judgment links: "
            f"{len(records)}"
        )
        print(
            "Downloading THIS PAGE first..."
        )

        for item in records:
            case_name = clean_filename(
                item["case_number"],
                max_len=90
            )

            if item["judgment_index"] > 1:
                filename = (
                    f"{item['serial']:03d}_"
                    f"J{item['judgment_index']}_"
                    f"{case_name}.pdf"
                )
            else:
                filename = (
                    f"{item['serial']:03d}_"
                    f"{case_name}.pdf"
                )

            filepath = folder / filename
            status = ""

            if (
                filepath.exists()
                and filepath.stat().st_size > 500
            ):
                existing += 1
                status = "ALREADY DOWNLOADED"
                print(
                    f"Already downloaded: "
                    f"{filename}"
                )
            else:
                print(
                    f"Downloading: "
                    f"{filename}"
                )

                success = direct_download(
                    context,
                    item["url"],
                    filepath,
                    page.url
                )

                if success:
                    downloaded += 1
                    status = "DOWNLOADED"
                    print("    ✓ Downloaded")
                else:
                    failed += 1
                    status = "FAILED"
                    print("    ✗ Failed")

                page.wait_for_timeout(
                    int(
                        DOWNLOAD_DELAY
                        * 1000
                    )
                )

            log_rows.append({
                "Court": court["name"],
                "Selected From Date": from_date,
                "Selected To Date": to_date,
                "Page": page_number,
                "Court Serial": item["serial"],
                "Case Number": item["case_number"],
                "File Name": filename,
                "Status": status,
            })

        print(
            "Current page completed."
        )
        print(
            "Now checking whether the Next "
            "page exists AND contains data..."
        )

        if not go_next_page(
            page,
            delhi_page_has_data
        ):
            break

        page_number += 1

        if page_number > 100:
            print(
                "Pagination safety "
                "limit reached."
            )
            break

    report_path, log_path = write_run_report(
        folder=folder,
        court_name=court["name"],
        from_date=from_date,
        to_date=to_date,
        pages=page_number,
        rows_checked=rows_checked,
        judgments_found=found,
        downloaded=downloaded,
        existing=existing,
        failed=failed,
        log_rows=log_rows,
    )

    print()
    print("=" * 78)
    print("FINAL REPORT")
    print("=" * 78)
    print(
        f"Court              : "
        f"{court['name']}"
    )
    print(
        f"Selected From Date : "
        f"{from_date}"
    )
    print(
        f"Selected To Date   : "
        f"{to_date}"
    )
    print(
        f"Downloaded Date(s) : "
        f"{selected_date_text(from_date, to_date)}"
    )
    print(
        f"Pages Processed    : "
        f"{page_number}"
    )
    print(
        f"Judgment PDFs      : "
        f"{found}"
    )
    print(
        f"Downloaded Now     : "
        f"{downloaded}"
    )
    print(
        f"Already Existing   : "
        f"{existing}"
    )
    print(
        f"Failed             : "
        f"{failed}"
    )
    print(
        f"PDFs Available     : "
        f"{downloaded + existing}"
    )
    print(
        f"Folder             : "
        f"{folder}"
    )
    print(
        f"Text Report        : "
        f"{report_path.name}"
    )
    print(
        f"CSV Log            : "
        f"{log_path.name}"
    )
    print("=" * 78)

    context.close()


# ============================================================
# HIMACHAL ENGINE
# ============================================================

def get_himachal_pdf_links(page):
    records = []
    links = page.locator("a[href]")

    for i in range(links.count()):
        link = links.nth(i)

        try:
            href = (link.get_attribute("href") or "").strip()
            text = re.sub(
                r"\s+",
                " ",
                (link.inner_text() or "").strip()
            )
            title = (link.get_attribute("title") or "").strip()

            combined = f"{href} {text} {title}".lower()

            if (
                ".pdf" not in combined
                and "viewojpdf" not in combined
            ):
                continue

            full_url = urljoin(page.url, href)

            if "annualreport" in full_url.lower():
                continue

            records.append({
                "index": len(records) + 1,
                "label": text or title or f"Judgment_{len(records)+1}",
                "url": full_url,
            })

        except Exception:
            pass

    return records


def process_himachal(court, browser):
    context = browser.new_context(
        accept_downloads=True
    )
    page = context.new_page()

    print()
    print("=" * 78)
    print(court["name"].upper())
    print("=" * 78)

    page.goto(
        court["url"],
        wait_until="domcontentloaded",
        timeout=60000
    )

    print()
    print(
        "Himachal uses its own website."
    )
    print("In the browser:")
    print("  1. Open Order/Judgement")
    print("  2. Open Period Wise")
    print(
        "  3. Select FROM DATE "
        "and TO DATE"
    )
    print(
        "  4. Select JUDGMENT if "
        "the filter is shown"
    )
    print(
        "  5. Search and wait for results"
    )
    print()

    input(
        "After JUDGMENT results appear, "
        "press ENTER here... "
    )

    from_date, to_date = (
        resolve_search_dates(page)
    )

    print_selected_dates(
        from_date,
        to_date
    )

    folder = make_download_folder(
        court,
        from_date,
        to_date
    )

    records = get_himachal_pdf_links(
        page
    )

    downloaded = 0
    existing = 0
    failed = 0
    log_rows = []

    print(
        f"Judgment/PDF links found: "
        f"{len(records)}"
    )

    for item in records:
        label = clean_filename(
            item["label"],
            max_len=90
        )

        filename = (
            f"{item['index']:03d}_"
            f"{label}.pdf"
        )

        filename = re.sub(
            r"\.pdf\.pdf$",
            ".pdf",
            filename,
            flags=re.IGNORECASE
        )

        filepath = folder / filename
        status = ""

        if (
            filepath.exists()
            and filepath.stat().st_size > 500
        ):
            existing += 1
            status = "ALREADY DOWNLOADED"
            print(
                f"Already downloaded: "
                f"{filename}"
            )
        else:
            print(
                f"Downloading: "
                f"{filename}"
            )

            success = direct_download(
                context,
                item["url"],
                filepath,
                page.url
            )

            if success:
                downloaded += 1
                status = "DOWNLOADED"
                print("    ✓ Downloaded")
            else:
                failed += 1
                status = "FAILED"
                print("    ✗ Failed")

            page.wait_for_timeout(
                int(
                    DOWNLOAD_DELAY
                    * 1000
                )
            )

        log_rows.append({
            "Court": court["name"],
            "Selected From Date": from_date,
            "Selected To Date": to_date,
            "Page": 1,
            "Court Serial": item["index"],
            "Case Number": item["label"],
            "File Name": filename,
            "Status": status,
        })

    report_path, log_path = write_run_report(
        folder=folder,
        court_name=court["name"],
        from_date=from_date,
        to_date=to_date,
        pages=1,
        rows_checked=len(records),
        judgments_found=len(records),
        downloaded=downloaded,
        existing=existing,
        failed=failed,
        log_rows=log_rows,
    )

    print()
    print("=" * 78)
    print("FINAL REPORT")
    print("=" * 78)
    print(
        f"Court              : "
        f"{court['name']}"
    )
    print(
        f"Selected From Date : "
        f"{from_date}"
    )
    print(
        f"Selected To Date   : "
        f"{to_date}"
    )
    print(
        f"Downloaded Date(s) : "
        f"{selected_date_text(from_date, to_date)}"
    )
    print(
        f"PDF Links          : "
        f"{len(records)}"
    )
    print(
        f"Downloaded Now     : "
        f"{downloaded}"
    )
    print(
        f"Already Existing   : "
        f"{existing}"
    )
    print(
        f"Failed             : "
        f"{failed}"
    )
    print(
        f"PDFs Available     : "
        f"{downloaded + existing}"
    )
    print(
        f"Folder             : "
        f"{folder}"
    )
    print(
        f"Text Report        : "
        f"{report_path.name}"
    )
    print(
        f"CSV Log            : "
        f"{log_path.name}"
    )
    print("=" * 78)

    context.close()


# ============================================================
# GENERIC OFFICIAL JUDGMENT-SITE ENGINE
# Used for sites whose result HTML differs from eCourts.
# ============================================================

def generic_link_is_document(link, row_text=""):
    try:
        href = (link.get_attribute("href") or "").strip()
        text = (link.inner_text() or "").strip()
        title = (link.get_attribute("title") or "").strip()
        aria = (link.get_attribute("aria-label") or "").strip()
        onclick = (link.get_attribute("onclick") or "").strip()

        combined = (
            f"{href} {text} {title} {aria} {onclick}"
        ).lower()
        row_lower = (row_text or "").lower()

        # Strong PDF/document indicators.
        strong = [
            ".pdf",
            "showfilejudgment",
            "showjudgment",
            "showjudgement",
            "viewjudgment",
            "viewjudgement",
            "view_judgment",
            "view_judgement",
            "judgmentpdf",
            "judgementpdf",
            "viewojpdf",
            "webshowjudgment",
            "downloadjudgment",
            "downloadjudgement",
            "download_judgment",
            "download_judgement",
        ]

        if any(token in combined for token in strong):
            return True

        # Result-table fallback: if the row itself is clearly a judgment/final
        # order result and the link looks like a view/download action.
        if (
            ("judgment" in row_lower or "judgement" in row_lower)
            and any(
                token in combined
                for token in ["view", "download", "open", "order"]
            )
        ):
            return True

    except Exception:
        pass

    return False


def get_generic_records(page, verbose=True):
    records = []
    serial_counter = 0

    try:
        rows = page.locator("table tbody tr")
    except Exception:
        rows = None

    if rows is not None and rows.count() > 0:
        for row_index in range(rows.count()):
            row = rows.nth(row_index)

            try:
                cells = row.locator("td")
                row_text = re.sub(
                    r"\s+",
                    " ",
                    row.inner_text().strip()
                )

                if not row_text:
                    continue

                serial_counter += 1
                serial = serial_counter

                if cells.count() > 0:
                    try:
                        first_text = cells.nth(0).inner_text().strip()
                        match = re.search(r"\d+", first_text)
                        if match:
                            serial = int(match.group())
                    except Exception:
                        pass

                case_label = row_text
                if cells.count() > 1:
                    try:
                        candidate = re.sub(
                            r"\s+",
                            " ",
                            cells.nth(1).inner_text().strip()
                        )
                        if candidate:
                            case_label = candidate
                    except Exception:
                        pass

                links = row.locator("a[href]")
                doc_index = 0

                for link_index in range(links.count()):
                    link = links.nth(link_index)

                    if not generic_link_is_document(
                        link,
                        row_text
                    ):
                        continue

                    doc_index += 1
                    href = (link.get_attribute("href") or "").strip()
                    link_text = re.sub(
                        r"\s+",
                        " ",
                        (link.inner_text() or "").strip()
                    )

                    records.append({
                        "serial": serial,
                        "case_number": case_label,
                        "doc_index": doc_index,
                        "href": href,
                        "link_text": link_text or "Judgment",
                        "mode": "row",
                        "row_index": row_index,
                        "link_index": link_index,
                    })

            except Exception:
                continue

    # Some official sites do not render results in a conventional table.
    # Use a strict page-wide fallback only when no result links were found.
    if not records:
        try:
            links = page.locator("a[href]")

            for link_index in range(links.count()):
                link = links.nth(link_index)

                if not generic_link_is_document(link, ""):
                    continue

                href = (link.get_attribute("href") or "").strip()
                link_text = re.sub(
                    r"\s+",
                    " ",
                    (link.inner_text() or "").strip()
                )

                # Exclude obvious site-wide static documents/navigation.
                low = f"{href} {link_text}".lower()
                if any(
                    token in low
                    for token in [
                        "annual report",
                        "annualreport",
                        "newsletter",
                        "rules.pdf",
                        "calendar.pdf",
                    ]
                ):
                    continue

                serial = len(records) + 1
                records.append({
                    "serial": serial,
                    "case_number": link_text or f"Judgment_{serial}",
                    "doc_index": 1,
                    "href": href,
                    "link_text": link_text or "Judgment",
                    "mode": "global",
                    "global_link_index": link_index,
                })

        except Exception:
            pass

    if verbose:
        print(f"Judgment/PDF result links detected: {len(records)}")

    return records


def find_generic_link(page, item):
    try:
        if item.get("mode") == "row":
            rows = page.locator("table tbody tr")
            row = rows.nth(item["row_index"])
            links = row.locator("a[href]")
            return links.nth(item["link_index"])

        links = page.locator("a[href]")
        return links.nth(item["global_link_index"])

    except Exception:
        return None


def generic_click_download(page, item, filepath):
    link = find_generic_link(page, item)

    if link is None:
        return False

    # 1. Browser download event.
    try:
        with page.expect_download(timeout=10000) as info:
            link.click()

        download = info.value
        download.save_as(str(filepath))

        if filepath.exists() and filepath.stat().st_size > 500:
            return True

    except Exception:
        pass

    # 2. Popup/new tab.
    try:
        old_pages = set(page.context.pages)
        link.click()
        page.wait_for_timeout(1800)

        new_pages = [
            p for p in page.context.pages
            if p not in old_pages
        ]

        if new_pages:
            popup = new_pages[-1]
            popup.wait_for_timeout(800)
            popup_url = popup.url

            success = False
            if popup_url:
                success = direct_download(
                    page.context,
                    popup_url,
                    filepath,
                    page.url
                )

            try:
                popup.close()
            except Exception:
                pass

            if success:
                return True

    except Exception:
        pass

    # 3. Same-tab navigation fallback.
    try:
        old_url = page.url
        link = find_generic_link(page, item)

        if link is None:
            return False

        link.click()
        page.wait_for_timeout(1500)

        if page.url != old_url:
            new_url = page.url
            success = direct_download(
                page.context,
                new_url,
                filepath,
                old_url
            )

            try:
                page.go_back(
                    wait_until="domcontentloaded",
                    timeout=20000
                )
            except Exception:
                pass

            return success

    except Exception:
        pass

    return False


def download_generic_item(page, context, item, filepath):
    href = (item.get("href") or "").strip()

    if (
        href
        and href != "#"
        and not href.lower().startswith("javascript:")
    ):
        full_url = urljoin(page.url, href)

        if direct_download(
            context,
            full_url,
            filepath,
            page.url
        ):
            return True

    print("    Trying browser-click method...")
    return generic_click_download(
        page,
        item,
        filepath
    )


def generic_signature(page):
    records = get_generic_records(
        page,
        verbose=False
    )

    signature = []
    for item in records[:10]:
        signature.append(
            (
                item.get("href", ""),
                item.get("case_number", ""),
            )
        )

    return tuple(signature)


def generic_go_next_page(page):
    selectors = [
        'a:has-text("Next")',
        'button:has-text("Next")',
        'a[title*="Next"]',
        'a[aria-label*="Next"]',
        'a:has-text(">")',
    ]

    next_button = None

    for selector in selectors:
        try:
            candidates = page.locator(selector)
            if candidates.count() > 0:
                next_button = candidates.last
                break
        except Exception:
            pass

    if next_button is None:
        print("No Next page control found. Stopping.")
        return False

    try:
        own_class = (next_button.get_attribute("class") or "").lower()
        parent_class = ""
        aria_disabled = (
            next_button.get_attribute("aria-disabled") or ""
        ).lower()

        try:
            parent_class = (
                next_button
                .locator("xpath=..")
                .get_attribute("class")
                or ""
            ).lower()
        except Exception:
            pass

        if (
            "disabled" in own_class
            or "disabled" in parent_class
            or aria_disabled == "true"
        ):
            print("Next page is disabled. Stopping.")
            return False

    except Exception:
        pass

    old_signature = generic_signature(page)
    old_url = page.url

    try:
        next_button.click()
        page.wait_for_timeout(1500)

        try:
            page.wait_for_load_state(
                "domcontentloaded",
                timeout=15000
            )
        except Exception:
            pass

        for _ in range(20):
            new_signature = generic_signature(page)

            if new_signature and new_signature != old_signature:
                print("Next page contains result data.")
                return True

            if page.url != old_url and new_signature:
                print("Next page contains result data.")
                return True

            page.wait_for_timeout(300)

        print(
            "Next page was opened but no new result data "
            "was found. Stopping."
        )
        return False

    except Exception as exc:
        print(f"Next page error: {exc}")
        return False


def process_generic(court, browser):
    context = browser.new_context(
        accept_downloads=True
    )
    page = context.new_page()

    print()
    print("=" * 78)
    print(court["name"].upper())
    print("=" * 78)

    page.goto(
        court["url"],
        wait_until="domcontentloaded",
        timeout=60000
    )

    print()
    print("Use the official judgment search shown in the browser.")
    print("  1. Select/enter the required FROM and TO date")
    print("  2. Select bench/type if the website requires it")
    print("  3. Enter CAPTCHA/security code if shown")
    print("  4. Submit/Search")
    print("  5. Wait until the judgment result list appears")
    print()

    if "Allahabad" in court["name"]:
        print(
            "Allahabad: select the required Main Seat/Bench and "
            "use the judgment/order date search."
        )
    elif "Punjab" in court["name"]:
        print(
            "Punjab & Haryana: use the judgment search and the "
            "date fields on the official page."
        )
    elif "Sikkim" in court["name"]:
        print(
            "Sikkim: use Judgments / Final Orders (Datewise)."
        )

    print()
    input(
        "After the result list appears, press ENTER here... "
    )

    from_date, to_date = resolve_search_dates(page)
    print_selected_dates(from_date, to_date)

    folder = make_download_folder(
        court,
        from_date,
        to_date
    )

    page_number = 1
    rows_checked = 0
    judgments_found = 0
    downloaded = 0
    existing = 0
    failed = 0
    log_rows = []

    while True:
        print()
        print("-" * 78)
        print(f"RESULT PAGE {page_number}")
        print("-" * 78)

        records = get_generic_records(page)

        if not records:
            print(
                "No judgment/PDF result data found on this page. "
                "Stopping."
            )
            break

        rows_checked += len(records)
        judgments_found += len(records)

        print("Downloading THIS PAGE first...")

        for item in records:
            serial = item["serial"]
            case_name = clean_filename(
                item["case_number"],
                max_len=90
            )

            if item.get("doc_index", 1) > 1:
                filename = (
                    f"{serial:03d}_"
                    f"J{item['doc_index']}_"
                    f"{case_name}_Judgment.pdf"
                )
            else:
                filename = (
                    f"{serial:03d}_"
                    f"{case_name}_Judgment.pdf"
                )

            filepath = folder / filename
            status = ""

            print()
            print(f"Record      : {serial}")
            print(f"Case/Label  : {item['case_number']}")
            print(f"File        : {filename}")

            if filepath.exists() and filepath.stat().st_size > 500:
                existing += 1
                status = "ALREADY DOWNLOADED"
                print("Status      : ALREADY DOWNLOADED")
            else:
                success = download_generic_item(
                    page,
                    context,
                    item,
                    filepath
                )

                if success:
                    downloaded += 1
                    status = "DOWNLOADED"
                    print("Status      : ✓ DOWNLOADED")
                else:
                    failed += 1
                    status = "FAILED"
                    print("Status      : ✗ FAILED")

                page.wait_for_timeout(
                    int(DOWNLOAD_DELAY * 1000)
                )

            log_rows.append({
                "Court": court["name"],
                "Selected From Date": from_date,
                "Selected To Date": to_date,
                "Page": page_number,
                "Court Serial": serial,
                "Case Number": item["case_number"],
                "File Name": filename,
                "Status": status,
            })

        print()
        print(
            f"Page {page_number} completed. "
            "Now checking whether a Next page exists AND "
            "contains new result data..."
        )

        if not generic_go_next_page(page):
            break

        page_number += 1
        if page_number > 100:
            print("Pagination safety limit reached.")
            break

    report_path, log_path = write_run_report(
        folder=folder,
        court_name=court["name"],
        from_date=from_date,
        to_date=to_date,
        pages=page_number,
        rows_checked=rows_checked,
        judgments_found=judgments_found,
        downloaded=downloaded,
        existing=existing,
        failed=failed,
        log_rows=log_rows,
    )

    print()
    print("=" * 78)
    print("FINAL REPORT")
    print("=" * 78)
    print(f"Court              : {court['name']}")
    print(f"Selected From Date : {from_date}")
    print(f"Selected To Date   : {to_date}")
    print(
        f"Downloaded Date(s) : "
        f"{selected_date_text(from_date, to_date)}"
    )
    print(f"Pages Processed    : {page_number}")
    print(f"Judgments Found    : {judgments_found}")
    print(f"Downloaded Now     : {downloaded}")
    print(f"Already Existing   : {existing}")
    print(f"Failed             : {failed}")
    print(f"PDFs Available     : {downloaded + existing}")
    print(f"Folder             : {folder}")
    print(f"Text Report        : {report_path.name}")
    print(f"CSV Log            : {log_path.name}")
    print("=" * 78)

    context.close()


# ============================================================
# MENU
# ============================================================

def show_menu():
    print()
    print("=" * 78)
    print(APP_TITLE.center(78))
    print("=" * 78)

    for key, court in COURTS.items():
        print(f"{key:>2}. {court['name']}")

    print(" 0. Exit")
    print("=" * 78)


def run_selected(court, browser):
    engine = court["engine"]

    if engine == "ecourts":
        process_ecourts(court, browser)

    elif engine == "delhi":
        process_delhi(court, browser)

    elif engine == "himachal":
        process_himachal(court, browser)

    elif engine == "generic":
        process_generic(court, browser)

    else:
        raise ValueError(f"Unknown engine: {engine}")


def main():
    print()
    print(APP_TITLE)
    print()
    print("Downloads will be saved under:")
    print(output_root())
    print()
    print(
        "CAPTCHA is entered manually in the browser. "
        "The program does not bypass CAPTCHA."
    )

    with sync_playwright() as playwright:
        browser = launch_browser(playwright)

        try:
            while True:
                show_menu()

                choice = input("Select court number: ").strip()

                if choice == "0":
                    break

                court = COURTS.get(choice)

                if court is None:
                    print("Invalid selection. Try again.")
                    continue

                try:
                    run_selected(
                        court,
                        browser
                    )

                except KeyboardInterrupt:
                    print()
                    print("Current court operation cancelled.")

                except Exception as exc:
                    print()
                    print("=" * 78)
                    print("ERROR")
                    print("=" * 78)
                    print(exc)
                    print()
                    print(
                        "The application will return to the court menu "
                        "instead of closing."
                    )

                print()
                again = input(
                    "Return to court menu? (Y/N): "
                ).strip().lower()

                if again not in ("y", "yes", ""):
                    break

        finally:
            try:
                browser.close()
            except Exception:
                pass

    print()
    print("Finished.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print()
        print("Fatal error:")
        print(exc)
        input("\nPress ENTER to close...")
