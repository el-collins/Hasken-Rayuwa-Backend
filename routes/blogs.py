from datetime import datetime, timezone
from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from bson import ObjectId

blog_router = router = APIRouter(tags=["Blogs"])


@router.get("/blogs")
async def read_blogs(
    # visibility: str | None = Query(None),
    skip: int = 0,
    limit: int = 20,
    db=Depends(get_db),
):
    """
    Retrieves a list of blogs from the database based on the specified criteria.
    """
    try:
        cursor = db.blogs_collection.find({}).skip(skip).limit(limit)
        blogs = await cursor.to_list(length=limit)
        return blogs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get blog by ID
@router.get("/blogs/{blog_id}")
async def read_blog(blog_id: str, db=Depends(get_db)):
    """
    Retrieves a single blog entry from the database based on the specified ID.
    """
    try:
        blog = await db.blogs_collection.find_one({"_id": ObjectId(blog_id)})
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
            )
        return blog
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Create Blog
@router.post("/blogs", status_code=status.HTTP_201_CREATED)
async def create_blog(
    title: str,
    author: str,
    content: str,
    db=Depends(get_db),
    # username: str = Depends(authenticate_user)
):
    """
    Creates a new blog entry in the database.
    """
    try:
        blog_doc = {
            "title": title,
            "author": author,
            "content": content,
            "date": datetime.now(timezone.utc),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = await db.blogs_collection.insert_one(blog_doc)
        if result.inserted_id:
            return await db.blogs_collection.find_one({"_id": blog_doc["_id"]})
        raise HTTPException(status_code=400, detail="Failed to create blog")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/blogs/{blog_id}")
async def update_blog(
    blog_id: str,
    updates: Dict[str, Any],
    db=Depends(get_db),
    # username: str = Depends(authenticate_user)
):
    """
    Updates one or more fields of a blog entry in the database.
    """
    try:
        # Verify blog exists
        blog = await db.blogs_collection.find_one({"_id": ObjectId(blog_id)})
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
            )

        # Validate update fields
        valid_fields = {"title", "author", "content"}
        update_data = {}
        for field, value in updates.items():
            if field not in valid_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid field: {field}",
                )
            update_data[field] = value

        # Add updated timestamp
        update_data["updated_at"] = datetime.utcnow()

        # Perform update
        result = await db.blogs_collection.update_one(
            {"_id": ObjectId(blog_id)}, {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Blog update failed")

        return await db.blogs_collection.find_one({"_id": blog_id})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Delete Blog
@blog_router.delete("/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: str,
    db=Depends(get_db),
    # username: str = Depends(authenticate_user)
):
    """
    Deletes a blog entry from the database.
    """
    try:
        result = await db.blogs_collection.delete_one({"_id": ObjectId(blog_id)})

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
            )

        return {"message": "Blog deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
