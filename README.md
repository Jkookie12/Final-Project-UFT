😊This is my Objected-Oriented Programming project "BlogPost Using Python Django" in my second year college.

### Description 🤍
This project is a web application built using Django, designed to allow users to create, read, update, and delete blog posts. 
It provides a simple yet powerful content management system where users can share their thoughts, ideas, and experiences through blog entries.

### Features 🤍
1. User authentication (signup, login, logout)
2. Create, edit, and delete blog posts
3. View a list of all posts
4. View detailed individual posts
5. Commenting a blogpost
6. Liking a blogpost

### Technologies Used 🤍
--- Backend: Python Django
--- Frontend: HTML, CSS, Bootstrap, JavaScript
--- Database: SQLite3

### Version Control 🤍
--- Git & GitHub

### Installation Guide 🤍
1. Clone the repository:
- git clone <your-repo-url>
- cd blogpost

2. Create a virtual environment:
- python -m venv env
- source venv/bin/activate  #on Windows use `env\Scripts\activate`

3. Install dependencies:
- pip install -r requirements.txt

4. Apply database migrations:
- python manage.py migrate

5. Run the development server:
-python manage.py runserver

6. Access the application:
- Open http://127.0.0.1:8000 in your browser.

### Usage 🤍
1. Register or log in to create and manage blog posts.
2. Navigate through the homepage to view all posts.
3. Click on a post title or read more to view its details.
4. Edit or delete posts (if authorized).

### Contributing 🤍
If you want to contribute:
1. Fork the repository.
2. Create a new branch (feature-new).
3. Commit your changes and push them.
4. Create a pull request.

### Contact 🤍
For any questions or feedback, feel free to contact at daisyloumontante1@gmail.com

---

## Desktop Application Build

A lightweight desktop version of the blog can be created using the
`desktop.py` launcher script together with PyInstaller.  The launcher
starts an embedded Waitress server and opens a native window with
`pywebview`.

To package everything into a single executable on Windows:

```powershell
# ensure you are using the project's virtual environment
.env\Scripts\python -m pip install pyinstaller

# build including templates and static assets
.env\Scripts\python -m pyinstaller \
    --onefile \
    --add-data "templates;templates" \
    --add-data "blogpost/templates;blogpost/templates" \
    --add-data "members/templates;members/templates" \
    --add-data "static;static" \
    desktop.py
```

The PyInstaller bootloader extracts the bundle to a temporary
folder before execution.  The settings module handles this by using
`sys._MEIPASS` when running frozen so Django can still resolve
`BASE_DIR` and load templates.

The resulting `dist\desktop.exe` is a standalone desktop app that
behaves identically to running `python desktop.py`.
