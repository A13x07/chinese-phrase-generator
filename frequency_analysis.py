import sqlite3

DATABASE_PATH = "data/chinese_learning.db"


def unknown_word_frequency():
    """Find unknown words that appear across multiple phrases."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    print("=== Unknown Word Frequency ===\n")

    cursor.execute("""
        SELECT pw.word, COUNT(DISTINCT pw.phrase_id) as phrase_count
        FROM phrase_words pw
        WHERE pw.is_known = 0
        GROUP BY pw.word
        ORDER BY phrase_count DESC
    """)

    results = cursor.fetchall()

    if not results:
        print("No unknown words found.")
        conn.close()
        return

    print(f"{'Unknown Word':<15} {'Appears in # phrases':<25}")
    print("-" * 40)

    for word, count in results:
        print(f"{word:<15} {count:<25}")

    conn.close()


def phrases_by_unknown_word():
    """Group phrases by their unknown words."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    print("\n=== Phrases Grouped by Unknown Word ===\n")

    cursor.execute("""
        SELECT DISTINCT pw.word
        FROM phrase_words pw
        WHERE pw.is_known = 0
        ORDER BY pw.word
    """)

    unknown_words = [row[0] for row in cursor.fetchall()]

    for word in unknown_words:
        cursor.execute("""
            SELECT p.phrase, p.difficulty
            FROM phrases p
            JOIN phrase_words pw ON p.id = pw.phrase_id
            WHERE pw.word = ? AND pw.is_known = 0
            ORDER BY p.unknown_count
        """, (word,))

        phrases = cursor.fetchall()
        print(f"Unknown word: {word} ({len(phrases)} phrases)")
        for phrase, difficulty in phrases:
            print(f"  [{difficulty}] {phrase}")
        print()

    conn.close()


def most_valuable_words():
    """Find unknown words that unlock the most phrases if learned."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    print("=== Most Valuable Words to Learn ===\n")
    print("Learning these words would unlock the most new phrases:\n")

    cursor.execute("""
        SELECT pw.word, 
               COUNT(DISTINCT pw.phrase_id) as total_phrases,
               SUM(CASE WHEN p.unknown_count = 1 THEN 1 ELSE 0 END) as would_unlock
        FROM phrase_words pw
        JOIN phrases p ON pw.phrase_id = p.id
        WHERE pw.is_known = 0
        GROUP BY pw.word
        ORDER BY would_unlock DESC, total_phrases DESC
    """)

    results = cursor.fetchall()

    if not results:
        print("No unknown words found.")
        conn.close()
        return

    print(f"{'Word':<15} {'Total phrases':<18} {'Would unlock':<15}")
    print("-" * 48)

    for word, total, unlock in results:
        print(f"{word:<15} {total:<18} {unlock:<15}")

    conn.close()


if __name__ == "__main__":
    unknown_word_frequency()
    phrases_by_unknown_word()
    most_valuable_words()