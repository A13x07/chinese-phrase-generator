import sqlite3
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

DATABASE_PATH = "data/chinese_learning.db"


def create_dialogue_tables():
    """Create tables for storing dialogues."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS dialogue_lines")
    cursor.execute("DROP TABLE IF EXISTS dialogues")

    cursor.execute("""
        CREATE TABLE dialogues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE dialogue_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dialogue_id INTEGER NOT NULL,
            line_order INTEGER NOT NULL,
            speaker TEXT NOT NULL,
            phrase TEXT NOT NULL,
            FOREIGN KEY (dialogue_id) REFERENCES dialogues(id)
        )
    """)

    conn.commit()
    conn.close()


def get_known_phrases():
    """Get all fully known phrases from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT phrase FROM phrases
        WHERE unknown_count = 0
        ORDER BY id
    """)

    phrases = [row[0] for row in cursor.fetchall()]
    conn.close()
    return phrases


def generate_dialogues(phrases, number_of_dialogues=5):
    """Send known phrases to Claude API to arrange into dialogues."""
    client = Anthropic()

    phrases_text = "\n".join(phrases)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"""Here are Chinese phrases that a student can read:

{phrases_text}

Group these phrases into exactly {number_of_dialogues} short dialogues 
between two people (A and B). Each dialogue should have 4-6 lines.

Rules:
1. Use ONLY phrases from the list above. Do not create new phrases.
2. You may slightly adjust phrases to fit the conversation flow, 
   but keep the same words.
3. Each dialogue should have a clear topic.
4. Format each dialogue exactly like this:

TOPIC: At the restaurant
A: 你好吗？
B: 我很好。
A: 你喜欢吃什么？
B: 我喜欢吃鱼。

Start each new dialogue with TOPIC: followed by the topic name."""
            }
        ]
    )

    return message.content[0].text


def parse_and_store_dialogues(response_text):
    """Parse the AI response and store dialogues in the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    dialogues = response_text.strip().split("TOPIC:")
    dialogues = [d.strip() for d in dialogues if d.strip()]
    for dialogue_text in dialogues:
        lines = dialogue_text.strip().split("\n")

        # First line is the topic
        topic = lines[0].strip()

        cursor.execute(
            "INSERT INTO dialogues (topic) VALUES (?)",
            (topic,)
        )
        dialogue_id = cursor.lastrowid

        line_order = 1
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue

            if line.startswith("A:") or line.startswith("A："):
                speaker = "A"
                phrase = line[2:].strip()
            elif line.startswith("B:") or line.startswith("B："):
                speaker = "B"
                phrase = line[2:].strip()
            else:
                continue

            cursor.execute(
                "INSERT INTO dialogue_lines (dialogue_id, line_order, speaker, phrase) VALUES (?, ?, ?, ?)",
                (dialogue_id, line_order, speaker, phrase)
            )
            line_order += 1

    conn.commit()
    conn.close()


def display_dialogues():
    """Display all dialogues from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, topic FROM dialogues ORDER BY id")
    dialogues = cursor.fetchall()

    print(f"\n=== Generated {len(dialogues)} Dialogues ===\n")

    for dialogue_id, topic in dialogues:
        print(f"--- {topic} ---")

        cursor.execute("""
            SELECT speaker, phrase FROM dialogue_lines
            WHERE dialogue_id = ?
            ORDER BY line_order
        """, (dialogue_id,))

        for speaker, phrase in cursor.fetchall():
            print(f"  {speaker}: {phrase}")
        print()

    conn.close()

def validate_dialogues():
    """Check dialogue lines for unknown words."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    import jieba

    cursor.execute("SELECT chinese FROM words")
    known_words = set(row[0] for row in cursor.fetchall())

    for word in known_words:
        jieba.add_word(word, freq=999999)

    punctuation = set("。？！，、；：""''（）《》【】…—·.?!,;:\"'()")

    cursor.execute("""
        SELECT dl.id, dl.phrase, d.topic
        FROM dialogue_lines dl
        JOIN dialogues d ON dl.dialogue_id = d.id
        ORDER BY d.id, dl.line_order
    """)

    lines = cursor.fetchall()
    flagged = []

    for line_id, phrase, topic in lines:
        words = list(jieba.cut(phrase))
        words = [w for w in words if w.strip() and w not in punctuation]

        from analyse_phrases import split_unknown_word
        expanded = []
        for word in words:
            if word in known_words:
                expanded.append(word)
            else:
                expanded.extend(split_unknown_word(word, known_words))

        unknown = [w for w in expanded if w not in known_words]

        if unknown:
            flagged.append((phrase, topic, unknown))

    conn.close()

    if flagged:
        print(f"\nWarning: {len(flagged)} dialogue lines contain unknown words:\n")
        for phrase, topic, unknown in flagged:
            print(f"  [{topic}] {phrase} — unknown: {', '.join(unknown)}")
    else:
        print("\nAll dialogue lines verified: no unknown words found.")

def export_dialogues():
    """Export dialogues to four .txt files with different formats."""
    from export_anki import add_pinyin, translate_phrases

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, topic FROM dialogues ORDER BY id")
    dialogues = cursor.fetchall()

    all_lines = []
    dialogue_structure = []

    for dialogue_id, topic in dialogues:
        cursor.execute("""
            SELECT speaker, phrase FROM dialogue_lines
            WHERE dialogue_id = ?
            ORDER BY line_order
        """, (dialogue_id,))

        lines = cursor.fetchall()
        dialogue_structure.append((topic, lines))
        for speaker, phrase in lines:
            all_lines.append(phrase)

    conn.close()

    # Generate pinyin and translations for all lines at once
    print("Adding pinyin...")
    pinyin_list = [add_pinyin(phrase) for phrase in all_lines]

    print("Translating...")
    translations = translate_phrases(all_lines)

    while len(translations) < len(all_lines):
        translations.append("(translation missing)")
    translations = translations[:len(all_lines)]

    # Build a lookup from phrase to pinyin and translation
    line_index = 0
    dialogue_data = []
    for topic, lines in dialogue_structure:
        enriched_lines = []
        for speaker, phrase in lines:
            py = pinyin_list[line_index]
            tr = translations[line_index]
            enriched_lines.append((speaker, phrase, py, tr))
            line_index += 1
        dialogue_data.append((topic, enriched_lines))

    # File 1: Characters only
    with open("data/dialogues_chinese.txt", "w", encoding="utf-8") as f:
        for topic, lines in dialogue_data:
            f.write(f"--- {topic} ---\n")
            for speaker, phrase, py, tr in lines:
                f.write(f"{speaker}: {phrase}\n")
            f.write("\n")

    # File 2: Characters + pinyin
    with open("data/dialogues_pinyin.txt", "w", encoding="utf-8") as f:
        for topic, lines in dialogue_data:
            f.write(f"--- {topic} ---\n")
            for speaker, phrase, py, tr in lines:
                f.write(f"{speaker}: {phrase} ({py})\n")
            f.write("\n")

    # File 3: Characters + translation
    with open("data/dialogues_translation.txt", "w", encoding="utf-8") as f:
        for topic, lines in dialogue_data:
            f.write(f"--- {topic} ---\n")
            for speaker, phrase, py, tr in lines:
                f.write(f"{speaker}: {phrase} — {tr}\n")
            f.write("\n")

    # File 4: Characters + pinyin + translation
    with open("data/dialogues_full.txt", "w", encoding="utf-8") as f:
        for topic, lines in dialogue_data:
            f.write(f"--- {topic} ---\n")
            for speaker, phrase, py, tr in lines:
                f.write(f"{speaker}: {phrase} ({py}) — {tr}\n")
            f.write("\n")

    print("\nExported dialogues to:")
    print("  data/dialogues_chinese.txt")
    print("  data/dialogues_pinyin.txt")
    print("  data/dialogues_translation.txt")
    print("  data/dialogues_full.txt")

if __name__ == "__main__":
    create_dialogue_tables()

    phrases = get_known_phrases()
    print(f"Found {len(phrases)} known phrases")

    print("Generating dialogues...\n")
    response = generate_dialogues(phrases)

    parse_and_store_dialogues(response)
    display_dialogues()
    validate_dialogues()
    export_dialogues()