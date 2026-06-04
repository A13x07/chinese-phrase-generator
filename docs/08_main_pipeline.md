# Task 08 — Main Pipeline

## What was done
- Created `main.py` to run the entire system in one command
- Five steps executed in sequence:
  1. Build database from Anki exports
  2. Generate phrases using Claude API
  3. Analyse and classify phrases by difficulty
  4. Run frequency analysis on unknown words
  5. Export phrases with pinyin and translation to Anki format
- Number of phrases is configurable via `NUMBER_OF_PHRASES`

## Why
Running individual scripts in the correct order is error-prone. 
A single entry point makes the system easy to use and demo. 
In the presentation, one command demonstrates the complete 
learning cycle from Anki export to Anki import.