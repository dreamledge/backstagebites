import json
import sys

RAW_PATH = "data/wall-of-fame-raw.json"
OUT_PATH = "data/wall-of-fame.json"

try:
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    print(f"Could not read {RAW_PATH}")
    sys.exit(0)

posts = []

tweets = raw if isinstance(raw, list) else raw.get("data", raw.get("tweets", []))

for t in tweets:
    if isinstance(t, dict):
        text = t.get("text") or t.get("content") or t.get("full_text") or ""
        user = t.get("user") or {}
        username = user.get("screen_name") or user.get("username") or user.get("name") or "anonymous"
        if username and not username.startswith("@"):
            username = "@" + username
        likes = int(t.get("favorite_count", t.get("likes", 0)))
        retweets = int(t.get("retweet_count", t.get("retweets", 0)))
        date = (t.get("created_at") or "").split("T")[0]
        if not date:
            date = "2026-01-01"
        posts.append({
            "platform": "twitter",
            "username": username,
            "content": text,
            "likes": likes,
            "retweets": retweets,
            "date": date,
            "url": t.get("url") or t.get("permalink") or ""
        })

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

print(f"Saved {len(posts)} posts to {OUT_PATH}")
