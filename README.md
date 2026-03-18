# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a content-based music recommendation system. Given a user's taste profile — preferred genre, mood, energy level, and other audio features — the system scores every song in the catalog and returns the top matches. It demonstrates how a simple weighted-score algorithm can turn raw song attributes into personalized suggestions, and highlights the trade-offs and biases that emerge even from a small, hand-crafted dataset.

---

## How The System Works

### Real-World Recommendation Context

Streaming platforms like Spotify and YouTube Music use two complementary strategies. **Collaborative filtering** looks at what similar users listened to — "people who liked X also liked Y" — and doesn't need to understand the music itself. **Content-based filtering** examines the song's own features (tempo, energy, mood, genre) and matches them to the listener's known preferences. This simulation focuses entirely on content-based filtering so every scoring decision is transparent and explainable.

### Song Features Used

Each `Song` object carries these attributes read from `data/songs.csv`:

| Feature | Type | Description |
|---|---|---|
| `genre` | string | Musical genre (pop, lofi, rock, etc.) |
| `mood` | string | Emotional feel (happy, chill, intense, etc.) |
| `energy` | float 0–1 | Overall intensity and activity level |
| `tempo_bpm` | float | Beats per minute |
| `valence` | float 0–1 | Musical positivity (0 = dark, 1 = bright) |
| `danceability` | float 0–1 | How suitable the track is for dancing |
| `acousticness` | float 0–1 | Likelihood the track is acoustic |

### User Profile

A `UserProfile` (or preference dictionary) stores:
- `favorite_genre` and `favorite_mood` — categorical targets
- `target_energy`, `target_valence`, `target_danceability` — numerical targets on a 0–1 scale
- `likes_acoustic` — boolean flag for acoustic preference
- `feature_weights` — optional per-feature multipliers

### Algorithm Recipe

For each song the system computes:

```
score = 0

if song.genre == user.favorite_genre  →  +2.0  (genre match)
if song.mood  == user.favorite_mood   →  +1.5  (mood match)
score += (1 - |song.energy - target_energy|)  × 1.0   (energy proximity)
score += (1 - |song.valence - target_valence|) × 0.8  (valence proximity)
score += (1 - |song.danceability - target_dance|) × 0.6  (danceability proximity)
if likes_acoustic AND song.acousticness >= 0.6  →  +0.5
```

Songs are then sorted highest-to-lowest and the top *k* are returned.

The **Scoring Rule** judges a single song; the **Ranking Rule** (sort by score, take top k) turns individual judgements into an ordered recommendation list. Both are necessary — scoring without ranking gives no recommendations, and ranking without a principled score gives meaningless ones.

### Data Flow

```
User Preferences
      │
      ▼
┌─────────────────────────────────────────┐
│  For each song in songs.csv:            │
│    score, reasons = score_song(prefs,   │
│                                  song)  │
└─────────────────────────────────────────┘
      │
      ▼
Sort by score (highest first)
      │
      ▼
Return Top-K Recommendations
(song, score, explanation)
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the recommender:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Experiments Tried

### Experiment 1 — Weight shift: double energy, halve genre

Changing genre weight from 2.0 → 1.0 and energy weight from 1.0 → 2.0 caused the high-energy pop profile to surface synthwave and EDM songs ahead of actual pop tracks. Songs like *One More Time* (EDM) and *Blinding Lights* (synthpop) moved up significantly. The genre label no longer acted as a hard gate, which produced more diverse but less genre-focused results.

### Experiment 2 — Feature removal: comment out mood scoring

Removing the mood bonus (+1.5) caused the chill lofi profile to rank *Focus Flow* (#1) above both *Library Rain* and *Midnight Coding* — which share both genre AND mood with the user — because the energy gap was marginally tighter. This confirmed mood is a strong differentiator and should stay weighted.

### Experiment 3 — Edge case: moody + high energy (conflicted profile)

A user who wants `mood: moody` but `energy: 0.90` creates an intentional conflict — most moody songs in the catalog are low energy. The system handled it gracefully: *Night Drive Loop* (synthwave, moody, energy=0.75) scored highest as the best available compromise. It didn't score perfectly on either axis but balanced both better than any other song.

---

## Limitations and Risks

- **Tiny catalog** — 22 songs means genre coverage is sparse; some genres have only one representative, so genre matching is almost deterministic.
- **No listening history** — the system knows nothing about what the user has already heard or skipped.
- **Binary categorical matching** — genre and mood are exact-string matches; "indie pop" and "pop" are treated as completely different even though they overlap.
- **Filter bubble risk** — a pop fan will almost always see pop songs at the top regardless of other features, because the +2.0 genre bonus is hard to overcome.
- **No lyric or language understanding** — two songs can have identical audio features but completely different cultural meaning.

---

## Reflection

See [model_card.md](model_card.md) for the full model card and personal reflection.

Building even this minimal recommender made it clear how much weight a single design choice carries. The decision to give genre a +2.0 bonus (vs. energy's proximity score of at most +1.0) effectively hard-wires genre as the dominant signal. A pop fan will rarely see jazz at the top, no matter how well it matches on every other dimension. Real platforms face the same dilemma at massive scale — prioritizing familiar genres keeps engagement high in the short term but traps users in a narrowing taste bubble over time. The "filter bubble" isn't a bug that crept in accidentally; it is the predictable output of optimizing for familiarity.

Using AI assistance throughout this project was useful for generating boilerplate and surfacing ideas quickly, but I needed to evaluate every suggestion against the rubric requirements. The AI's first draft of the scoring function rewarded high energy unconditionally (higher is better) rather than measuring proximity to a target — a subtle but important difference that would have made the system useless for chill-music fans. Reading the output carefully and testing multiple profiles was the only way to catch that.
