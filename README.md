## 📚 Book Database Python Script

The code provided is a Python script that includes two classes: `BSCH` and `DB`.

### 📖 BSCH Class

The `BSCH` class is used to access a JSON file containing data related to workbooks.

### 📚 DB Class

The `DB` class is used to access a JSON file containing data related to books and authors. The `DB` class has several methods that can be called to retrieve information from the JSON file.

- `list_all()`: Returns a formatted list of all the books and authors in the database
- `get_presentation()`: Returns a dictionary of author names and links to their presentations
- `get_books(author)`: Returns a list of books written by a specific author
- `get_bio(author)`: Returns a dictionary containing information about a specific author (such as their name and biography)
- `get_content(author, name)`: Returns a dictionary containing information about a specific book (such as its title and content)
- `get_rnd()`: Returns a dictionary containing information about a randomly selected book and its author.

### 🌐 Flask Application

The script also includes a Flask application that can be used to serve the information retrieved by the `DB` class.

### 🛣️ Routes

- `/`: Renders an HTML template
- `/type/grade/`: Displays a list of authors and their books
- `/type/grade/auth_ind=<int:auth_ind>/book_ind=<int:book_ind>`: Displays information about a specific book.

### 🐍 Python Libraries Used

| Name | Description | Documentation |
| --- | --- | --- |
| pandas | Data manipulation and analysis | https://pandas.pydata.org/docs/ |
| json | Reading JSON files | https://docs.python.org/3/library/json.html |
| random | Generating random selections | https://docs.python.org/3/library/random.html |
| Flask | Creating web applications | https://flask.palletsprojects.com/en/2.0.x/ |
| markupsafe | Securely rendering HTML templates | https://markupsafe.palletsprojects.com/en/2.0.x/ |

This code is used to retrieve and display information about books and authors in a Flask web application.
