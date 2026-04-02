"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}

    print(f"\nUser profile: genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
          f"energy={user_prefs['energy']}, likes_acoustic={user_prefs['likes_acoustic']}")
    print("\n" + "=" * 52)
    print(f"  Top {5} Recommendations")
    print("=" * 52)

    recommendations = recommend_songs(user_prefs, songs, k=5)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} — {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Why   : {explanation}")

    print("\n" + "=" * 52)


if __name__ == "__main__":
    main()
