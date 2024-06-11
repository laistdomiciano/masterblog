from flask import Flask, render_template
import json


app = Flask(__name__)

def load_posts():
    """Opens the json file and loads blog posts"""
    with open("blog_posts.json", "r") as fileobj:
        blog_posts = json.load(fileobj)
    return blog_posts

posts = load_posts()

def save_posts(blog_posts):
    """Updates the json file"""
    with open("blog_posts.json", "w") as fileobj:
        json.dump(blog_posts, fileobj)

@app.route('/hello')
def hello_world():
    return 'Hello, World! Here is Lais, your favourite coder!'


@app.route('/')
def index():
    blog_posts = posts
    return render_template('index.html', posts=blog_posts)

if __name__ == '__main__':
    app.run()
