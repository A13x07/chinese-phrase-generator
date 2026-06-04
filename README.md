# Chinese Phrase Generator

A tool that generates Chinese reading and speaking practice material 
matched to the learner's current vocabulary level.

**The problem:** As a beginner studying Chinese (~300-400 characters), 
finding practice material at the right level is difficult. Most 
content either uses vocabulary I haven't learned yet or is too 
repetitive.

**The solution:** This program takes my known vocabulary (exported from 
Anki), generates new phrases using AI, then analyses and classifies 
them by difficulty based on how many unknown words they contain.

## Tech Stack
- Python (data cleaning, text processing, API interaction)
- SQLite (storage, classification, analysis)
- Claude API (phrase generation and translation)
- jieba (Chinese word segmentation)
- pypinyin (pinyin generation)

## Setup
1. Clone the repository
2. Create a virtual environment
3. Install dependencies with `pip install -r requirements.txt`
4. Create a `.env` file with your API key
5. Place Anki exports in `data/raw/`
6. Run `python main.py` to execute the full pipeline

## Output
- Phrases classified by difficulty (easy, medium, hard)
- Frequency analysis of unknown words
- Anki-importable file at `data/anki_export.txt`

## Documentation
Task-by-task development documentation is in the `docs/` folder.