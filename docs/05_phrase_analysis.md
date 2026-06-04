# Task 05 — Phrase Analysis and Classification

## What was done
- Created `analyse_phrases.py` which handles the full pipeline:
  generates phrases, stores them in the database, analyses them
- Added two new database tables:
  - `phrases` — stores each phrase with word count, unknown count, 
    and difficulty level
  - `phrase_words` — stores every word from every phrase, with a 
    flag indicating whether it is known or unknown
- Used `jieba` for Chinese word segmentation (splitting phrases 
  into individual words)
- Added known words to jieba with high frequency to improve 
  segmentation accuracy
- Filtered Chinese punctuation from analysis
- Phrases are classified by difficulty:
  - easy (0 unknown words)
  - medium (1 unknown word)
  - hard (2 unknown words)
  - very hard (3+ unknown words)
- Created `data/raw/additional_words.txt` for common words 
  missing from the original Anki exports

## SQL features used
- `FOREIGN KEY` linking phrase_words to phrases
- `UPDATE` with `WHERE` clause for setting difficulty
- `SELECT` with `ORDER BY` for grouped results
- Subqueries to find unknown words per phrase

## Known limitation
- jieba occasionally merges two known words into one compound 
  (e.g. 我 + 要 → 我要). This is a known limitation of 
  automatic Chinese word segmentation.

## Dependencies added
- `jieba` — Chinese word segmentation library

## Improvements made during testing
- Added `split_unknown_word()` function to handle jieba merging 
  known words (splits into 2 or 3 parts)
- Added known words to jieba dictionary with high frequency to 
  improve segmentation accuracy
- Added `additional_words.txt` for common words missing from 
  Anki exports (吗, 的, 这, 们, etc.)
- Added Chinese punctuation filtering
- Added punctuation rule to the AI prompt for consistent output
- Testing showed 19/20 phrases classified as easy, with the 
  remaining phrase containing a genuinely unknown word (岁)