# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is a classroom demonstration of content-based music recommendation. It is designed to suggest 3–5 songs from a small catalog based on a user's preferred genre, mood, energy level, valence, and danceability. The system is intended for educational exploration of how weighted-score algorithms translate user preferences into ranked results. It is **not** intended for deployment to real users, commercial use, or any context where recommendation quality materially affects listening experience or revenue.

---

## 3. How the Model Works

Imagine you tell a friend your favorite type of music: "I love chill lofi, something low-energy with an acoustic feel." Your friend then flips through a stack of albums and gives each one a score based on how well it matches what you said.

VibeFinder does exactly that. For every song in the catalog it checks:

- Does the genre match your favorite genre? If yes, +2 points.
- Does the mood match your favorite mood? If yes, +1.5 points.
- How close is the song's energy to your target? A perfect match adds +1 point; a big mismatch adds almost nothing.
- How close are the valence (brightness) and danceability to your targets? Each contributes up to +0.8 or +0.6 points.
- If you like acoustic music and the song is very acoustic, add +0.5 points.

After every song gets a score, the list is sorted from highest to lowest and the top results are returned along with a plain-English explanation of why each song was chosen.

There is no machine learning involved. The weights (2.0, 1.5, 1.0, etc.) were hand-designed and do not change based on feedback.

---

## 4. Data

- **Catalog size:** 22 songs
- **Source:** 10 starter songs provided in the original repo + 12 additional songs added to increase genre and mood diversity
- **Genres represented:** pop, lofi, rock, metal, jazz, ambient, synthwave, hip hop, edm, country, reggae, folk, blues, synthpop, latin pop, k-pop, alt pop, indie pop
- **Moods represented:** happy, chill, intense, relaxed, moody, focused, nostalgic, romantic, joyful, dancey, soulful, mellow, party
- **Audio features per song:** energy (0–1), tempo_bpm, valence (0–1), danceability (0–1), acousticness (0–1)
- **Limitations of the data:** The catalog is extremely small. Several genres have only one representative song, meaning a genre match is essentially deterministic. The energy and valence values were estimated, not measured from actual audio analysis tools like the Spotify Audio Features API. The dataset skews toward Western popular music; non-Western genres are underrepresented.

---

## 5. Strengths

- **Transparent and explainable** — every recommendation comes with a plain-English reason string showing exactly which features matched and by how much.
- **Works well for users with strong genre preferences** — profiles like "chill lofi" or "high-energy pop" get very consistent, sensible top results.
- **Handles edge cases gracefully** — a conflicted profile (high energy + moody) still converges on the best available compromise rather than failing.
- **No training data required** — the scoring is fully rule-based, so it works immediately on any new user profile without any learning period.

---

## 6. Limitations and Bias

**Genre dominance (filter bubble).** The +2.0 genre bonus is the largest single score component. A song that perfectly matches mood, energy, valence, and danceability but is the wrong genre will almost never beat a genre-match song. This means users are unlikely to discover music outside their stated preferred genre — exactly the filter bubble problem real platforms struggle with.

**Sparse catalog amplifies bias.** With only one or two songs per genre, a genre match is near-deterministic. A pop fan will see the same 3–4 pop songs at the top of every recommendation list regardless of other preferences.

**Exact-string categorical matching.** "indie pop" and "pop" are treated as completely different genres even though they overlap. A user who likes "pop" will not match songs tagged "indie pop" or "latin pop," missing potentially relevant songs.

**No diversity enforcement.** The algorithm optimizes for the single best score. If two songs are nearly identical in attributes, both appear in the top results with no effort to surface variety.

**Energy proximity is symmetric.** The formula `1 - |energy_gap|` treats being 0.2 above target the same as being 0.2 below target. In practice, users who want "chill" music are usually more annoyed by an accidentally high-energy song than by one that's slightly lower than expected.

---

## 7. Evaluation

Four user profiles were tested:

| Profile | Key preferences | Top result | Matched intuition? |
|---|---|---|---|
| High-Energy Pop Fan | genre=pop, mood=happy, energy=0.85 | *Sunrise City* (pop, happy, 0.82 energy) | Yes — genre + mood + energy all matched |
| Chill Lofi Listener | genre=lofi, mood=chill, energy=0.38 | *Library Rain* (lofi, chill, 0.35 energy) | Yes — near-perfect match on all features |
| Deep Intense Rock Fan | genre=rock, mood=intense, energy=0.92 | *Storm Runner* (rock, intense, 0.91 energy) | Yes — only one rock song in catalog |
| Edge Case: Moody + High-Energy | genre=synthwave, mood=moody, energy=0.90 | *Night Drive Loop* (synthwave, moody, 0.75 energy) | Reasonable — best available compromise |

**Surprises:**
- *Gym Hero* (pop, intense) kept appearing in the pop fan's top 3 even though the target mood was "happy," not "intense." The genre match (+2.0) outweighed the mood mismatch. This revealed that the genre bonus can overshadow mood mismatches.
- The rock fan's #2 and #3 picks were from metal and hip-hop respectively — neither is "rock" — but both had the "intense" mood match (+1.5). This was actually reasonable and showed mood can substitute for genre when catalog coverage is thin.

**Weight-shift experiment:** Halving the genre weight (2.0 → 1.0) and doubling the energy weight (1.0 → 2.0) produced more genre-diverse results but made the recommendations feel less cohesive. The pop fan started receiving EDM and synthpop tracks ahead of some pop songs.

---

## 8. Future Work

1. **Add collaborative filtering as a second signal.** Combine content-based scores with "users who liked X also liked Y" signals to break genre filter bubbles and enable serendipitous discovery.
2. **Enforce diversity in top-k results.** After scoring, apply a diversity penalty to prevent the same genre or artist from dominating the entire top-5 list.
3. **Learn weights from feedback.** Replace hand-tuned weights with a simple gradient descent loop that adjusts weights based on user thumbs-up / thumbs-down signals, making the system adaptive.
4. **Use real audio features.** Integrate the Spotify Audio Features API (or a local audio analysis library) to replace hand-estimated values with accurate measurements.
5. **Asymmetric proximity scoring.** Treat exceeding a target differently from falling below it — relevant for features like energy where users have directional preferences.

---

## 9. Personal Reflection

The most surprising thing about building VibeFinder was how quickly one design decision — the +2.0 genre bonus — ended up controlling most of the output. I expected the algorithm to balance all features roughly equally, but in practice genre acted as a hard filter. That taught me that "bias" in a recommender system isn't always a subtle statistical artifact; sometimes it's a deliberate engineering choice that just looks neutral because it's expressed as a number.

Working with AI assistance accelerated the project significantly, especially for boilerplate code and generating diverse song data. However, I had to catch and correct a scoring mistake where the AI's first draft rewarded higher energy unconditionally instead of measuring proximity to the user's target. That single bug would have made the system recommend high-energy tracks to everyone, regardless of their preference. Testing with multiple profiles — including the "chill lofi" profile — was what exposed it. This confirmed a lesson I'll carry forward: AI-generated code needs to be verified against concrete test cases, not just read and accepted.

The most interesting conceptual shift for me was understanding that a recommendation system doesn't need to understand music to seem "smart." VibeFinder has no idea what a guitar sounds like or what makes a song feel nostalgic. It just compares numbers. Yet for a user who gets back *Library Rain* and *Midnight Coding* as their top two lofi recommendations, it probably feels like the system "gets" them. That gap between what the system is actually doing and what users perceive it to be doing is exactly why model cards and transparent explanations matter.
