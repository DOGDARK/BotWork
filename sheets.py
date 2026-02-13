import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

from config import SPREADSHEET_NAME

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1


def get_all_rows():
    return sheet.get_all_values()[1:]


def add_user(username: str) -> bool:
    if username in sheet.col_values(1):
        return False
    sheet.append_row([username, ""])
    return True


def get_free_users():
    return [
        row[0] for row in get_all_rows()
        if len(row) < 2 or row[1] == ""
    ]


def find_row(username: str):
    for idx, val in enumerate(sheet.col_values(1), start=1):
        if val == username:
            return idx
    return None


def set_status(username: str, status: str):
    row = find_row(username)
    if not row:
        return False

    if status == "review":
        today = date.today().strftime("%d.%m.%Y")
        sheet.update_cell(row, 2, f"отзыв оставлен {today}")
    else:
        sheet.update_cell(row, 2, status)
    return True


def delete_user(username: str):
    row = find_row(username)
    if not row:
        return False
    sheet.delete_rows(row)
    return True
