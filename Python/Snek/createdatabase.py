import os
import sqlite3


def main() -> None:
    current = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(f"{current}/Database"):
        os.makedirs(f"{current}/Database")
        print("Directory successfully made")
    cnx = sqlite3.connect(f"{current}/Database/snekscores.db")
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
    main()
