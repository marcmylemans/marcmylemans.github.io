---
layout: post
title: Creating a Simple Flask Project - Hello  World!
date: 2023-12-27 09:00:00
categories: python flask
tags: python flask script
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

## Step 2: Create a Simple Flask App

Create a new Python file, for example, **app.py**, and add the following code:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

Explanation:
from flask import Flask: Imports the Flask class.

app = Flask(__name__): Creates an instance of the Flask class.

@app.route('/'): A decorator that tells Flask what URL should trigger the function below it.

def hello_world(): A function that returns the string 'Hello, World!'.

app.run(debug=True): Runs the app in debug mode. The server will reload itself if you change the code.

## Step 3: Run Your Flask App

In the terminal, navigate to the directory where your app.py is located and run:

```
python app.py
```

You should see output indicating that the server is running. By default, it will run on http://127.0.0.1:5000/.

## Step 4: Visit Your Application

Open a web browser and go to http://127.0.0.1:5000/. You should see "Hello, World!" displayed.

