from datetime import datetime
from pydantic import HttpUrl
from pytube import YouTube, exceptions as pytube_exceptions
from models.links import Link
from core.auth import authenticate_user
from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Query
from bson import ObjectId

link_router = router = APIRouter(tags=["Links"])


@router.get("/links", response_model=list[Link])
async def read_links(
    media_type: str | None = Query(None),
    skip: int = 0,
    limit: int = 20,
    db=Depends(get_db),
):
    """
    Retrieves a list of links from the database based on the specified criteria.

    Returns:
        list[Link]: A list of Link objects that match the specified criteria.
    """
    try:
        query = {}
        if media_type:
            query["media_type"] = media_type

        cursor = db.links_collection.find(query).skip(skip).limit(limit)
        links = await cursor.to_list(length=limit)
        return links
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/links", status_code=status.HTTP_201_CREATED)
async def create_link(
    url: HttpUrl, username: str = Depends(authenticate_user), db=Depends(get_db)
):
    """
    Creates a new link in the database with the given URL and media type.

    Returns:
        Link: The newly created link object.

    Raises:
        HTTPException: If the user is not authenticated, if the URL format is invalid, or if the link already exists.
    """
    url_str = str(url)

    try:
        # Check if link already exists
        existing_link = await db.links_collection.find_one({"url": url_str})
        if existing_link:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Link already exists"
            )

        # Process URL based on type
        if url_str.startswith("https://youtu.be") or url_str.startswith(
            "https://www.youtube.com"
        ):
            try:
                video = YouTube(url_str)
                media_type = "youtube"
                title = video.title
                description = video.description
            except pytube_exceptions.PytubeError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error accessing YouTube video details: {str(e)}",
                )
        elif url_str.startswith("https://spotifyanchor-web.app"):
            media_type = "spotify"
            title = None
            description = None
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL format"
            )

        # Create new link document
        link_doc = {
            "url": url_str.strip(),
            "media_type": media_type,
            "title": title,
            "description": description,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = await db.links_collection.insert_one(link_doc)
        if result.inserted_id:
            return await db.links_collection.find_one({"_id": link_doc["_id"]})
        raise HTTPException(status_code=400, detail="Failed to create link")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/links/{link_id}", response_model=Link)
async def update_link(
    link_id: str,
    url: HttpUrl,
    username: str = Depends(authenticate_user),
    db=Depends(get_db),
):
    """
    Updates the URL of a link in the database.

    Parameters:
        link_id (str): The ID of the link to update.
        url (HttpUrl): The new URL for the link.
        username (str, optional): The username of the authenticated user. Defaults to the result of the `authenticate_user` dependency.
        db (Session, optional): The database session. Defaults to the result of the `get_db` dependency.

    Returns:
        Link: The updated link object.

    Raises:
        HTTPException: If the user is not authenticated, if the link does not exist, or if the URL format is invalid.
    """
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )

    try:
        url_str = str(url)

        # Determine media type
        if url_str.startswith("https://youtu.be"):
            media_type = "youtube"
        elif url_str.startswith("https://spotifyanchor-web.app"):
            media_type = "spotify"
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL format"
            )

        # Update the document
        update_data = {
            "url": url_str,
            "media_type": media_type,
            "updated_at": datetime.utcnow(),
        }

        result = await db.links_collection.update_one(
            {"_id": ObjectId(link_id)}, {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
            )

        return await db.links_collection.find_one({"_id": link_id})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(
    link_id: str, username: str = Depends(authenticate_user), db=Depends(get_db)
):
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )

    try:
        result = await db.links_collection.delete_one({"_id": ObjectId(link_id)})

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
            )

        return {"link_id": link_id, "message": "Link deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
