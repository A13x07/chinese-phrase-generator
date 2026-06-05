# Chinese Phrase Generator

A tool that generates Chinese reading and speaking practice material 
matched to the learner's current vocabulary level.

**The problem:** As a beginner studying Chinese (~300 known words), 
finding practice material at the right level is difficult. Most 
content either uses vocabulary I haven't learned yet or is too 
repetitive.

**The solution:** This program takes my known vocabulary (exported from 
Anki), generates new phrases and dialogues using AI, then analyses 
and classifies them by difficulty based on how many unknown words 
they contain.

## Tech Stack
- Python (data cleaning, text processing, API interaction)
- SQLite (storage, classification, analysis, views)
- Claude API (phrase and dialogue generation, translation)
- jieba (Chinese word segmentation)
- pypinyin (pinyin generation)

## Setup
1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your API key: `ANTHROPIC_API_KEY=your-key`
6. Place Anki exports in `data/raw/`
7. Run `python main.py`

## What the pipeline does
1. Cleans and loads Anki vocabulary into a database
2. Generates practice phrases using AI (capped at 30% of vocabulary)
3. Analyses each phrase against known vocabulary using word segmentation
4. Classifies phrases by difficulty (0, 1, 2, 3+ unknown words)
5. Identifies the most valuable unknown words to learn next
6. Exports phrases into separate Anki-importable files by difficulty
7. Generates verified dialogues for speaking practice

## Output files
- `data/known_phrases.txt` — fully known phrases
- `data/one_unknown.txt` — phrases with one new word
- `data/two_unknown.txt` — phrases with two new words
- `data/three_plus_unknown.txt` — phrases with three or more new words
- `data/dialogues_chinese.txt` — dialogues (characters only)
- `data/dialogues_pinyin.txt` — dialogues (characters + pinyin)
- `data/dialogues_translation.txt` — dialogues (characters + English)
- `data/dialogues_full.txt` — dialogues (characters + pinyin + English)

## Documentation
Task-by-task development documentation is in the `docs/` folder.

## Note on classification
Difficulty is determined by comparing each generated phrase against 
the learner's known vocabulary using word segmentation (jieba). 
Phrases are classified by the number of unknown words they contain: 
easy (0), medium (1), hard (2), and very hard (3+). This 
classification is approximate, as accuracy depends on segmentation 
and context.