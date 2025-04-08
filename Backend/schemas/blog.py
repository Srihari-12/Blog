from pydantic import BaseModel

# ---------- Blog ----------
class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass  # Used when creating

class BlogUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class BlogOut(BlogBase):
    id: int
    author_email: str

    class Config:
        orm_mode = True

# ---------- Comment ----------
class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: str | None = None

class CommentOut(CommentCreate):
    id: int
    blog_id: int
    author_email: str

    class Config:
        orm_mode = True
