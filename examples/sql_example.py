import sqlite3
import os


def insert_record(db, name, phone, birthday):
    db.execute(''' INSERT INTO test_table (NAME,PHONE,BIRTHDAY)
                  VALUES(?,?,?)''', (name, phone, birthday))
    db.commit()


def read_data(db):
    data = db.execute(''' SELECT * FROM test_table ORDER BY NAME''')
    for record in data:
        print(" ".join([str(item) for item in record]))


def main():
    db = sqlite3.connect('test.db')

    db.execute(''' CREATE TABLE IF NOT EXISTS test_table(
        NAME TEXT NOT NULL,
        PHONE TEXT NOT NULL,
        BIRTHDAY TEXT NOT NULL) ''')

    insert_record(db, "Stan Smith", "+1-900-456-43-34", "01.02.1990")
    insert_record(db, "Ivan Ivanov", "0-345-43-43", "25.03.1874")
    insert_record(db, "Rodger Wellington", "+7-950-434-43-43", "05/03/2000")

    read_data(db)
    db.close()
    os.remove("test.db")


if __name__ == "__main__":
    main()
