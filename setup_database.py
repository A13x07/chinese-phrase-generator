import sqlite3
import os

RAW_DATA_DIR = "data/raw"
DATABASE_PATH = "data/chinese_learning.db"


def create_database():
    """Create the database and tables."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS anki_raw")
    cursor.execute("DROP TABLE IF EXISTS words")

    cursor.execute("""
        CREATE TABLE anki_raw (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chinese TEXT NOT NULL,
            pinyin TEXT,
            english TEXT,
            source_file TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chinese TEXT NOT NULL UNIQUE
        )
    """)

    conn.commit()
    return conn


def load_raw_records(conn, directory):
    """Load all original Anki records into anki_raw table."""
    cursor = conn.cursor()
    count = 0

    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(directory, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                columns = line.split("\t")

                chinese = columns[0].strip() if len(columns) > 0 else ""
                pinyin = columns[1].strip() if len(columns) > 1 else ""
                english = columns[2].strip() if len(columns) > 2 else ""

                if not chinese:
                    continue

                cursor.execute(
                    "INSERT INTO anki_raw (chinese, pinyin, english, source_file) VALUES (?, ?, ?, ?)",
                    (chinese, pinyin, english, filename)
                )
                count += 1

    conn.commit()
    print(f"Loaded {count} raw records into anki_raw")


def load_unique_words(conn, directory):
    """Load unique Chinese words into words table."""
    cursor = conn.cursor()
    from clean_anki_export import clean_anki_files

    words = clean_anki_files(directory)

    for word in words:
        cursor.execute(
            "INSERT OR IGNORE INTO words (chinese) VALUES (?)",
            (word,)
        )

    conn.commit()
    print(f"Loaded {len(words)} unique words into words table")


if __name__ == "__main__":
    conn = create_database()
    load_raw_records(conn, RAW_DATA_DIR)
    load_unique_words(conn, RAW_DATA_DIR)

    # Verify the data
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM anki_raw")
    print(f"\nVerification:")
    print(f"  anki_raw records: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM words")
    print(f"  unique words: {cursor.fetchone()[0]}")

    # Show a sample query
    print("\nSample: first 10 words from the words table:")
    cursor.execute("SELECT id, chinese FROM words LIMIT 10")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")

    conn.close()