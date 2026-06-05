from setup_database import create_database, load_raw_records, load_unique_words
from analyse_phrases import create_phrases_table, store_phrases, analyse_phrases
from generate_phrases import get_known_words, generate_phrases
from frequency_analysis import unknown_word_frequency, most_valuable_words

RAW_DATA_DIR = "data/raw"
DATABASE_PATH = "data/chinese_learning.db"

NUMBER_OF_PHRASES = 100


def run_pipeline():
    """Run the complete Chinese Phrase Generator pipeline."""

    # Step 1: Build database from Anki exports
    print("=" * 50)
    print("STEP 1: Building database from Anki exports")
    print("=" * 50)
    conn = create_database()
    load_raw_records(conn, RAW_DATA_DIR)
    load_unique_words(conn, RAW_DATA_DIR)
    conn.close()

    # Step 2: Generate phrases
    print("\n" + "=" * 50)
    print("STEP 2: Generating phrases")
    print("=" * 50)
    create_phrases_table()
    words = get_known_words()
    print(f"Loaded {len(words)} known words")
    phrases = generate_phrases(words, NUMBER_OF_PHRASES)
    store_phrases(phrases)

    # Step 3: Analyse phrases
    print("\n" + "=" * 50)
    print("STEP 3: Analysing phrases")
    print("=" * 50)
    analyse_phrases()

    # Step 4: Frequency analysis
    print("\n" + "=" * 50)
    print("STEP 4: Frequency analysis")
    print("=" * 50)
    unknown_word_frequency()
    most_valuable_words()

    # Step 5: Create views and export to Anki format
    print("\n" + "=" * 50)
    print("STEP 5: Creating views and exporting to Anki")
    print("=" * 50)
    from create_views import create_views, export_views
    create_views()
    export_views()


if __name__ == "__main__":
    run_pipeline()