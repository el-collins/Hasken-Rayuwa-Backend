from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import get_db, SQLModel
from main import app
from core.auth import authenticate_user
from core.config import settings

# Set up a test database
TEST_DATABASE_URL = f"sqlite:///./{settings.DATABASE_FILE_NAME}"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test database
SQLModel.metadata.create_all(bind=engine)

# Define a function to get a test database session
def override_get_db():
    """
    A function to override the default get_db function for testing purposes.
    
    This function yields a database session using TestingSessionLocal.
    
    Yields:
        Session: A database session.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Create a test client
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Mock the authentication dependency
def mock_authenticate_user():
    return settings.ADMIN_USERNAME

app.dependency_overrides[authenticate_user] = mock_authenticate_user

# Test cases
def test_create_link():
    """
    Test case for creating a link.

    This function sends a POST request to the "/links" endpoint with a JSON payload containing the URL of a YouTube video.
    It asserts that the response status code is 201 (Created) and that the returned JSON data contains the expected values for the "media_type", "title", and "description" keys.

    Parameters:
        None

    Returns:
        None

    Raises:
        AssertionError: If the response status code is not 201, or if any of the expected values in the returned JSON data are missing or incorrect.
    """
    youtube_url = "https://youtu.be/dQw4w9WgXcQ"
    response = client.post("/links", json={"url": youtube_url})
    assert response.status_code == 201
    data = response.json()
    assert data["media_type"] == "youtube"
    assert data["title"] is not None
    assert data["description"] is not None

def test_read_links():
    """
    Test case for reading links.

    This function sends a GET request to the "/links" endpoint and asserts that the response status code is 200 (OK).
    It also asserts that the returned data is a list.

    Parameters:
        None

    Returns:
        None

    Raises:
        AssertionError: If the response status code is not 200, or if the returned data is not a list.
    """
    response = client.get("/links")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_link():
    """
    A test case for updating a link.

    Parameters:
        None

    Returns:
        None
    """
    # Create a new link
    youtube_url = "https://youtu.be/dQw4w9WgXcQ"
    create_response = client.post("/links", json={"url": youtube_url})
    link_id = create_response.json()["id"]

    # Update the link
    new_url = "https://spotifyanchor-web.app/episode/abc123"
    update_response = client.put(f"/links/{link_id}", json={"url": new_url})
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["url"] == new_url
    assert data["media_type"] == "spotify"

def test_delete_link():
    """
    Test case for deleting a link.

    This function creates a new link using the provided YouTube URL and then deletes it using the link's ID.
    It verifies that the link is successfully deleted by sending a GET request to the "/links" endpoint and
    asserting that the returned data is empty.

    Parameters:
        None

    Returns:
        None

    Raises:
        AssertionError: If the response status code for deleting the link is not 204 (No Content), or if the
                        returned data is not empty after deleting the link.
    """
    # Create a new link
    youtube_url = "https://youtu.be/dQw4w9WgXcQ"
    create_response = client.post("/links", json={"url": youtube_url})
    link_id = create_response.json()["id"]

    # Delete the link
    delete_response = client.delete(f"/links/{link_id}")
    assert delete_response.status_code == 204

    # Verify that the link is deleted
    get_response = client.get("/links")
    data = get_response.json()
    assert len(data) == 0