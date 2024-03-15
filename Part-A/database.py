import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('users_posts.db')
cursor = conn.cursor()

# Fetch data from the users table
cursor.execute("SELECT * FROM users")
users_data = cursor.fetchall()

# Fetch data from the posts table
cursor.execute("SELECT * FROM posts")
posts_data = cursor.fetchall()

# Print the fetched data
print("Users data:")
for user in users_data:
    print(user)

print("\nPosts data:")
for post in posts_data:
    print(post)

# Close the connection
conn.close()
