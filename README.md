# Mailling Project

This is a Django-based project for managing Gmail accounts, sending emails, and categorizing messages.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.10+
- PostgreSQL
- Git

## Installation

Follow these steps to set up the project:

1. **Clone the repository:**

- Create a empty folder and `cd` into that folder.
- Type the following command to clone project in same directory.

   ```bash
   git clone https://github.com/Lucien45/mailling_spam_inteligence_artificielle.git
   cd mailling_spam_inteligence_artificielle
   ```

2. **Create and activate the virtual environment:**
   ```bash
   python -m venv .env
   .env\Scripts\activate
   ```
   > If their is any error activating virtual env, please google search it for your system or try 
`.env\bin\activate` or `source .env/bin/activate`

3. **Install required packages:**
    ```bash
    pip install -r requirements.txt
    ```
   
4. **onfigure the database:**
    ```bash
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

5. **Run the server:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    ```