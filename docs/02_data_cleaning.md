# Task 02 — Data Cleaning

## What was done
- Created `clean_anki_export.py` to process raw Anki exports
- The script reads all `.txt` files from `data/raw/`
- Skips Anki metadata lines (`#separator:tab`, `#html:false`)
- Splits each line by tab and extracts only the first column 
  (Chinese characters)
- Uses a regex pattern to verify the text contains Chinese 
  characters (Unicode range \u4e00–\u9fff)
- Removes duplicates while preserving order
- Result: 311 unique Chinese words extracted from 3 Anki decks

## Why
The raw Anki exports contain pinyin, English translations, 
Russian translations, and formatting metadata. The system only 
needs the Chinese words themselves. Cleaning the data first 
ensures only valid Chinese vocabulary enters the database.