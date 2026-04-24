from pydantic import BaseModel


class JournalCreate(BaseModel):
    title: str
    content: str
    category: str
    vocab_words: list[str] = []
    score: int | None = None
    created_at: str | None = None


class Journal(JournalCreate):
    id: str


class StoryCreate(BaseModel):
    title: str
    content: str
    category: str
    themes: list[str] = []
    created_at: str | None = None


class Story(StoryCreate):
    id: str


class Stats(BaseModel):
    total_journals: int
    total_stories: int
    streak_days: int
    words_used: list[str]
