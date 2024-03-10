# SpookyAPI

## Description
Spooky is a Django-based web application that provides functionalities for user authentication, friendship management, and spooky messages.

## Features
- **User Authentication**: Users can sign up, log in, and authenticate using their credentials.
- **Friendship Management**: Users can send friend requests, accept or reject friend requests, remove friends, and list their friends.
- **Spooky Messages**: Users can create spooky messages, list sent and received spookies, and delete spookies they've sent.


## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/itsvenox/----
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
  - `/api/v1/auth/signup/`: POST - Sign up a user.
  - `/api/v1/auth/login/`: POST - Log in a user.
- **Friendship**:
  - `/api/v1/friendship/send-friend-request/`: POST - Send a friend request.
  - `/api/v1/friendship/handle-friendship-request/`: POST - Accept or reject a friend request.
  - `/api/v1/friendship/remove-friend/`: POST - Remove a friend.
  - `/api/v1/friendship/my-friends/`: GET - List user's friends.
- **Spookies**:
  - `/api/v1/spookies/create-spooky/`: POST - Create a spooky message.
  - `/api/v1/spookies/list-spookies/`: GET - List sent and received spookies.
  - `/api/v1/spookies/delete-spooky/<int:spooky_id>/`: DELETE - Delete a spooky message.

## Contributing
Contributions are welcome! Feel free to fork the repository, make pull requests, and suggest new features or improvements.
