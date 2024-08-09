from pydantic import HttpUrl
from pytube import YouTube, exceptions as pytube_exceptions
from sqlmodel import Session
from models.links import Link
from core.auth import authenticate_user
from db.database import get_db, get_or_create_entity
from fastapi import APIRouter, Depends, HTTPException, status, Query

link_router = router = APIRouter(tags=['Links'])

@router.get('/links', response_model=list[Link])
def read_links(
    media_type: str | None = Query(None), 
    skip: int = 0, 
    limit: int = 20, 
    db: Session = Depends(get_db)) -> list[Link]:
    
    """
    Retrieves a list of links from the database based on the specified criteria.

    Returns:
        list[Link]: A list of Link objects that match the specified criteria.
    """
    query = db.query(Link)
    if media_type:
        query = query.filter(Link.media_type == media_type)
    links = query.offset(skip).limit(limit).all()
    
    return links


@router.post('/links', status_code=status.HTTP_201_CREATED)
def create_link(
    url: HttpUrl, 
    username: str = Depends(authenticate_user), 
    db: Session = Depends(get_db)
    ) -> Link:
    
    """
    Creates a new link in the database with the given URL and media type.

    Returns:
        Link: The newly created link object.

    Raises:
        HTTPException: If the user is not authenticated, if the URL format is invalid, or if the link already exists.
    """
    url_str = str(url)
    
    if url_str.startswith('https://youtu.be') or url_str.startswith('https://www.youtube.com'):
        try:
            video = YouTube(url_str)
            print(video)
            media_type = 'youtube'
            title = video.title
            description = video.description
        except pytube_exceptions.PytubeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f'Error accessing YouTube video details: {str(e)}'
            )
    elif url_str.startswith('https://spotifyanchor-web.app'):
        media_type = 'spotify'
        title = None
        description = None
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid URL format')

    # Check if the link already exists
    if db.query(Link).filter(Link.url == url_str).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Link already exists')

    link = get_or_create_entity(
        db, 
        Link, 
        url=url_str.strip(), 
        media_type=media_type, 
        title=title, 
        description=description
    )
    
    return link

@router.put('/links/{link_id}', response_model=Link)
def update_link(
    link_id: str, 
    url: HttpUrl, 
    username: str = Depends(authenticate_user), 
    db: Session = Depends(get_db)
) -> Link:
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
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized user"
        )

    link = db.query(Link).filter(Link.id == link_id).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Link not found'
        )

    if url.startswith('https://youtu.be'):
        media_type = 'youtube'
    elif url.startswith('https://spotifyanchor-web.app'):
        media_type = 'spotify'
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Invalid URL format'
        )

    # link.url = str(url)
    # link.media_type = media_type
    # db.commit()
    # db.refresh(link)
    
    # updated_link = 
    get_or_create_entity(
        db,
        Link,
        str(url),
        media_type
    )
    
    return update_link


@router.delete('/links/{link_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: str, username: str = Depends(authenticate_user), db : Session =Depends(get_db)):
    """
    Deletes a link from the database.

    Parameters:
        link_id (str): The ID of the link to delete.
        username (str, optional): The username of the authenticated user. Defaults to the result of the `authenticate_user` dependency.
        db (Session, optional): The database session. Defaults to the result of the `get_db` dependency.

    Raises:
        HTTPException: If the user is not authenticated, or if the link does not exist.
    """
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")

    link = db.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Link not found')

    db.delete(link)
    db.commit()

    return {'link_id': link_id, 'message': 'Link deleted successfully'}
