"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(title: str, recommendations: list) -> None:
    """Print a formatted block of recommendations to the terminal."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"       Score: {score:.2f}")
        print(f"       Why:   {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"\nLoaded songs: {len(songs)}")

    # ---- Profile 1: High-Energy Pop Fan ----
    pop_profile = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "target_valence": 0.85,
        "target_danceability": 0.80,
        "likes_acoustic": False,
        "feature_weights": {
            "genre": 2.0,
            "mood": 1.5,
            "energy": 1.0,
            "valence": 0.8,
            "danceability": 0.6,
        },
    }

    # ---- Profile 2: Chill Lofi Listener ----
    lofi_profile = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "target_valence": 0.58,
        "target_danceability": 0.58,
        "likes_acoustic": True,
        "feature_weights": {
            "genre": 2.0,
            "mood": 1.5,
            "energy": 1.0,
            "valence": 0.8,
            "danceability": 0.6,
            "acousticness": 0.5,
        },
    }

    # ---- Profile 3: Deep Intense Rock Fan ----
    rock_profile = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "target_valence": 0.40,
        "target_danceability": 0.55,
        "likes_acoustic": False,
        "feature_weights": {
            "genre": 2.0,
            "mood": 1.5,
            "energy": 1.0,
            "valence": 0.8,
            "danceability": 0.6,
        },
    }

    # ---- Edge-case Profile: Conflicting Preferences (sad + high energy) ----
    conflicted_profile = {
        "genre": "synthwave",
        "mood": "moody",
        "energy": 0.90,
        "target_valence": 0.25,
        "target_danceability": 0.70,
        "likes_acoustic": False,
        "feature_weights": {
            "genre": 2.0,
            "mood": 1.5,
            "energy": 1.0,
            "valence": 0.8,
            "danceability": 0.6,
        },
    }

    profiles = [
        ("Profile 1: High-Energy Pop Fan", pop_profile),
        ("Profile 2: Chill Lofi Listener", lofi_profile),
        ("Profile 3: Deep Intense Rock Fan", rock_profile),
        ("Profile 4: Edge Case — Moody High-Energy (conflicted)", conflicted_profile),
    ]

    for label, profile in profiles:
        recs = recommend_songs(profile, songs, k=5)
        print_recommendations(label, recs)

    print()


if __name__ == "__main__":
    main()
