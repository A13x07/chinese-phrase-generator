# Task 07 — Anki Export

## What was done
- Created `export_anki.py` to prepare phrases for Anki import
- The script reads analysed phrases from the database, filtered 
  by difficulty (easy and medium by default)
- Pinyin is generated using the `pypinyin` library
- English translations are generated using the Claude API in a 
  single batch call
- Output is a tab-separated .txt file matching the Anki import 
  format: Chinese, Pinyin, English
- Includes error handling for mismatched translation counts
- Punctuation is filtered from pinyin output

## Complete learning cycle
This completes the full pipeline:
1. Export vocabulary from Anki (.txt files)
2. Clean and load into database
3. Generate practice phrases using AI
4. Analyse and classify by difficulty
5. Identify most valuable unknown words
6. Add pinyin and translations
7. Export back to Anki for further study

## Dependencies added
- `pypinyin` — Chinese to pinyin conversion

## Why
Exporting back to Anki closes the learning loop. The student 
can import generated phrases as new flashcards, practising 
reading and speaking with material matched to their level.