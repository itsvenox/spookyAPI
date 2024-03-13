# SpookyAPI

## Description
Spooky is a REST API made with Django-rf that provides functionalities for user authentication, friendship management, and spooky messages.

## Features
- **User Authentication**: Users can sign up, log in, and authenticate using their credentials.
- **Friendship Management**: Users can send friend requests, accept or reject friend requests, remove friends, and list their friends.
- **Spooky Messages**: Users can create spooky messages, list sent and received spookies, and delete spookies they've sent.


## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/itsvenox/spookyAPI.git
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Apply migrations:
    ```bash
    python manage.py migrate
    ```


## Usage
1. Run the development server:
    ```bash
    python manage.py runserver
    ```
2. Access the application at `http://localhost:8000` in your web browser.


## API Endpoints
- **Authentication**:
  - `/api/auth/signup/`: POST - Sign up a user.
    - **Request Body**:
      ```json
      {
        "username": "string",
        "email": "string",
        "password": "string",
        "phone_number": "string"
      }
      ```
    - **Response**:
      ```json
      {
        "message": "success",
        "data": {
          "token": "string"
        }
      }
      ```
  - `/api/auth/login/`: POST - Log in a user.
    - **Request Body**:
      ```json
      {
        "username_or_email_or_phone": "string",
        "password": "string"
      }
      ```
    - **Response**:
      ```json
      {
        "message": "success",
        "data": {
          "token": "string"
        }
      }
      ```
- **Friendship**:
  - `/api/friendship/send-friend-request/`: POST - Send a friend request.
    - **Request Body**:
      ```json
      {
        "recipient": "string"
      }
      ```
    - **Response**:
      ```json
      {
        "message": "Friend request sent successfully"
      }
      ```
  - `/api/friendship/handle-friendship-request/`: POST - Accept or reject a friend request.
    - **Request Body**:
      ```json
      {
        "sender": "string",
        "action": "string"
      }
      ```
    - **Response**:
      ```json
      {
        "message": "Friend request accepted and friendship created"
      }
      ```
  - `/api/friendship/remove-friend/`: POST - Remove a friend.
    - **Request Body**:
      ```json
      {
        "friend": "string"
      }
      ```
    - **Response**:
      ```json
      {
        "message": "Friend removed successfully"
      }
      ```
  - `/api/friendship/my-friends/`: GET - List user's friends.
    - **Response**:
      ```json
      {
        "friends": [
          {
            "id": "integer",
            "username": "string",
            "profile_picture": "string",
            "friends_since": "string"
          }
        ]
      }
      ```
- **Spookies**:
  - `/api/spookies/create-spooky/`: POST - Create a spooky message.
    - **Request Body**:
      ```json
      {
        "message": "string",
        "friends": ["string"]
      }
      ```
    - **Response**:
      ```json
      {
        "spooky": {
          "id": "integer",
          "message": "string",
          "sender": "string",
          "expiration_time": "string",
          "created_at": "string"
        },
        "latest_spookies": {
          "username": "integer"
        }
      }
      ```
  - `/api/spookies/list-spookies/`: GET - List sent and received spookies.
    - **Response**:
      ```json
      {
        "sent_spookies": [
          {
            "id": "integer",
            "message": "string",
            "sender": "string",
            "expiration_time": "string",
            "created_at": "string"
          }
        ],
        "received_spookies": [
          {
            "id": "integer",
            "message": "string",
            "sender": "string",
            "expiration_time": "string",
            "created_at": "string"
          }
        ]
      }
      ```
  - `/api/spookies/spookies/<int:spooky_id>/`: DELETE - Delete a spooky message.
    - **Response**:
      ```json
      {
        "message": "Spooky message deleted successfully."
      }
      ```



## Contributing
Contributions are welcome! Feel free to fork the repository, make pull requests, and suggest new features or improvements.
