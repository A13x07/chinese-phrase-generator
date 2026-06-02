# Task 04 — Phrase Generation

## What was done
- Created `generate_phrases.py` to generate practice phrases 
  using the Claude API
- The script reads known words from the SQLite database and 
  sends them to Claude Sonnet 4.6 with specific instructions
- The prompt restricts the AI to use only known vocabulary and 
  produce phrases of 3+ words
- API key is stored in `.env` (excluded from Git) and loaded 
  using `python-dotenv`
- Successfully generated 20 natural Chinese practice phrases

## Key decisions
- Model: Claude Sonnet 4.6 — best balance of quality and cost
- The number of phrases is configurable via a function parameter
- The prompt is designed to be strict: Chinese only, no pinyin, 
  no translations, no numbering — just raw phrases for analysis

## Dependencies added
- `anthropic` — official Claude API SDK
- `python-dotenv` — loads API key from `.env` file

## Why
The AI generates practice material tailored to the student's 
exact vocabulary level. Without strict prompt rules, the AI 
tends to introduce unknown words, which is why the analysis 
step (next task) is necessary.