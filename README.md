**Spookies API Documentation**

# Welcome to the Spookies API!

## Overview

The Spookies API is a Django-based web service designed to manage user interactions. It facilitates:

* User authentication (signup and login)
* Friendship management (sending/accepting/rejecting requests, removing friends, listing friends)
* Creation and deletion of "spooky messages" among friends

This documentation provides comprehensive details on interacting with the API endpoints, covering authentication, friendship management, and spooky message functionalities.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/itsvenox/spookyAPI.git
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Apply migrations:**

```bash
python manage.py migrate
```

## Features

* **User Authentication:** Securely access resources by signing up or logging in with your credentials.

* **Friendship Management:** Build your social network by sending friend requests, managing incoming requests, removing friends, and viewing your friend list.

* **Spooky Messages:** Create and share spooky messages with your friends. You can list sent and received spookies and even delete messages you've sent.

## Authentication

The API uses token-based authentication for secure access. To access protected resources, users must first obtain an authentication token by logging in or signing up.

### Endpoints

* **Login (`/api/v1/auth/login/`):** POST request to authenticate a user and receive an authentication token.

  **Request Example:**

  ```json
  {
    "username": "example_user",
    "password": "example_password"
  }
  ```

  **Response Example:**

  ```json
  {
    "token": "example_token"
  }
  ```

* **Signup (`/api/v1/auth/signup/`):** POST request to create a new user account and receive an authentication token.

  **Request Example:**

  ```json
  {
    "username": "new_user",
    "email": "new_user@example.com",
    "password": "new_password",
    "phone_number": "1234567890"
  }
  ```

  **Response Example:**

  ```json
  {
    "token": "example_token"
  }
  ```

* **Current User (`/api/v1/auth/current-user/`):** GET request to retrieve details of the currently authenticated user.

  **Response Example:**

  ```json
  {
    "id": 1,
    "username": "example_user",
    "email": "example_user@example.com",
    "phone_number": "1234567890",
    "profile_picture": "example_picture_url",
    "level": 5,
    "reputation": 100
  }
  ```

## Friendship Management

The Spookies API empowers you to manage your social circle.

### Endpoints

* **Send Friend Request (`/api/v1/friendship/send-friend-request/`):** POST request to send a friend request to another user.

  **Request Example:**

  ```json
  {
    "recipient": "friend_username"
  }
  ```

  **Response Example:**

  ```json
  {
    "message": "Friend request sent successfully"
  }
  ```

* **Handle Friend Request (`/api/v1/friendship/handle-friendship-request/`):** POST request to accept or reject a friend request.

  **Request Example:**

  ```json
  {
    "sender": "sender_username",
    "action": "accept" // or "reject"
  }
  ```

  **Response Example:**

  ```json
  {
    "message": "Friend request accepted and friendship created"
  }
  ```

* **Remove Friend (`/api/v1/friendship/remove-friend/`):** POST request to remove a friend.

  **Request Example:**

  ```json
  {
    "friend": "friend_username"
  }
  ```

  **Response Example:**

  ```json
  {
    "message": "Friend removed successfully"
  }
  ```

* **My Friends (`/api/v1/friendship/my-friends/`):** GET request to list all your friends.
  **Response Example:**
    ```json
    {
        "friends": [
            {
                "id": 2,
                "username": "friend_username",
                "profile_picture": "friend_picture_url",
                "friends_since": "2 days ago"
            },
            {
                "id": 3,
                "username": "another_friend",
                "profile_picture": "another_friend_picture_url",
                "friends_since": "1 week ago"
            }
        ]
    }
    ```


## Spookies (continued)

### Spookies

Unleash your inner spook with spooky messages!

### Endpoints

* **Create Spooky (`/api/v1/spooky/create-spooky/`):** POST request to create a spooky message and send it to your friends.

  **Request Example:**

  ```json
  {
    "message": "Hello there, ghosts and ghouls!",
    "friends": ["friend_username1", "friend_username2"]
  }
  ```

  **Response Example:**

  ```json
  {
    "spooky": {
      "id": 1,
      "sender": "example_user",
      "message": "Hello there, ghosts and ghouls!",
      "expiration_time": "2024-03-16T14:30:00Z"
    },
    "latest_spookies": {
      "friend_username1": 1,
      "friend_username2": 1
    }
  }
  ```

* **List Spookies (`/api/v1/spooky/list-spookies/`):** GET request to list all the spooky messages you've sent and received.

  **Response Example:**

  ```json
  {
    "sent_spookies": [
      {
        "id": 1,
        "sender": "example_user",
        "message": "Hello there, ghosts and ghouls!",
        "expiration_time": "2024-03-16T14:30:00Z"
      }
    ],
    "received_spookies": [
      {
        "id": 2,
        "sender": "friend_username",
        "message": "Boo! ",
        "expiration_time": "2024-03-16T14:35:00Z"
      }
    ]
  }
  ```

* **Delete Spooky (`/api/v1/spooky/delete-spooky/<spooky_id>/`):** DELETE request to delete a specific spooky message you've sent.

  **Response Example:**

  ```json
  {
    "message": "Spooky message deleted successfully."
  }
  ```

## Usage

Interact with the Spookies API using tools like cURL, Postman, or programming libraries suited for your needs.

**Example cURL commands:**

* **Login:**

```bash
curl -X POST -d "username=username&password=password" http://example.com/api/v1/auth/login/
```

* **Send Friend Request:**

```bash
curl -X POST -H "Authorization: Token <token>" -d "recipient=username" http://example.com/api/v1/friendship/send-friend-request/
```

* **Create Spooky:**

```bash
curl -X POST -H "Authorization: Token <token>" -d "message=Boo!&friends=username1,username2" http://example.com/api/v1/spooky/create-spooky/
```



## Conclusion

If you have any questions or encounter issues, feel free to contact me: @itsvenox .

Happy Spookying with Spookies!
