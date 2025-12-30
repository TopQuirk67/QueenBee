# QueenBee Notebook Organization

## 📚 Notebook Structure (Updated Dec 2025)

### 1. QB Data Pipeline.ipynb (formerly "Gary Private Spelling Bee Analysis.ipynb")
**Purpose:** DATA PIPELINE - Run once per day/week to refresh datasets

**What it does:**
- Loads data from Google Sheets (solutions DB, missed words, last words)
- Validates data for typos and duplicates
- Calculates word difficulty scores with time decay (2-year half-life)
- **NEW:** Tracks "easy finds" to recognize learning improvement
- Exports datasets for downstream use

**Outputs:**
- `data/ml_word_dataset.csv` - Comprehensive word dataset for ML (~60k+ words)
- `data/study_list_*.csv` - Four study list categories (valid words only)
- `data/study_lists.pkl` - Pickled study lists for quiz notebook
- `data/db.csv`, `data/mw.csv`, `data/lw.csv` - Local caches

**Stop Point:** Run cells through "STOP HERE" marker. Don't run legacy code below that marker.

---

### 2. QB Quiz Notebook.ipynb
**Purpose:** INTERACTIVE STUDY - Quiz yourself on difficult words

**Features:**
- Four study categories:
  - Singleton 4-letter words (e.g., NOEL, NOIR)
  - Multi-word 4-letter alphagrams
  - Singleton 5+ letter words
  - Multi-word 5+ letter alphagrams
- Progressive hints after wrong guesses
- Highlights your "focus word" from difficulty scoring
- Statistics tracking (perfect/skipped/revealed)

**Quick Start:**
```python
# Quiz 10 random singleton 4-letter words
run_category_quiz('singleton_4letter', max_words=10, randomize=True)

# Quiz 20 multi-word 5+ letter alphagrams
run_category_quiz('multi_5plus', max_words=20, randomize=True)
```

---

### 3. QB Analysis & Plots.ipynb
**Purpose:** EXPLORATORY ANALYSIS - Visualize trends and patterns

**Analyses:**
- Performance over time (monthly trends)
- Queen Bee rate tracking
- Puzzle difficulty by size/day of week
- Word difficulty distributions
- Difficulty vs frequency correlations
- Custom ad-hoc queries

**Data Sources:**
- Loads `data/db.csv`, `data/mw.csv`, `data/lw.csv`
- Loads `data/ml_word_dataset.csv` for richer analysis

---

## 🔄 Typical Workflow

1. **Weekly Data Refresh:**
   - Run main analysis notebook through "STOP HERE" marker
   - Exports fresh datasets with latest Google Sheets data

2. **Daily Study:**
   - Open QB Quiz Notebook
   - Select category and word count
   - Practice!

3. **Monthly Review:**
   - Open QB Analysis & Plots
   - Check performance trends
   - Identify patterns in difficult words

4. **ML Development:**
   - Use `data/ml_word_dataset.csv` as input
   - Train models to predict word difficulty
   - Generate puzzle recommendations

---

## 📊 Dataset Descriptions

### ml_word_dataset.csv
Comprehensive dataset for machine learning with **all** potential words:

| Column | Description |
|--------|-------------|
| word | The word |
| alphagram | Sorted unique letters (e.g., NANKEEN → AEKN) |
| word_length | Number of letters in word |
| alphagram_length | Number of distinct letters |
| validity | valid/invalid/unknown based on most recent puzzle |
| last_valid_date | Date of last validity check |
| has_been_played | Whether word appeared in any puzzle solution |
| total_difficulty | **Average difficulty across ALL appearances** (0.0 = never missed/struggled, includes easy finds) |
| missed_count | Raw count of misses (no decay) |
| last_words_avg_score | Raw average of last-words position scores (no decay) |
| easy_find_occurrences | Count of appearances where word was not missed or last word |
| total_appearances | Total times word appeared in all puzzles played |
| in_scrabble_dict | Boolean - in NWL2023 dictionary |
| frequency | Word frequency from Kaggle dataset (None if missing) |

**Difficulty Scoring Details:**
- Uses 2-year half-life decay: e^(-0.34657 × days_ago / 365.25)
- Each appearance gets scored:
  - Missed: 1.0 × decay_factor
  - Last word: 0.5 × ((N - pos) / N)^5 × decay_factor
  - Easy find: 0.0 × decay_factor
- **Final score = average across all appearances**
- Easy finds dilute scores by adding to denominator: learning is recognized!
- Example: IGLOO with 2 recent misses + 6 easy finds = 0.125 (vs 0.5 if only counting misses)

**Use Cases:**
- Train ML models to predict difficulty
- Find potential new puzzles (valid words not yet played)
- Identify study priorities (valid + high difficulty)

### study_list_*.csv
Four categories of **valid words only**, sorted by difficulty:

- `study_list_singleton_4letter.csv` - Solo 4-letter words
- `study_list_multi_4letter.csv` - 4-letter words with multiple valid words per alphagram
- `study_list_singleton_5plus.csv` - Solo 5+ letter words
- `study_list_multi_5plus.csv` - 5+ letter words with multiple valid words per alphagram

**Columns:**
- word, alphagram, difficulty, missed_count, last_words_avg, frequency
- all_alphagram_words - comma-separated list of all valid words for this alphagram

---

## 🧹 Cleanup Notes

The main analysis notebook contains legacy code below the "STOP HERE" marker. This code can be safely deleted after verifying the new system works:

**Already Migrated:**
- Plots → QB Analysis & Plots.ipynb
- Quiz engine → QB Quiz Notebook.ipynb
- Study lists → New study_categories system

**Keep:**
- `word_history()` function (useful for debugging)
- Code Graveyard sections (already marked deprecated)

---

## 🎯 Future ML Pipeline

1. **Feature Engineering** (using ml_word_dataset.csv):
   - Word frequency
   - Alphagram complexity
   - Letter patterns
   - Compound word detection
   - Historical difficulty

2. **Model Training:**
   - Target: total_difficulty score
   - Features: frequency, word_length, alphagram_length, etc.
   - Predict difficulty for unseen words

3. **Puzzle Generation:**
   - Enumerate all possible 7-letter alphagrams
   - Filter by historical patterns (e.g., S is rare)
   - Rank by predicted difficulty
   - Generate study recommendations

4. **Pre-Study System:**
   - For upcoming puzzles, predict hard words
   - Generate targeted study lists
   - Track improvement over time
