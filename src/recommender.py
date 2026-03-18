import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio/metadata attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences for recommendation matching."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP recommender that scores and ranks Song objects against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user profile."""
        scored = []
        for song in self.songs:
            score = self._score(user, song)
            scored.append((score, song))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        reasons = []
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append(f"genre match ({song.genre})")
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append(f"mood match ({song.mood})")
        energy_gap = abs(song.energy - user.target_energy)
        if energy_gap <= 0.15:
            reasons.append(f"energy close to target (gap={energy_gap:.2f})")
        if user.likes_acoustic and song.acousticness >= 0.6:
            reasons.append(f"acoustic feel (acousticness={song.acousticness:.2f})")
        if not reasons:
            reasons.append("closest match in catalog")
        return "; ".join(reasons)

    def _score(self, user: UserProfile, song: Song) -> float:
        """Compute a weighted score for a single song against a user profile."""
        score = 0.0
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.5
        energy_similarity = 1.0 - abs(song.energy - user.target_energy)
        score += energy_similarity * 1.0
        if user.likes_acoustic:
            score += song.acousticness * 0.5
        return score


# ---------------------------------------------------------------------------
# Functional API (used by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Score a single song against user preferences and return (score, reasons_string).

    Scoring recipe:
      +2.0  genre match
      +1.5  mood match
      +1.0  × energy similarity  (1 - |song_energy - target_energy|)
      +0.8  × valence similarity
      +0.6  × danceability similarity
      +0.5  bonus if user likes_acoustic and song acousticness >= 0.6
    """
    score = 0.0
    reasons = []

    weights = user_prefs.get("feature_weights", {})

    genre_w = weights.get("genre", 2.0)
    if song["genre"].lower() == user_prefs.get("genre", user_prefs.get("favorite_genre", "")).lower():
        score += genre_w
        reasons.append(f"genre match (+{genre_w})")

    mood_w = weights.get("mood", 1.5)
    if song["mood"].lower() == user_prefs.get("mood", user_prefs.get("favorite_mood", "")).lower():
        score += mood_w
        reasons.append(f"mood match (+{mood_w})")

    target_energy = float(user_prefs.get("energy", user_prefs.get("target_energy", 0.5)))
    energy_w = weights.get("energy", 1.0)
    energy_sim = 1.0 - abs(song["energy"] - target_energy)
    energy_pts = round(energy_sim * energy_w, 3)
    score += energy_pts
    reasons.append(f"energy similarity (+{energy_pts:.2f})")

    if "target_valence" in user_prefs:
        valence_w = weights.get("valence", 0.8)
        valence_sim = 1.0 - abs(song["valence"] - float(user_prefs["target_valence"]))
        valence_pts = round(valence_sim * valence_w, 3)
        score += valence_pts
        reasons.append(f"valence similarity (+{valence_pts:.2f})")

    if "target_danceability" in user_prefs:
        dance_w = weights.get("danceability", 0.6)
        dance_sim = 1.0 - abs(song["danceability"] - float(user_prefs["target_danceability"]))
        dance_pts = round(dance_sim * dance_w, 3)
        score += dance_pts
        reasons.append(f"danceability similarity (+{dance_pts:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic and song["acousticness"] >= 0.6:
        acoustic_w = weights.get("acousticness", 0.5)
        score += acoustic_w
        reasons.append(f"acoustic match (+{acoustic_w})")

    return round(score, 3), "; ".join(reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


# ---------------------------------------------------------------------------
# Default taste profile
# ---------------------------------------------------------------------------

user_taste_profile = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_tempo_bpm": 80.0,
    "target_valence": 0.60,
    "target_danceability": 0.60,
    "likes_acoustic": True,
    "favorite_artists": ["LoRoom", "Paper Lanterns"],
    "feature_weights": {
        "genre": 2.0,
        "mood": 1.5,
        "energy": 1.0,
        "tempo": 0.8,
        "valence": 0.8,
        "danceability": 0.6,
        "acousticness": 0.5,
    },
}


def get_user_profile_dict() -> Dict:
    """Return the default taste profile as a plain dictionary."""
    return dict(user_taste_profile)


def user_dict_to_dataclass(profile: Dict) -> UserProfile:
    """Convert a taste-profile dict into the UserProfile dataclass."""
    return UserProfile(
        favorite_genre=profile.get("favorite_genre", ""),
        favorite_mood=profile.get("favorite_mood", ""),
        target_energy=float(profile.get("target_energy", 0.5)),
        likes_acoustic=bool(profile.get("likes_acoustic", False)),
    )
