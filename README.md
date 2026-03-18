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

## Terminal Output — All Profiles

### Profile 1: High-Energy Pop Fan

```
Loaded songs: 22

============================================================
  Profile 1: High-Energy Pop Fan
============================================================

  #1  Sunrise City — Neon Echo
       Genre: pop | Mood: happy | Energy: 0.82
       Score: 5.86
       Why:   genre match (+2.0); mood match (+1.5); energy similarity (+0.97); valence similarity (+0.79); danceability similarity (+0.59)

  #2  Shape of You — Ed Sheeran
       Genre: pop | Mood: dancey | Energy: 0.85
       Score: 4.32
       Why:   genre match (+2.0); energy similarity (+1.00); valence similarity (+0.74); danceability similarity (+0.59)

  #3  Gym Hero — Max Pulse
       Genre: pop | Mood: intense | Energy: 0.93
       Score: 4.21
       Why:   genre match (+2.0); energy similarity (+0.92); valence similarity (+0.74); danceability similarity (+0.55)

  #4  Rooftop Lights — Indigo Parade
       Genre: indie pop | Mood: happy | Energy: 0.76
       Score: 3.77
       Why:   mood match (+1.5); energy similarity (+0.91); valence similarity (+0.77); danceability similarity (+0.59)

  #5  Despacito — Luis Fonsi
       Genre: latin pop | Mood: romantic | Energy: 0.82
       Score: 2.27
       Why:   energy similarity (+0.97); valence similarity (+0.75); danceability similarity (+0.55)
```

**Why did *Sunrise City* rank #1?** It is the only song in the catalog that matches on both genre (`pop`) AND mood (`happy`). That alone earns +3.5 points before any numerical features are compared — more than the maximum any energy/valence/danceability score can contribute. No other pop song in the catalog has `mood: happy`, so it is effectively unreachable by competitors.

**Why does *Gym Hero* appear at #3 despite having `mood: intense`?** The +2.0 genre bonus for `pop` puts it ahead of *Rooftop Lights* (which matches `mood: happy` but not genre). This is the filter bubble in action — a pop song with the wrong mood still beats a non-pop song with the right mood.

---

### Profile 2: Chill Lofi Listener

```
============================================================
  Profile 2: Chill Lofi Listener
============================================================

  #1  Library Rain — Paper Lanterns
       Genre: lofi | Mood: chill | Energy: 0.35
       Score: 6.35
       Why:   genre match (+2.0); mood match (+1.5); energy similarity (+0.97); valence similarity (+0.78); danceability similarity (+0.60); acoustic match (+0.5)

  #2  Midnight Coding — LoRoom
       Genre: lofi | Mood: chill | Energy: 0.42
       Score: 6.32
       Why:   genre match (+2.0); mood match (+1.5); energy similarity (+0.96); valence similarity (+0.78); danceability similarity (+0.58); acoustic match (+0.5)

  #3  Focus Flow — LoRoom
       Genre: lofi | Mood: focused | Energy: 0.4
       Score: 4.86
       Why:   genre match (+2.0); energy similarity (+0.98); valence similarity (+0.79); danceability similarity (+0.59); acoustic match (+0.5)

  #4  Spacewalk Thoughts — Orbit Bloom
       Genre: ambient | Mood: chill | Energy: 0.28
       Score: 4.14
       Why:   mood match (+1.5); energy similarity (+0.90); valence similarity (+0.74); danceability similarity (+0.50); acoustic match (+0.5)

  #5  Coffee Shop Stories — Slow Stereo
       Genre: jazz | Mood: relaxed | Energy: 0.37
       Score: 2.76
       Why:   energy similarity (+0.99); valence similarity (+0.70); danceability similarity (+0.58); acoustic match (+0.5)
```

---

### Profile 3: Deep Intense Rock Fan

```
============================================================
  Profile 3: Deep Intense Rock Fan
============================================================

  #1  Storm Runner — Voltline
       Genre: rock | Mood: intense | Energy: 0.91
       Score: 5.76
       Why:   genre match (+2.0); mood match (+1.5); energy similarity (+0.99); valence similarity (+0.74); danceability similarity (+0.53)

  #2  Enter Sandman — Metallica
       Genre: metal | Mood: intense | Energy: 0.97
       Score: 3.73
       Why:   mood match (+1.5); energy similarity (+0.95); valence similarity (+0.74); danceability similarity (+0.54)

  #3  Lose Yourself — Eminem
       Genre: hip hop | Mood: intense | Energy: 0.95
       Score: 3.69
       Why:   mood match (+1.5); energy similarity (+0.97); valence similarity (+0.74); danceability similarity (+0.48)

  #4  Gym Hero — Max Pulse
       Genre: pop | Mood: intense | Energy: 0.93
       Score: 3.40
       Why:   mood match (+1.5); energy similarity (+0.99); valence similarity (+0.50); danceability similarity (+0.40)

  #5  Night Drive Loop — Neon Echo
       Genre: synthwave | Mood: moody | Energy: 0.75
       Score: 2.05
       Why:   energy similarity (+0.83); valence similarity (+0.73); danceability similarity (+0.49)
```

**Surprise:** *Gym Hero* (pop, intense) appears at #4 for a rock fan because `mood: intense` earns +1.5 points regardless of genre. Mood acts as a cross-genre bridge. A pop song with the right intensity gets recommended to a rock fan, which could feel wrong but is mathematically defensible.

---

### Profile 4: Edge Case — Moody High-Energy (conflicted)

```
============================================================
  Profile 4: Edge Case — Moody High-Energy (conflicted)
============================================================

  #1  Night Drive Loop — Neon Echo
       Genre: synthwave | Mood: moody | Energy: 0.75
       Score: 5.54
       Why:   genre match (+2.0); mood match (+1.5); energy similarity (+0.85); valence similarity (+0.61); danceability similarity (+0.58)

  #2  Bad Guy — Billie Eilish
       Genre: alt pop | Mood: moody | Energy: 0.56
       Score: 3.47
       Why:   mood match (+1.5); energy similarity (+0.66); valence similarity (+0.74); danceability similarity (+0.57)

  #3  Storm Runner — Voltline
       Genre: rock | Mood: intense | Energy: 0.91
       Score: 2.18
       Why:   energy similarity (+0.99); valence similarity (+0.62); danceability similarity (+0.58)

  #4  Enter Sandman — Metallica
       Genre: metal | Mood: intense | Energy: 0.97
       Score: 2.12
       Why:   energy similarity (+0.93); valence similarity (+0.74); danceability similarity (+0.45)

  #5  Blinding Lights — The Weeknd
       Genre: synthpop | Mood: nostalgic | Energy: 0.88
       Score: 1.98
       Why:   energy similarity (+0.98); valence similarity (+0.43); danceability similarity (+0.57)
```

**Observation:** The catalog has no truly "high-energy moody" songs (energy > 0.85 AND mood = moody). *Night Drive Loop* wins as the best compromise — it matches both genre and mood but its energy of 0.75 falls 0.15 below the target of 0.90. The system handled the conflict gracefully rather than failing.

---

## Experiments Tried

### Experiment 1 — Weight shift: genre halved (2.0→1.0), energy doubled (1.0→2.0)

```
Weight-Shift Experiment — Pop Fan (genre=1.0, energy=2.0)
============================================================
#1  Sunrise City — Neon Echo
     Genre: pop | Mood: happy | Energy: 0.82  |  Score: 5.83

#2  Rooftop Lights — Indigo Parade
     Genre: indie pop | Mood: happy | Energy: 0.76  |  Score: 4.68

#3  Shape of You — Ed Sheeran
     Genre: pop | Mood: dancey | Energy: 0.85  |  Score: 4.32

#4  Gym Hero — Max Pulse
     Genre: pop | Mood: intense | Energy: 0.93  |  Score: 4.13

#5  Despacito — Luis Fonsi
     Genre: latin pop | Mood: romantic | Energy: 0.82  |  Score: 3.24
```

Key change: *Rooftop Lights* (indie pop, happy) jumped from #4 to #2, displacing *Shape of You*. With a weaker genre gate, "indie pop" no longer loses to "pop" by default — the mood match (+1.5) and tight energy proximity pushed it ahead. The results became more genre-diverse but the top-1 stayed the same because *Sunrise City* still won on mood + energy combined.

### Experiment 2 — Feature removal: mood scoring commented out

Without the +1.5 mood bonus, the chill lofi profile ranked *Focus Flow* (#1) above *Library Rain* and *Midnight Coding* — which share both genre AND mood with the user — because *Focus Flow*'s energy (0.40) was marginally closer to the target (0.38). A difference of 0.02 in energy gap decided first place. This confirmed mood is a crucial differentiator: removing it makes the system sensitive to tiny numerical differences that don't reflect real listening preferences.

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
