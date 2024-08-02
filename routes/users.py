from sqlmodel import Session
import cloudinary.uploader
import cloudinary.api
from db.database import get_db, get_or_create_entity
from models.users import VolunteerUser, ContactUser, User
from core.auth import authenticate_user, logout_user
from fastapi import APIRouter, Depends, Form, File, HTTPException, UploadFile, Query

users_router = router = APIRouter(tags=["Users"])

@router.post('/users/contact')
def create_contact(
    fullname: str, 
    email: str , 
    message: str , 
    db: Session = Depends(get_db)) -> dict:
    
    """
    Creates a new contact message in the database.

    Returns:
        Contact: The created contact object.
    """
    existing_user = db.query(User).filter(User.email == email).first()
    
    if not existing_user:
        save_user = get_or_create_entity(
            db, 
            User, 
            fullname=fullname, 
            email=email
        )
    
    contact = get_or_create_entity(
        db, 
        ContactUser, 
        fullname=fullname, 
        email=email, 
        message=message
    )
    
    print("contact created", contact)
    
    return {'msg': "Contact User created"}

@router.post('/users/volunteer')
def user_volunteer(fullname: str, email: str , phone_number: str, address: str, db: Session = Depends(get_db)) -> dict:
    
    existing_user = db.query(User).filter(User.email == email).first()
    
    if not existing_user:
        save_user = get_or_create_entity(
            db, 
            User, 
            fullname=fullname, 
            email=email
        )
        
    volunteer = get_or_create_entity(
        db, 
        VolunteerUser, 
        fullname=fullname, 
        email=email, 
        phone_number=phone_number, 
        address=address
        )
    
    return {'msg': "Volunteer User created"}

@router.get('/users')
def get_users(
    db: Session = Depends(get_db),
    skip: int = 0, 
    limit: int = 20,
    group: str | None = Query(None, description="Filter by group: contact, volunteer or both")
) -> list[dict]:
    """
    Retrieves a list of users from the database, comparing with contact and volunteer users, and returns the results with the specified format.

    Parameters:
        db (Session, optional): The database session. Defaults to the result of the `get_db` dependency.
        skip (int): The number of records to skip in the query.
        limit (int): The maximum number of records to return.
        group (str, optional): Filter by group: contact, volunteer or both.

    Returns:
        list[dict]: A list of user objects that match the specified criteria with group information.
    """
    
    # Query to get all users from the User model
    user_query = db.query(User).offset(skip).limit(limit).all()

    # Query to get all contact users
    contact_query = db.query(ContactUser).all()
    contact_emails = {user.email for user in contact_query}

    # Query to get all volunteer users
    volunteer_query = db.query(VolunteerUser).all()
    volunteer_emails = {user.email for user in volunteer_query}

    # Prepare the results
    results = []

    for user in user_query:
        email = user.email
        if email in contact_emails and email in volunteer_emails:
            if not group or group == 'both':
                results.append({'email': email, 'group': 'contact | volunteer'})
        elif email in contact_emails:
            if not group or group == 'contact':
                results.append({'email': email, 'group': 'contact'})
        elif email in volunteer_emails:
            if not group or group == 'volunteer':
                results.append({'email': email, 'group': 'volunteer'})

    return results

@router.post('/images', tags=["Images"])
async def upload_image(file: UploadFile = File(...)):
    try:
        upload_result = cloudinary.uploader.upload(file.file)
        return {"url": upload_result['secure_url']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/images', tags=["Images"])
async def get_images(next_cursor: str = Query(None)):
    """
    Retrieves images from Cloudinary with optional pagination parameters.

    Parameters:
        next_cursor (str, optional): The cursor for fetching the next set of images.

    Returns:
        dict: A dictionary containing the image URLs and the next cursor.
    """
    try:
        resources = cloudinary.api.resources(type="upload", max_results=30, next_cursor=next_cursor)
        image_urls = [resource["secure_url"] for resource in resources["resources"]]
        next_cursor = resources.get("next_cursor")
        return {"images": image_urls, "next_cursor": next_cursor}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch images from Cloudinary")