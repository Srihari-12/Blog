
from pydantic import BaseModel

# -------- Input Schemas --------
class CommentCreate(BaseModel):
    content: str
    blog_id: int

# -------- Output Schemas --------
class CommentOut(CommentCreate):
    id: int
    author_email: str

    class Config:
        orm_mode = True
