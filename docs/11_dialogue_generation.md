# Task 11 — Dialogue Generation

## What was done
- Created `generate_dialogues.py` to arrange known phrases 
  into short conversational dialogues
- The AI groups verified easy phrases into dialogues with 
  topics like restaurant, weather, family, making plans
- Each dialogue has 4-6 lines between two speakers (A and B)
- All dialogue lines are validated against the known vocabulary 
  using the same analysis logic from the phrase analysis step
- Four export formats generated:
  - `dialogues_chinese.txt` — characters only
  - `dialogues_pinyin.txt` — characters + pinyin
  - `dialogues_translation.txt` — characters + English
  - `dialogues_full.txt` — characters + pinyin + English

## Scalable generation
- Number of phrases: capped at 30% of total known words
- Number of dialogues: one per 15 known phrases, minimum 3
- Both scale automatically as the student's vocabulary grows

## Database tables
- `dialogues` — stores each dialogue with an ID and topic
- `dialogue_lines` — stores each line with speaker, phrase, 
  and order, linked to its dialogue via FOREIGN KEY

## SQL features used
- `FOREIGN KEY` linking dialogue lines to dialogues
- `JOIN` to connect dialogue lines with their topics
- `ORDER BY` to maintain conversation order
- `cursor.lastrowid` to get the ID of the just-inserted dialogue

## Why
Phrases in isolation are useful for reading practice, but 
dialogues provide context for speaking practice. Grouping 
phrases into conversations makes the practice material more 
realistic and engaging.