---
layout: post
title: Creating a Simple Flask Project - Simple Website
date: 2023-12-27 09:30:00
categories: python flask
tags: python flask script website
---

# Creating a Simple Flask Project - Hello  World!

## Requirements

Downloading Python is a straightforward process. You can obtain the latest version from the official [Python Downloads](https://www.python.org/downloads/) page.

Once you've downloaded the Python installer, the installation process is made easy with a user-friendly wizard. If you prefer step-by-step guidance, you can refer to the official documentation on using Python on Windows: [Using Python on Windows](https://docs.python.org/3/using/windows.html).

> **Important:** Make sure to select "Add Python to PATH" during the installation. This option allows you to run Python from the command line without specifying the full path each time.




## Step 1: Setting up the Environment and Install Flask

First, you need to create a virtual environment and install Flask. Open your terminal or command prompt and run:

```
python -m venv venv
```

And activate it with:

On Windows:
```
venv\Scripts\activate
```

On MacOS/Linux: source

```
venv/bin/activate
```

Installing Flask:

```bash
pip install Flask
```

## Step 2: Organize Your Project

Create a directory structure like this:

```
YourProject/
│   app.py
└───templates/
    └───index.html
```

YourProject: Your main project folder.

app.py: Your Flask application file.

templates/: A folder to hold your HTML templates.


## Step 3: Create an HTML Template
In the templates folder, create a file named index.html and add some basic HTML content. For example:


```html
<!DOCTYPE html>
<html>
<head>
    <title>My Flask App</title>
</head>
<body>
    <h1>Welcome to My Flask App</h1>
    <p>This is a simple Flask web application.</p>
</body>
</html>

```

## Step 4: Modify Your Flask App to Use the Template

In your app.py, modify the code to render the index.html template.

```
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

Explanation:
from flask import Flask, render_template: Imports the necessary modules from Flask.

render_template('index.html'): Renders the index.html template when the home route ('/') is accessed.

## Step 5: Run Your Flask App

Navigate to your project directory in the terminal and run:

```
python app.py
```

## Step 6: Visit Your Website
Open http://127.0.0.1:5000/ in a web browser. You should see the contents of your index.html displayed.

## Step 7: Expand Your Website

You can create more HTML templates and add more routes to your Flask app. Use the render_template function to render different templates for different routes. In this example we add a few more pages and also include a CSS stylesheet from bootstrapcdn.com to make our site more stylish.


```
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### Modify your index.html to include navigation:

```
<!DOCTYPE html>
<html>
<head>
    <title>My Flask App</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">FlaskApp</a>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                    <a class="nav-link" href="/">Home <span class="sr-only">(current)</span></a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/about">About</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/contact">Contact</a>
                </li>
            </ul>
        </div>
    </nav>
    <div class="container">
        <h1>Welcome to My Flask App</h1>
        <p>This is a simple Flask web application.</p>
    </div>
</body>
</html>
```

### Create More HTML Templates

In the templates folder, create additional HTML files like about.html and contact.html. You can use similar HTML structure as index.html.


about.html

```
<!DOCTYPE html>
<html>
<head>
    <title>About - My Flask App</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">FlaskApp</a>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                    <a class="nav-link" href="/">Home <span class="sr-only">(current)</span></a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/about">About</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/contact">Contact</a>
                </li>
            </ul>
        </div>
    </nav>
    <h1>About Us</h1>
    <p>This is the about page for the Flask web application.</p>
</body>
</html>
```

contact.html

```
<!DOCTYPE html>
<html>
<head>
    <title>Contact - My Flask App</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">FlaskApp</a>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                    <a class="nav-link" href="/">Home <span class="sr-only">(current)</span></a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/about">About</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/contact">Contact</a>
                </li>
            </ul>
        </div>
    </nav>
    <h1>Contact Us</h1>
    <p>This is the contact page for the Flask web application.</p>
</body>
</html>
```

## Step 8: Run and Test Your Application
Run app.py and visit each page (/, /about, /contact) in your web browser to see the navigation bar and Bootstrap styling in action.

**Conclusion**
You now have a Flask web application with multiple pages, styled with Bootstrap, and a navigation bar for easy browsing. This setup forms a great foundation for more complex web applications. Remember to consult Flask and Bootstrap documentation for more advanced features and customization options.