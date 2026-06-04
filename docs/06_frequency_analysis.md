# Task 06 — Frequency Analysis

## What was done
- Created `frequency_analysis.py` to analyse unknown words across 
  all generated phrases
- Three SQL-based reports:
  1. **Unknown word frequency** — counts how many phrases each 
     unknown word appears in
  2. **Phrases grouped by unknown word** — shows all phrases 
     containing a specific unknown word
  3. **Most valuable words to learn** — ranks unknown words by 
     how many phrases they would unlock if learned
- Improved `split_unknown_word()` to use a longest-match algorithm 
  that scans left to right, always trying the longest known word 
  first
- Added a check to keep genuinely unknown words whole when no 
  known parts are found (e.g. 时间 stays as one unknown instead 
  of being split into 时 and 间)

## SQL features used
- `COUNT(DISTINCT)` for frequency counting
- `GROUP BY` and `ORDER BY` for aggregation and ranking
- `JOIN` to connect phrases with their word analysis
- `SUM(CASE WHEN ... THEN ... ELSE ... END)` for conditional 
  counting (phrases that would be unlocked)
- Subqueries and filtered aggregation

## Testing results (100 phrases)
- 92 easy, 8 medium, 1 hard, 0 very hard
- Most valuable word to learn: 贵 (expensive) — appears in 2 
  phrases, learning it would unlock both
- The "would unlock" metric correctly shows 0 for words in 
  phrases with multiple unknowns, since learning one word 
  alone would not make the phrase fully readable

## Why
The frequency analysis helps the student decide which new words 
to learn first. A word that appears in multiple phrases is more 
valuable because learning it unlocks more practice material at 
once. This is a data-driven approach to vocabulary expansion.