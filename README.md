# Hasken Rayuwa Link Storage API

Hasken Rayuwa Link Storage API is a FastAPI application that allows authenticated users to store and manage YouTube and Spotify links. The application provides several endpoints for creating, retrieving, updating, and deleting links.

## Features

- User authentication with admin credentials
- Create new links with YouTube or Spotify URLs
- Retrieve a list of stored links, filtered by media type (YouTube or Spotify)
- Update the URL of an existing link
- Delete an existing link
- Logout functionality for authenticated users

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/hasken-rayuwa-api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd hasken-rayuwa-api
    ```

3. Create a virtual environment and activate it:

    ```bash 
    poetry shell
    ```

4. Install the required dependencies:

    ```bash
    poetry install
    ```

5. Start the FastAPI application:

    ```bash
    uvicorn main:app --reload --port 5000
    ```

The API will be available at <http://localhost:5000>.

## Usage

### Authentication

To authenticate as an admin user, you need to provide the admin credentials in the Authorization header using Basic Auth. The default admin credentials are:

- Username: check config
- Password: check config

Endpoints
========

### POST /auth

Authenticates the user with the provided credentials.

### POST /links

Creates a new link in the database with the given YouTube or Spotify URL. Requires authentication.

### GET /links

Retrieves a list of stored links. Supports filtering by media type using the `media_type` query parameter.

### PUT /links/{link_id}

Updates the URL of an existing link. Requires authentication.

### DELETE /links/{link_id}

Deletes an existing link. Requires authentication.

### POST /logout

Logs out the authenticated user.

<!-- License
=======

This project is licensed under the MIT License. -->
# Hasken-Rayuwa-Backend
