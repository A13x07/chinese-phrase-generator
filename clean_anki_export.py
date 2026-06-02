import os
import re

RAW_DATA_DIR = "data/raw"


def is_chinese(text):
    """Check if a string contains Chinese characters."""
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def clean_anki_files(directory):
    """Read all .txt files from the directory, extract Chinese words."""
    all_words = []

    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(directory, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Skip empty lines and Anki metadata headers
                if not line or line.startswith("#"):
                    continue

                # Split by tab, take the first column (Chinese)
                columns = line.split("\t")
                chinese_word = columns[0].strip()

                # Only keep if it actually contains Chinese characters
                if chinese_word and is_chinese(chinese_word):
                    all_words.append(chinese_word)

    # Remove duplicates while preserving order
    seen = set()
    unique_words = []
    for word in all_words:
        if word not in seen:
            seen.add(word)
            unique_words.append(word)

    return unique_words


if __name__ == "__main__":
    words = clean_anki_files(RAW_DATA_DIR)
    print(f"Total unique Chinese words extracted: {len(words)}")
    print("First 20 words:")
    for word in words[:20]:
        print(f"  {word}")