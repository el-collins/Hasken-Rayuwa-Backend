import datetime
from uuid import UUID, uuid4
from sqlmodel import Session
from models.blogs import Blog

# from core.auth import authenticate_user
from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

blog_router = router = APIRouter(tags=["Blogs"])


@router.get("/blogs", response_model=list[Blog])
def read_blogs(
    # visibility: str | None = Query(None),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
) -> list[Blog]:
    """
    Retrieves a list of blogs from the database based on the specified criteria.

    Returns:
        list[Blog]: A list of Blog objects that match the specified criteria.
    """
    query = db.query(Blog)
    # if visibility:
    #     query = query.filter(Blog.visibility == visibility)
    blogs = query.offset(skip).limit(limit).all()

    return blogs


# Get blog by ID
@router.get("/blogs/{blog_id}", response_model=Blog)
def read_blog(blog_id: UUID, db: Session = Depends(get_db)) -> Blog:
    """
    Retrieves a single blog entry from the database based on the specified ID.
    """
    blog = db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    return blog


# Create Blog
@router.post("/blogs", status_code=status.HTTP_201_CREATED, response_model=Blog)
def create_blog(
    title: str,
    author: str,
    content: str,
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
        date=datetime.datetime.now(datetime.timezone.utc),
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@router.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(
    blog_id: UUID,
    updates: Dict[str, Any],
    db: Session = Depends(get_db),
    # username: str = Depends(authenticate_user)
) -> Blog:
    """
    Updates one or more fields of a blog entry in the database.

    Args:
        blog_id (UUID): The ID of the blog to update.
        updates (Dict[str, Any]): A dictionary containing the fields to update and their new values.
        db (Session): The database session.

    Returns:
        Blog: The updated blog entry.

    Raises:
        HTTPException: If the blog is not found or if there's an attempt to update a non-existent field.
    """
    blog = db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    valid_fields = {"title", "author", "content"}
    for field, value in updates.items():
        if field not in valid_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid field: {field}",
            )
        setattr(blog, field, value)

    db.add(blog)
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}
