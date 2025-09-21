import json
from flask import Flask, render_template, request, redirect, url_for

# Initialize the Flask application
app = Flask(__name__)

# Path to the data file
JSON_FILE = 'blog_posts.json'


def load_posts():
    """
    Reads posts from a JSON file.
    Returns a list of posts, or an empty list if the file is not found.
    """
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_posts(posts):
    """
    Writes the list of posts back to the JSON file.
    Uses indent=4 for pretty formatting and UTF-8 encoding for non-English text.
    """
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(posts, file, indent=4)


def fetch_post_by_id(post_id):
    """
    Finds a post by its ID from the loaded posts.
    """
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


# Define the route for the index page
@app.route('/')
def index():
    """
    Renders the main blog page, displaying all posts.
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


# Define the route for adding a new blog post
@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handles adding a new blog post. Displays the form on GET and
    processes the form data on POST.
    """
    if request.method == 'POST':
        # Load existing posts
        posts = load_posts()

        # Determine the new post's ID by finding the max ID in the list
        if posts:
            # Find the highest existing ID and add 1
            last_id = max(post['id'] for post in posts)
            new_id = last_id + 1
        else:
            # If no posts exist, start with ID 1
            new_id = 1

        # Get data from the form
        new_post_title = request.form.get('title')
        new_post_author = request.form.get('author')
        new_post_content = request.form.get('content')

        # Create new post
        new_post = {
            "id": new_id,
            "title": new_post_title,
            "author": new_post_author,
            "content": new_post_content
        }

        # Add the new post to the list
        posts.append(new_post)

        # Save the updated list back to the JSON file
        save_posts(posts)

        # Redirect to the home page
        return redirect(url_for('index'))

    # On a GET request, simply render the form
    return render_template('add.html')

# Define the route for the delete functionality
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    """Deletes a specific blog post by its ID."""
    # Load existing posts from the JSON file
    blog_posts = load_posts()

    # Create a new list with all posts except the one to be deleted
    updated_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated list back to the JSON file
    save_posts(updated_posts)

    # Redirect the user to the main blog page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    # Fetch the specific post using the helper function
    post_to_edit = fetch_post_by_id(post_id)

    if post_to_edit is None:
        # If the post is not found, return 404
        return "Post not found", 404

    if request.method == 'POST':
        # Load all posts
        blog_posts = load_posts()

        # Find the same post in the list to update it
        for post in blog_posts:
            if post['id'] == post_id:
                post['title'] = request.form.get('title')
                post['author'] = request.form.get('author')
                post['content'] = request.form.get('content')
                break  # we found and updated the post

        # Save the updated list back to JSON
        save_posts(blog_posts)

        # Redirect back to main blog page
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post_to_edit)


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
