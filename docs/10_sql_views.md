# Task 10 — SQL Views and Grouped Export

## What was done
- Created `create_views.py` with SQL views that group phrases 
  by number of unknown words
- Four views created:
  - `view_known_phrases` — phrases with 0 unknown words
  - `view_one_unknown` — phrases with exactly 1 unknown word
  - `view_two_unknown` — phrases with exactly 2 unknown words
  - `view_three_plus_unknown` — phrases with 3 or more unknowns
- Each view exports to a separate Anki-importable .txt file 
  with Chinese, pinyin, and English translation
- Updated `main.py` to run views and export as the final step
- Removed the old single-file export in favour of grouped files

## SQL features used
- `CREATE VIEW` — saved queries acting as virtual tables
- `GROUP_CONCAT` — combines unknown words into one string
- `JOIN` — connects phrases with word-level analysis
- `GROUP BY` — aggregates word data per phrase
- `ORDER BY` — sorts by word count and difficulty

## Output files
- `data/known_phrases.txt` — fully known, ready for practice
- `data/one_unknown.txt` — one new word to learn
- `data/two_unknown.txt` — two new words to learn
- `data/three_plus_unknown.txt` — advanced, multiple unknowns

## Why
Separating phrases by difficulty gives the student control 
over their learning. Known phrases are for immediate practice. 
Phrases with unknowns are for gradual vocabulary expansion, 
with the student choosing which new words to tackle first.