import sqlite3
from tinydb import TinyDB, where


def get_pages():
    db = TinyDB('./db.json')

    conn = sqlite3.connect('/data/data/com.steadfastinnovation.android.projectpapyrus/databases/papyrus.db')

    last = db.get(where('id') == 'last')['value']

    pages_query = ("SELECT pages.uuid, pages.page_num, notes.name, pages.created FROM pages JOIN notes on pages.note_uuid = notes.uuid"
                   " WHERE pages.modified > {}").format(last)

    last_query = "SELECT MAX(modified) from pages"

    rows = conn.execute(pages_query).fetchall()

    def tag_new(row):
        row = list(row)
        row[3] = True if row[3] > last else False
        return row

    pages = map(tag_new, rows)

    last = conn.execute(last_query).fetchone()[0]

    conn.close()

    db.update({'value': last}, where('id') == 'last')

    return pages
