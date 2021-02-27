import sqlite3
import os



text = '/data/data/com.steadfastinnovation.android.projectpapyrus/databases/papyrus.db'

conn = sqlite3.connect('papyrus.db')

print(conn.execute("select max(modified) from pages").fetchone()[0])

conn.close()
