import sqlite3

DATABASE_PATH = "data/chinese_learning.db"


def create_views():
    """Create SQL views to group phrases by number of unknown words."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Drop existing views
    cursor.execute("DROP VIEW IF EXISTS view_known_phrases")
    cursor.execute("DROP VIEW IF EXISTS view_one_unknown")
    cursor.execute("DROP VIEW IF EXISTS view_two_unknown")
    cursor.execute("DROP VIEW IF EXISTS view_three_plus_unknown")

    # View 1: Phrases with no unknown words
    cursor.execute("""
        CREATE VIEW view_known_phrases AS
        SELECT id, phrase, total_words, difficulty
        FROM phrases
        WHERE unknown_count = 0
        ORDER BY total_words
    """)

    # View 2: Phrases with exactly 1 unknown word
    cursor.execute("""
        CREATE VIEW view_one_unknown AS
        SELECT p.id, p.phrase, p.total_words,
               GROUP_CONCAT(pw.word, ', ') AS unknown_words
        FROM phrases p
        JOIN phrase_words pw ON p.id = pw.phrase_id
        WHERE p.unknown_count = 1 AND pw.is_known = 0
        GROUP BY p.id
        ORDER BY p.total_words
    """)

    # View 3: Phrases with exactly 2 unknown words
    cursor.execute("""
        CREATE VIEW view_two_unknown AS
        SELECT p.id, p.phrase, p.total_words,
               GROUP_CONCAT(pw.word, ', ') AS unknown_words
        FROM phrases p
        JOIN phrase_words pw ON p.id = pw.phrase_id
        WHERE p.unknown_count = 2 AND pw.is_known = 0
        GROUP BY p.id
        ORDER BY p.total_words
    """)

    # View 4: Phrases with 3 or more unknown words
    cursor.execute("""
        CREATE VIEW view_three_plus_unknown AS
        SELECT p.id, p.phrase, p.total_words, p.unknown_count,
               GROUP_CONCAT(pw.word, ', ') AS unknown_words
        FROM phrases p
        JOIN phrase_words pw ON p.id = pw.phrase_id
        WHERE p.unknown_count >= 3 AND pw.is_known = 0
        GROUP BY p.id
        ORDER BY p.unknown_count, p.total_words
    """)

    conn.commit()
    print("Views created successfully")

    # Display summary from each view
    print("\n--- Phrase Summary by Difficulty ---\n")

    cursor.execute("SELECT COUNT(*) FROM view_known_phrases")
    print(f"Known phrases (0 unknown):     {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM view_one_unknown")
    print(f"One unknown word:              {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM view_two_unknown")
    print(f"Two unknown words:             {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM view_three_plus_unknown")
    print(f"Three or more unknown words:   {cursor.fetchone()[0]}")

    # Show samples from each view
    print("\n--- Sample: Known Phrases ---")
    cursor.execute("SELECT phrase FROM view_known_phrases LIMIT 5")
    for row in cursor.fetchall():
        print(f"  {row[0]}")

    print("\n--- Sample: One Unknown Word ---")
    cursor.execute("SELECT phrase, unknown_words FROM view_one_unknown LIMIT 5")
    for row in cursor.fetchall():
        print(f"  {row[0]} — unknown: {row[1]}")

    print("\n--- Sample: Two Unknown Words ---")
    cursor.execute("SELECT phrase, unknown_words FROM view_two_unknown LIMIT 5")
    for row in cursor.fetchall():
        print(f"  {row[0]} — unknown: {row[1]}")

    print("\n--- Sample: Three+ Unknown Words ---")
    cursor.execute("SELECT phrase, unknown_words FROM view_three_plus_unknown LIMIT 5")
    for row in cursor.fetchall():
        print(f"  {row[0]} — unknown: {row[1]}")

    conn.close()

def export_views():
    """Export each view to Anki-importable .txt files with pinyin and translation."""
    from export_anki import add_pinyin, translate_phrases

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    views = [
        ("data/known_phrases.txt", "SELECT phrase FROM view_known_phrases"),
        ("data/one_unknown.txt", "SELECT phrase FROM view_one_unknown"),
        ("data/two_unknown.txt", "SELECT phrase FROM view_two_unknown"),
        ("data/three_plus_unknown.txt", "SELECT phrase FROM view_three_plus_unknown"),
    ]

    for filepath, query in views:
        cursor.execute(query)
        phrases = [row[0] for row in cursor.fetchall()]

        if not phrases:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("#separator:tab\n")
                f.write("#html:false\n")
            print(f"  {filepath} — 0 phrases")
            continue

        pinyin_list = [add_pinyin(phrase) for phrase in phrases]
        translations = translate_phrases(phrases)

        while len(translations) < len(phrases):
            translations.append("(translation missing)")
        translations = translations[:len(phrases)]

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("#separator:tab\n")
            f.write("#html:false\n")
            for phrase, py, translation in zip(phrases, pinyin_list, translations):
                f.write(f"{phrase}\t{py}\t{translation}\n")

        print(f"  {filepath} — {len(phrases)} phrases")

    conn.close()
    print("\nAll files ready for Anki import")


if __name__ == "__main__":
    create_views()
    export_views()