## Minigram
The ***minigram*** branch showcases a more ambitious project I developed on my own: Minigram. It’s a social media platform where users can interact with posts, profiles, likes, and comments. What began as a project for learning morphed into a hobby, driven by my passion for coding and connecting people online.

I've put extra effort into Minigram, even in my free time, because it represents not just what I've learned but also what I love about development: bringing people together. Feel free to clone the minigram branch and see what Minigram is all about.

Check out the other branches!
* [Minigram's Frontend with React](https://github.com/themane04/django/tree/minigram_frontend_react)
* [Minigram's Backend with React changes](https://github.com/themane04/django/tree/minigram_backend_react)
* [Notes project](https://github.com/themane04/django/tree/master)

## Setup
### Clone and navigate into the repository
```
git clone -b minigram git@github.com:themane04/django.git
cd django
```
### Create and Activate a Virtual Environment
Create a virtual environment named *.venv* in your project directory, and activate it using the appropriate command for your operating system:
```
# Windows Terminal
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1

# Linux or MacOS
$ source .venv/bin/activate
```
If you encounter issues, consult [this guide on virtual environments](python.land/virtual-environments/virtualenv) for additional help.

### Install Project Dependencies
With the virtual environment activated, install the required Python packages specified in *requirements.txt*:
```
pip install -r requirements.txt
```

### Set Up the PostgreSQL Database
This project uses a PostgreSQL database to store its data. To set up your local database:
If you want you can either type in the queries yourself to create the database and set it up or you can simply download [PgAdmin](https://www.pgadmin.org/download/pgadmin-4-windows/) and set up everything using the GUI.

Create a New Database:
* Open PgAdmin and connect to your PostgreSQL server.
* Right-click on the *Databases* node, then select Create > Database....
* Name your database as you wish, but remember the name since you will need it.

Configure Your *.env* File:
* Update your .env file with the database connection details:
  * *DATABASE_NAME:* The name of the database you just created.
  * *DATABASE_USER:* Your PostgreSQL user name.
  * *DATABASE_PASSWORD:* Your PostgreSQL password.
  * Other relevant details as needed (host, port, etc.), typically these will be localhost and the default PostgreSQL port if you're working locally.
> [!NOTE]  
> Ensure that the database settings in your *.env* file match the credentials and database name you've set in pgAdmin to avoid connection issues.

### Apply the Migrations to the Database
Django uses migrations to apply changes made to your models (e.g., creating a new table, or adding a field to an existing table) into the database schema. To ensure your database structure matches your Django project's models, follow these steps:

* In your terminal (ensure your virtual environment is active and you are in the project directory), run the following command to create migration files based on the changes detected in your models:
```
py .\manage.py makemigrations
```
* Next, apply these migrations to update your database schema:
```
py .\manage.py migrate
```

### Run the Development Server
Start Django's development server to view the project locally:
```
python manage.py runserver
```

### Navigate to the website
Once the development server is running, you'll see a message in the terminal that includes a URL, usually something like *http://127.0.0.1:8000/* or *http://localhost:8000/.* 
Click on this link or copy and paste it into your web browser's address bar to navigate to the website. You should now see the homepage of Minigram, indicating that the setup process was successful and the server is running correctly.
