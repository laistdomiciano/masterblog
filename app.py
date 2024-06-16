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


if __name__ == '__main__':
    app.run()
