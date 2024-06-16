from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_posts():
    """Opens the json file and loads blog posts"""
    with open("blog_posts.json", "r") as fileobj:
        blog_posts = json.load(fileobj)
    return blog_posts


def save_blog_posts(posts):
    """Updates the json file"""
    with open('blog_posts.json', 'w') as fileobj:
        json.dump(posts, fileobj)


@app.route('/hello')
def hello_world():
    return 'Hello, World! Here is Lais, your favourite coder!'


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load existing blog posts
        blog_posts = load_posts()

        # Create new blog post
        new_post = {
            'id': max(post['id'] for post in blog_posts) + 1 if blog_posts else 1,
            'author': author,
            'title': title,
            'content': content
        }

        # Append new post to the list
        blog_posts.append(new_post)

        # Save updated list to JSON file
        save_blog_posts(blog_posts)

        # Redirect to the home page
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Load existing blog posts
    blog_posts = load_posts()

    # Find the blog post with the given id and remove it from the list
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save updated list to JSON file
    save_blog_posts(blog_posts)

    # Redirect back to the home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    blog_posts = load_posts()
    if blog_posts is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        blog_posts['author'] = request.form.get('author')
        blog_posts['title'] = request.form.get('title')
        blog_posts['content'] = request.form.get('content')

        # Save updated post back to JSON file
        blog_posts = load_posts()
        for idx, p in enumerate(blog_posts):
            if p['id'] == post_id:
                blog_posts[idx] = blog_posts
                break
        save_blog_posts(blog_posts)

        # Redirect back to index page
        return redirect(url_for('index'))

    # Else, it's a GET request
    # Display the update.html page
    return render_template('update.html', post=blog_posts)

if __name__ == '__main__':
    app.run()
