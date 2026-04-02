import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio attributes."""
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
    """Represents a user's music taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Content-based music recommender that scores and ranks songs for a user."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by weighted score for the given user."""
        scored = sorted(
            self.songs,
            key=lambda song: _score_song_obj(user, song)[0],
            reverse=True,
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        _, reasons = _score_song_obj(user, song)
        return "; ".join(reasons) if reasons else "No strong matches found"


def _score_song_obj(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Score a Song dataclass against a UserProfile, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if song.genre == user.favorite_genre:
        score += 3.0
        reasons.append(f"genre match (+3.0)")

    if song.mood == user.favorite_mood:
        score += 2.0
        reasons.append(f"mood match (+2.0)")

    energy_proximity = (1 - abs(song.energy - user.target_energy)) * 2.0
    score += energy_proximity
    reasons.append(f"energy proximity (+{energy_proximity:.2f})")

    if user.likes_acoustic:
        acoustic_bonus = song.acousticness * 1.0
        score += acoustic_bonus
        reasons.append(f"acoustic bonus (+{acoustic_bonus:.2f})")

    return score, reasons


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song dict against user preference dict, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre", ""):
        score += 3.0
        reasons.append("genre match (+3.0)")

    if song["mood"] == user_prefs.get("mood", ""):
        score += 2.0
        reasons.append("mood match (+2.0)")

    target_energy = user_prefs.get("energy", 0.5)
    energy_proximity = (1 - abs(song["energy"] - target_energy)) * 2.0
    score += energy_proximity
    reasons.append(f"energy proximity (+{energy_proximity:.2f})")

    if user_prefs.get("likes_acoustic", False):
        acoustic_bonus = song["acousticness"] * 1.0
        score += acoustic_bonus
        reasons.append(f"acoustic bonus (+{acoustic_bonus:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs for a user, returning the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
