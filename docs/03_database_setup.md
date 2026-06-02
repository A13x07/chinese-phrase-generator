# Task 03 — Database Setup

## What was done
- Created `setup_database.py` to build and populate a SQLite database
- Two tables created:
  - `anki_raw` — stores all original Anki records (Chinese, pinyin, 
    English, source file). 329 records loaded.
  - `words` — stores unique Chinese words only. 311 words loaded.
- The script reuses the cleaning function from `clean_anki_export.py`
- Added `*.db` to `.gitignore` since the database is regenerated 
  from raw data

## SQL features used
- `CREATE TABLE` with `PRIMARY KEY AUTOINCREMENT`
- `INSERT OR IGNORE` to handle duplicates
- `DROP TABLE IF EXISTS` for safe rebuilds during development
- Parameterised queries (`?`) to prevent SQL injection

## Why
The database is the foundation of the system. All phrase 
generation, analysis, and classification in later steps will 
query this database to determine which words the student knows.