import sqlite3
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

DATABASE_PATH = "data/chinese_learning.db"


def get_known_words():
    """Fetch all known Chinese words from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chinese FROM words")
    words = [row[0] for row in cursor.fetchall()]
    conn.close()
    return words


def generate_phrases(words, number_of_phrases=20):
    """Send known words to Claude API and get practice phrases back."""
    client = Anthropic()

    word_list = ", ".join(words)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"""Here is a list of Chinese words that I know:

{word_list}

Generate exactly {number_of_phrases} Chinese phrases or short sentences 
for me to practice reading and speaking. 

Rules:
1. Use ONLY the words from my list above. Do not use any words 
   that are not in my list.
2. Each phrase must be 3 or more words long.
3. Make the phrases natural and useful for daily conversation.
4. Write ONLY the Chinese phrases, one per line.
5. Do not include pinyin, English translations, or numbering."""
            }
        ]
    )

    response_text = message.content[0].text
    phrases = [line.strip() for line in response_text.strip().split("\n") if line.strip()]

    return phrases


if __name__ == "__main__":
    words = get_known_words()
    print(f"Loaded {len(words)} known words from database")
    print(f"\nGenerating phrases...\n")

    phrases = generate_phrases(words)

    print(f"Generated {len(phrases)} phrases:\n")
    for i, phrase in enumerate(phrases, 1):
        print(f"  {i}. {phrase}")