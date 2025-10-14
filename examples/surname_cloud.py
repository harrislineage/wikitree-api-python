"""
Example App: Surname Cloud from Ancestors
-----------------------------------------

Demonstrates how to use the WikiTree API client to:
  - Authenticate with a WikiTree account
  - Retrieve multiple generations of ancestors
  - Extract their LastNameAtBirth (LNAB)
  - Visualize surname frequency as a word cloud
"""

import os
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wikitree_api import WikiTreeSession, WikiTreeAPIError

def build_surname_cloud(wikitree_id: str, email: str, password: str, depth: int = 5):
    wt = WikiTreeSession()

    print("Authenticating with WikiTree...")
    try:
        wt.authenticate(email=email, password=password)
        print(f"Authenticated as {wt.user_name}")
    except WikiTreeAPIError as e:
        print("Login failed:", e)
        return

    print(f"Fetching up to {depth} generations of ancestors for {wikitree_id}...")
    try:
        data = wt.getAncestors(
            key=wikitree_id,
            depth=depth,
            fields="Id,Name,LastNameAtBirth"
        )
    except WikiTreeAPIError as e:
        print("API error:", e)
        return

    if isinstance(data, list):
        data = data[0] # pyright: ignore[reportArgumentType]
    
    ancestors = data.get("ancestors", [])
    if not ancestors:
        print("No ancestor data returned.")
        return

    # Count LNAB frequency
    surnames = [a.get("LastNameAtBirth", "").strip() for a in ancestors if a.get("LastNameAtBirth")]
    counts = Counter(surnames)

    if not counts:
        print("No surnames found.")
        return

    print(f"Found {len(counts)} unique surnames among {len(ancestors)} ancestors.")

    # Generate and display the word cloud
    wc = WordCloud(
        width=1000,
        height=600,
        background_color="white",
        colormap="plasma",
        prefer_horizontal=0.9
    ).generate_from_frequencies(counts)

    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Surname Cloud for Ancestors of {wikitree_id}", fontsize=16)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Set credentials via environment variables for convenience
    email = os.getenv("WIKITREE_EMAIL") or input("WikiTree Email: ")
    password = os.getenv("WIKITREE_PASSWORD") or input("WikiTree Password: ")
    key = input("Enter a WikiTree ID (e.g., Clemens-1): ") or "Clemens-1"

    build_surname_cloud(key, email, password, depth=5)
