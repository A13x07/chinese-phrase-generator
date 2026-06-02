# Chinese Phrase Generator

A tool that generates Chinese reading and speaking practice material
matched to the learner's current vocabulary level.

**The problem:** As a beginner studying Chinese (~300 known words),
finding practice material at the right level is difficult. Most
content either uses vocabulary I haven't learned yet or is too
repetitive.

**The solution:** This program takes my known vocabulary (exported from
Anki), generates new phrases and sentences using AI, then analyses
and classifies them by difficulty based on how many unknown words
they contain.

## Tech Stack
- Python (data cleaning, text processing, API interaction)
- SQLite (storage, classification, analysis)
- Claude API (phrase and sentence generation)
- jieba (Chinese word segmentation)
- pypinyin (pinyin annotation)

## Status
In development.