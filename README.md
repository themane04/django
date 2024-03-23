## Bridging Frontend and Backend with React
I took on a challenge to combine the strengths of Django and React, aiming for a seamless interaction between backend logic and a dynamic frontend. This led to creating two specific branches: one for developing Minigram’s frontend frontend with React and another for adjusting the Django ***backend*** to ensure everything works together smoothly.

Despite my enthusiasm and the progress made, I haven’t finished this project yet due to time constraints. However, the groundwork is there, and it’s been an eye-opening experience seeing how these two technologies can complement each other.

This project is on pause for now, but I’m hopeful about picking it up again in the future to see through its completion.

Check out the other branches!
* [Minigram's Frontend with React](https://github.com/themane04/django/tree/minigram_frontend_react)
* [Minigram only Django](https://github.com/themane04/django/tree/minigram)
* [Notes project](https://github.com/themane04/django/tree/master)

## Setup
### Clone both branches minigram_backend_react and minigram_frontend_react
```
git clone -b minigram_backend_react git@github.com:themane04/django.git

# rename the folder for the backend to avoid git issues for example django_b

git clone -b minigram_frontend_react git@github.com:themane04/django.git
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
* Update your .env file with the database connection details, all of the things that you need are in *.env.example*:
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

### Moving on to the Frontend
After you've started the django server you can leave it like that and move onto the [frontend branch](https://github.com/themane04/django/tree/minigram_frontend_react).
