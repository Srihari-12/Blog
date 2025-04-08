from fastapi import APIRouter, HTTPException, Depends, Security, Query
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy import or_
from Backend.models.blog_model import Blog, Comment
from Backend.models.user_model import User
from Backend.schemas.blog import  BlogCreate, BlogUpdate, BlogOut, CommentCreate, CommentOut, CommentUpdate
from Backend.util.jwt_utils import verify_token
from Backend.util.get_db import get_db

router = APIRouter()

# Use APIKeyHeader for cleaner Swagger auth
auth_header = APIKeyHeader(name="Authorization")

def get_current_email(token: str = Security(auth_header)) -> str:
    if token.startswith("Bearer "):
        token = token[7:]
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return email

@router.post("/blogs", response_model=BlogOut)
def create_blog(blog: BlogCreate, db: Session = Depends(get_db), email: str = Depends(get_current_email)):
    new_blog = Blog(**blog.dict(), author_email=email)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/blogs", response_model=list[BlogOut])
def get_blogs(skip: int = 0, limit: int = 10, search: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(Blog)
    if search:
        query = query.filter(or_(Blog.title.contains(search), Blog.content.contains(search)))
    return query.offset(skip).limit(limit).all()

@router.get("/blogs/{blog_id}", response_model=BlogOut)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter_by(id=blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/blogs/{blog_id}", response_model=BlogOut)
def update_blog(blog_id: int, blog: BlogUpdate, db: Session = Depends(get_db), email: str = Depends(get_current_email)):
    existing_blog = db.query(Blog).filter_by(id=blog_id, author_email=email).first()
    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found or you're not the author")

    for key, value in blog.dict(exclude_unset=True).items():
        setattr(existing_blog, key, value)

    db.commit()
    db.refresh(existing_blog)
    return existing_blog

@router.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db), email: str = Depends(get_current_email)):
    existing_blog = db.query(Blog).filter_by(id=blog_id, author_email=email).first()
    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found or you're not the author")

    db.delete(existing_blog)
    db.commit()
    return {"message": "Blog deleted successfully"}

@router.post("/blogs/{blog_id}/comments", response_model=CommentOut)
def create_comment(blog_id: int, comment: CommentCreate, db: Session = Depends(get_db), email: str = Depends(get_current_email)):
    blog = db.query(Blog).filter_by(id=blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    new_comment = Comment(**comment.dict(), blog_id=blog_id, author_email=email)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@router.get("/blogs/{blog_id}/comments", response_model=list[CommentOut])
def get_comments_for_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter_by(id=blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return db.query(Comment).filter_by(blog_id=blog_id).all()

@router.put("/comments/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db), email: str = Depends(get_current_email)):
    existing_comment = db.query(Comment).filter_by(id=comment_id, author_email=email).first()
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found or you're not the author")

    for key, value in comment.dict(exclude_unset=True).items():
        setattr(existing_comment, key, value)

    db.commit()
    db.refresh(existing_comment)
    return existing_comment

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), email: str = Depends(get_current_email)):
    existing_comment = db.query(Comment).filter_by(id=comment_id, author_email=email).first()
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found or you're not the author")

    db.delete(existing_comment)
    db.commit()
    return {"message": "Comment deleted successfully"}

@router.get("/my-blogs", response_model=list[BlogOut])
def get_my_blogs(db: Session = Depends(get_db), email: str = Depends(get_current_email)):
    return db.query(Blog).filter_by(author_email=email).all()