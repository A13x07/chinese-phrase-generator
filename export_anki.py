import sqlite3
from pypinyin import pinyin, Style
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

DATABASE_PATH = "data/chinese_learning.db"
OUTPUT_PATH = "data/anki_export.txt"


def get_phrases_by_difficulty(difficulty_levels=None):
    """Get phrases from the database filtered by difficulty."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    if difficulty_levels is None:
        difficulty_levels = ["easy"]

    placeholders = ", ".join("?" for _ in difficulty_levels)
    cursor.execute(
        f"SELECT phrase, difficulty FROM phrases WHERE difficulty IN ({placeholders})",
        difficulty_levels
    )

    phrases = cursor.fetchall()
    conn.close()
    return phrases


def add_pinyin(phrase):
    """Convert a Chinese phrase to pinyin."""
    punctuation = set("。？！，、；：""''（）《》【】…—·.?!,;:\"'()")
    result = pinyin(phrase, style=Style.TONE)
    return " ".join([item[0] for item in result if item[0] not in punctuation])


def translate_phrases(phrases):
    """Use Claude API to translate a list of Chinese phrases."""
    client = Anthropic()

    phrases_text = "\n".join(phrases)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"""Translate each Chinese phrase to English. 
Return ONLY the translations, one per line, in the same order.
Do not include the original Chinese or any numbering.

{phrases_text}"""
            }
        ]
    )

    response_text = message.content[0].text
    translations = [line.strip() for line in response_text.strip().split("\n") if line.strip()]

    return translations


def export_to_anki(phrases, pinyin_list, translations, output_path):
    """Export phrases with pinyin and translations in Anki format."""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("#separator:tab\n")
        file.write("#html:false\n")

        for phrase, py, translation in zip(phrases, pinyin_list, translations):
            file.write(f"{phrase}\t{py}\t{translation}\n")

    print(f"Exported {len(phrases)} phrases to {output_path}")


if __name__ == "__main__":
    # Get easy and medium phrases
    results = get_phrases_by_difficulty(["easy", "medium"])

    if not results:
        print("No phrases found. Run analyse_phrases.py first.")
        exit()

    phrases = [row[0] for row in results]
    difficulties = [row[1] for row in results]

    print(f"Found {len(phrases)} phrases to export")

    # Add pinyin
    print("Adding pinyin...")
    pinyin_list = [add_pinyin(phrase) for phrase in phrases]

    # Translate
    print("Translating...")
    translations = translate_phrases(phrases)

    # Check counts match
    if len(translations) != len(phrases):
        print(f"Warning: got {len(translations)} translations for {len(phrases)} phrases")
        # Pad or trim to match
        while len(translations) < len(phrases):
            translations.append("(translation missing)")
        translations = translations[:len(phrases)]

    # Export
    export_to_anki(phrases, pinyin_list, translations, OUTPUT_PATH)

    # Show a sample
    print("\nSample output:\n")
    for i in range(min(5, len(phrases))):
        print(f"  Chinese:     {phrases[i]}")
        print(f"  Pinyin:      {pinyin_list[i]}")
        print(f"  English:     {translations[i]}")
        print(f"  Difficulty:  {difficulties[i]}")
        print()