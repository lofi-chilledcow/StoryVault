import os
import random
from datetime import datetime

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8001")

mcp = FastMCP("StoryVault")

TEMPLATES = {
    "tech": "Problem → Solution → Lesson learned",
    "work": "Scene → Challenge → What you'd do differently",
    "life": "Emotional hook → Story → How it changed you",
    "fun":  "Funny scene → What went wrong → Resolution",
}


# ---------------------------------------------------------------------------
# Tool 1: get_writing_challenge
# ---------------------------------------------------------------------------

@mcp.tool()
def get_writing_challenge(category: str, words: list[str]) -> str:
    """Get a daily writing challenge using words from VocabularyTracker"""
    chosen = random.sample(words, min(3, len(words))) if words else ["resilient", "deliberate", "clarity"]
    template = TEMPLATES.get(category, TEMPLATES["life"])
    word_bullets = "\n".join(f"  • {w}" for w in chosen)
    return (
        f"📝 Writing Challenge — Category: {category}\n\n"
        f"Use these vocabulary words in your writing:\n{word_bullets}\n\n"
        f"Structure:\n  {template}\n\n"
        f"Target: 150–300 words. Good luck! 🚀"
    )


# ---------------------------------------------------------------------------
# Tool 2: get_template
# ---------------------------------------------------------------------------

@mcp.tool()
def get_template(category: str) -> str:
    """Get a writing template for a specific category"""
    template = TEMPLATES.get(category)
    if not template:
        return f"Unknown category '{category}'. Choose from: tech, work, life, fun."
    return (
        f"Template for [{category}]:\n\n"
        f"  {template}\n\n"
        f"Expand each step into 2–3 sentences. Aim for 150–300 words total."
    )


# ---------------------------------------------------------------------------
# Tool 3: coach_writing
# ---------------------------------------------------------------------------

@mcp.tool()
def coach_writing(content: str, words: list[str] | None = None) -> str:
    """Get AI coaching feedback on your writing"""
    lines = []
    content_lower = content.lower()

    # Vocabulary check
    if words:
        used    = [w for w in words if w.lower() in content_lower]
        missing = [w for w in words if w.lower() not in content_lower]
        if used:
            lines.append(f"✅ Vocabulary used ({len(used)}/{len(words)}): {', '.join(used)}")
        if missing:
            lines.append(f"⚠️  Missing words: {', '.join(missing)} — try weaving them in naturally.")

    # Hook strength — first sentence
    first_sentence = content.strip().split(".")[0].strip()
    if len(first_sentence.split()) < 5:
        lines.append("🪝 Hook: Your opening is very short. Start with action, emotion, or a bold statement.")
    elif "?" in first_sentence or any(w in first_sentence.lower() for w in ["imagine", "the day", "i never", "it was"]):
        lines.append("🪝 Hook: Strong opening — it draws the reader in immediately.")
    else:
        lines.append("🪝 Hook: Decent start. Could be stronger — try opening with a specific moment or feeling.")

    # Word count + structure
    word_count = len(content.split())
    lines.append(f"\n📊 Word count: {word_count}")
    if word_count < 50:
        lines.append("📏 Structure: Too short — develop each section more.")
    elif word_count < 150:
        lines.append("📏 Structure: Good start! Push towards 150–300 words for a complete story.")
    else:
        lines.append("📏 Structure: Good length. Confirm you have a hook, middle, and a lesson/resolution.")

    # Flow
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    if len(paragraphs) < 2:
        lines.append("🔀 Flow: Break into paragraphs — one per story beat improves readability.")
    else:
        lines.append(f"🔀 Flow: {len(paragraphs)} paragraphs — well structured.")

    lines.append("\n💪 Every entry makes you a sharper writer. Keep going!")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Tool 4: check_vocabulary
# ---------------------------------------------------------------------------

@mcp.tool()
def check_vocabulary(content: str, words: list[str]) -> dict:
    """Check which vocabulary words are used in the text"""
    content_lower = content.lower()
    used    = [w for w in words if w.lower() in content_lower]
    missing = [w for w in words if w.lower() not in content_lower]
    score   = round(len(used) / len(words) * 100) if words else 0
    return {"used": used, "missing": missing, "score": score}


# ---------------------------------------------------------------------------
# Tool 5: save_journal
# ---------------------------------------------------------------------------

@mcp.tool()
def save_journal(
    title: str,
    content: str,
    category: str,
    vocab_words: list[str] | None = None,
    score: int | None = None,
) -> str:
    """Save a journal entry to StoryVault"""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "title": title,
        "content": content,
        "category": category,
        "vocab_words": vocab_words or [],
        "score": score,
        "created_at": created_at,
    }
    try:
        resp = httpx.post(f"{API_URL}/api/journals", json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return f"✅ Journal saved!\n  ID: {data['id']}\n  Title: {title}\n  Category: {category}\n  Date: {created_at}"
    except httpx.HTTPStatusError as e:
        return f"❌ Failed to save journal: {e.response.status_code} — {e.response.text}"
    except Exception as e:
        return f"❌ Error: {e}"


# ---------------------------------------------------------------------------
# Tool 6: save_story
# ---------------------------------------------------------------------------

@mcp.tool()
def save_story(
    title: str,
    content: str,
    category: str,
    themes: list[str] | None = None,
) -> str:
    """Save a polished story to StoryVault story bank"""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "title": title,
        "content": content,
        "category": category,
        "themes": themes or [],
        "created_at": created_at,
    }
    try:
        resp = httpx.post(f"{API_URL}/api/stories", json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return f"✅ Story saved!\n  ID: {data['id']}\n  Title: {title}\n  Category: {category}\n  Date: {created_at}"
    except httpx.HTTPStatusError as e:
        return f"❌ Failed to save story: {e.response.status_code} — {e.response.text}"
    except Exception as e:
        return f"❌ Error: {e}"


# ---------------------------------------------------------------------------
# Tool 7: get_stories
# ---------------------------------------------------------------------------

@mcp.tool()
def get_stories(category: str | None = None) -> str:
    """Search and retrieve stories from StoryVault"""
    params = {}
    if category:
        params["category"] = category
    try:
        resp = httpx.get(f"{API_URL}/api/stories", params=params, timeout=10)
        resp.raise_for_status()
        stories = resp.json()
        if not stories:
            return "No stories found."
        lines = [f"📚 {len(stories)} story/stories:\n"]
        for s in stories:
            date       = s.get("created_at", "")[:10]
            themes_str = ", ".join(s.get("themes", [])) or "—"
            lines.append(
                f"• [{s['category']}] {s['title']}\n"
                f"  Themes: {themes_str} | Date: {date}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"❌ Error fetching stories: {e}"


# ---------------------------------------------------------------------------
# Tool 8: get_journals
# ---------------------------------------------------------------------------

@mcp.tool()
def get_journals(category: str | None = None, limit: int = 5) -> str:
    """Get recent journal entries from StoryVault"""
    params: dict = {"limit": limit}
    if category:
        params["category"] = category
    try:
        resp = httpx.get(f"{API_URL}/api/journals", params=params, timeout=10)
        resp.raise_for_status()
        journals = resp.json()
        if not journals:
            return "No journals found."
        lines = [f"📓 {len(journals)} journal(s):\n"]
        for j in journals:
            date      = j.get("created_at", "")[:10]
            words_str = ", ".join(j.get("vocab_words", [])) or "—"
            score_str = f" | Score: {j['score']}" if j.get("score") is not None else ""
            lines.append(
                f"• [{j['category']}] {j['title']}\n"
                f"  Words: {words_str}{score_str} | Date: {date}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"❌ Error fetching journals: {e}"


# ---------------------------------------------------------------------------
# Tool 9: get_stats
# ---------------------------------------------------------------------------

@mcp.tool()
def get_stats() -> str:
    """Get StoryVault writing statistics"""
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        resp = httpx.get(f"{API_URL}/api/stats", params={"date": today}, timeout=10)
        resp.raise_for_status()
        s = resp.json()
        words_used    = s.get("words_used", [])
        words_preview = ", ".join(words_used[:10]) or "none yet"
        ellipsis      = "..." if len(words_used) > 10 else ""
        return (
            f"📊 StoryVault Stats ({today})\n\n"
            f"  📓 Journals : {s['total_journals']}\n"
            f"  📚 Stories  : {s['total_stories']}\n"
            f"  🔥 Streak   : {s['streak_days']} day(s)\n"
            f"  💬 Words    : {len(words_used)} unique\n"
            f"     ({words_preview}{ellipsis})"
        )
    except Exception as e:
        return f"❌ Error fetching stats: {e}"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
