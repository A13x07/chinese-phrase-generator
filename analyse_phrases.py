import sqlite3
import jieba

DATABASE_PATH = "data/chinese_learning.db"


def create_phrases_table():
    """Create tables for storing and analysing generated phrases."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS phrases")
    cursor.execute("DROP TABLE IF EXISTS phrase_words")

    cursor.execute("""
        CREATE TABLE phrases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phrase TEXT NOT NULL,
            total_words INTEGER DEFAULT 0,
            unknown_count INTEGER DEFAULT 0,
            difficulty TEXT DEFAULT 'unclassified'
        )
    """)

    cursor.execute("""
        CREATE TABLE phrase_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phrase_id INTEGER NOT NULL,
            word TEXT NOT NULL,
            is_known INTEGER NOT NULL,
            FOREIGN KEY (phrase_id) REFERENCES phrases(id)
        )
    """)

    conn.commit()
    conn.close()


def store_phrases(phrases):
    """Store generated phrases in the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    for phrase in phrases:
        cursor.execute(
            "INSERT INTO phrases (phrase) VALUES (?)",
            (phrase,)
        )

    conn.commit()
    conn.close()
    print(f"Stored {len(phrases)} phrases in the database")

def split_unknown_word(word, known_words):
    """Try to split an unknown word into known words."""
    # Try splitting into two parts
    for i in range(1, len(word)):
        left = word[:i]
        right = word[i:]
        if left in known_words and right in known_words:
            return [left, right]

    # Try splitting into three parts
    for i in range(1, len(word)):
        for j in range(i + 1, len(word)):
            left = word[:i]
            middle = word[i:j]
            right = word[j:]
            if left in known_words and middle in known_words and right in known_words:
                return [left, middle, right]

    return [word]

def analyse_phrases():
    """Segment each phrase and check words against known vocabulary."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Get all known words
    cursor.execute("SELECT chinese FROM words")
    known_words = set(row[0] for row in cursor.fetchall())

    # Add known words to jieba so it prioritises them
    for word in known_words:
        jieba.add_word(word, freq=999999)

    # Get all phrases
    cursor.execute("SELECT id, phrase FROM phrases")
    phrases = cursor.fetchall()

    for phrase_id, phrase in phrases:
        # Segment the phrase into words
        words = list(jieba.cut(phrase))

        # Filter out punctuation and empty strings
        punctuation = set("。？！，、；：""''（）《》【】…—·.?!,;:\"'()")
        words = [w for w in words if w.strip() and w not in punctuation]

        unknown_count = 0

        expanded_words = []
        for word in words:
            if word in known_words:
                expanded_words.append(word)
            else:
                expanded_words.extend(split_unknown_word(word, known_words))

        total_words = len(expanded_words)

        for word in expanded_words:
            is_known = 1 if word in known_words else 0
            if not is_known:
                unknown_count += 1

            cursor.execute(
                "INSERT INTO phrase_words (phrase_id, word, is_known) VALUES (?, ?, ?)",
                (phrase_id, word, is_known)
            )

        # Classify difficulty
        if unknown_count == 0:
            difficulty = "easy"
        elif unknown_count == 1:
            difficulty = "medium"
        elif unknown_count == 2:
            difficulty = "hard"
        else:
            difficulty = "very hard"

        cursor.execute(
            "UPDATE phrases SET total_words = ?, unknown_count = ?, difficulty = ? WHERE id = ?",
            (total_words, unknown_count, difficulty, phrase_id)
        )

    conn.commit()
    conn.close()
    print(f"Analysed {len(phrases)} phrases")


if __name__ == "__main__":
    from generate_phrases import generate_phrases, get_known_words

    # Step 1: Create tables
    create_phrases_table()

    # Step 2: Generate and store phrases
    words = get_known_words()
    print(f"Loaded {len(words)} known words")

    phrases = generate_phrases(words, 20)
    store_phrases(phrases)

    # Step 3: Analyse
    analyse_phrases()

    # Step 4: Show results
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    print("\n--- Results by difficulty ---\n")

    for difficulty in ["easy", "medium", "hard", "very hard"]:
        cursor.execute(
            "SELECT phrase, unknown_count FROM phrases WHERE difficulty = ? ORDER BY unknown_count",
            (difficulty,)
        )
        results = cursor.fetchall()
        print(f"{difficulty.upper()} ({len(results)} phrases):")

        for phrase, count in results:
            cursor.execute(
                "SELECT word FROM phrase_words WHERE phrase_id = (SELECT id FROM phrases WHERE phrase = ?) AND is_known = 0",
                (phrase,)
            )
            unknown_words = [row[0] for row in cursor.fetchall()]
            unknown_str = f" — unknown: {', '.join(unknown_words)}" if unknown_words else ""
            print(f"  {phrase}{unknown_str}")

        print()

    conn.close()