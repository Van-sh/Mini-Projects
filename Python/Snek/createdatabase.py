import sqlite3
from pathlib import Path


def setup(db_path: Path) -> None:
    db_path.parent.mkdir(exist_ok=True)

    cnx = sqlite3.connect(db_path)
    csr = cnx.cursor()
    csr.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    data = csr.fetchall()
    if ("snekscores",) not in data:
        csr.execute(
            """CREATE TABLE snekscores(
                id integer primary key autoincrement
                , Username varchar(255)
                , highScore integer
                );"""
        )
        print("Table successfully made")
    cnx.close()


if __name__ == "__main__":
    setup(Path("Datababse/snekscores.db"))
