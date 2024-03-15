import requests
import sqlite3

# Define the API endpoint URL
url = "https://dummyapi.io/data/v1/user"

# Define your app_id
app_id = "65f2926fa76fe01c3178c1d5"  # Replace with your actual app ID obtained after signup

# Define request headers with app_id
headers = {"app-id": app_id}

def fetch_users_data():
    # Make a GET request to the API with headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract and parse the response JSON
        users_data = response.json()

        # Connect to the SQLite database
        conn = sqlite3.connect('users_posts.db')
        cursor = conn.cursor()

        # Insert users' data into the users table
        for user in users_data['data']:
            user_id = user['id']
            first_name = user['firstName']
            last_name = user['lastName']
            email = user.get('email', '')
            # Check if the user ID already exists in the database
            cursor.execute("SELECT id FROM users WHERE id=?", (user_id,))
            existing_user = cursor.fetchone()

            # If the user ID does not exist, insert the user data
            if not existing_user:
                cursor.execute("INSERT INTO users (id, firstName, lastName, email) VALUES (?, ?, ?, ?)",
                               (user_id, first_name, last_name, email))
            else:
                print(f"User with ID {user_id} already exists in the database. Skipping insertion.")

        
        # Commit changes and close connection
        conn.commit()
        conn.close()

        print("Users data fetched and stored successfully.")
    else:
        print("Error:", response.status_code)

def fetch_posts_data():
    # Define the base API endpoint URL
    base_url = "https://dummyapi.io/data/v1/user"

    # Connect to the SQLite database
    conn = sqlite3.connect('users_posts.db')
    cursor = conn.cursor()

    # Fetch user IDs from the users table
    cursor.execute("SELECT id FROM users")
    user_ids = cursor.fetchall()

    for user_id in user_ids:
        # Make a GET request to the API with user-specific endpoint
        url = f"{base_url}/{user_id[0]}/post"
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract and parse the response JSON
            posts_data = response.json()

            # Insert posts data into the posts table
            for post in posts_data['data']:
                post_id = post['id']
                title =post.get('title', 'No Title')
                body = post.get('body', 'No Body')

                # Check if the post ID already exists in the database
                cursor.execute("SELECT id FROM posts WHERE id=?", (post_id,))
                existing_post = cursor.fetchone()

                # If the post ID does not exist, insert the post data
                if not existing_post:
                    cursor.execute("INSERT INTO posts (id, userId, title, body) VALUES (?, ?, ?, ?)",
                                   (post_id, user_id[0], title, body))
                else:
                    print(f"Post with ID {post_id} already exists in the database. Skipping insertion.")

            print(f"Posts data for user {user_id[0]} fetched and stored successfully.")
        else:
            print(f"Error fetching posts data for user {user_id[0]}:", response.status_code)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fetch_users_data()
    fetch_posts_data()
