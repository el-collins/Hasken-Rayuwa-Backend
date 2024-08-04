import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Session
from models.blogs import Blog
# from core.auth import authenticate_user
from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Query

blog_router = router = APIRouter(tags=['Blogs'])


@router.get('/blogs', response_model=list[Blog])
def read_blogs(
    visibility: str | None = Query(None),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)) -> list[Blog]:
    
    """
    Retrieves a list of blogs from the database based on the specified criteria.

    Returns:
        list[Blog]: A list of Blog objects that match the specified criteria.
    """
    query = db.query(Blog)
    if visibility:
        query = query.filter(Blog.visibility == visibility)
    blogs = query.offset(skip).limit(limit).all()
    
    return blogs




# Create Blog
@router.post("/blogs", status_code=status.HTTP_201_CREATED, response_model=Blog)
def create_blog(
    title: str,
    author: str,
    content: str,
    visibility: Optional[str] = "active",
    db: Session = Depends(get_db),
    # username: str = Depends(authenticate_user)
) -> Blog:
    """
    Creates a new blog entry in the database.
    """
    blog = Blog(
        id=uuid4(),
        title=title,
        author=author,
        content=content,
        visibility=visibility,
        date=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


# Update Blog
@blog_router.put("/blogs/{blog_id}")
def update_blog(
    blog_id: UUID,
    title: Optional[str] = None,
    content: Optional[str] = None,
    visibility: Optional[str] = None,
    db: Session = Depends(get_db),
    # username: str = Depends(authenticate_user)
) -> Blog:
    """
    Updates an existing blog entry in the database.
    """
    blog = db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    if title:
        blog.title = title
    if content:
        blog.content = content
    if visibility:
        blog.visibility = visibility

    db.commit()
    db.refresh(blog)
    return blog

# Delete Blog
@blog_router.delete("/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    blog_id: UUID,
    db: Session = Depends(get_db),
    # username: str = Depends(authenticate_user)
):
    """
    Deletes a blog entry from the database.
    """
    blog = db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}