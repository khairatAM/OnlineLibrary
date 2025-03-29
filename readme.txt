ONLINE LIBRARY MANAGEMENT SYSTEM (--KHAIRAT MONGUNO)

TOOLS:
This web system was developed using the following technologies:
- Django (A Python MVT web development framework)
- SQLite (For the database)

HOW TO RUN:
1. Ensure Python 3 is install on your system. If it is not, install it by running the command:
    `python3 -m pip install --user virtualenv`.

2. Duplicate the repo to a chosen directory on your local device. 

3. Open a new terminal and cd to the directory containing the repo. Then, in the terminal, run the command 
    `source django-env/bin/activate`
   to activate the virtual environment for the project.

4. Next, execute the following command in the terminal:
    `cd onlinelibrary`.

5. And, in the same terminal, where the virtual environment is active, run the following commands sequentially: 
    `python manage.py makemigrations`
    `python manage.py migrate`
   to set up the SQLite database.

5. Run the project server with the command:
    `python manage.py runserver`.

6. Access the project by pasting the following URL in your browser of choice (preferably Chrome):
    `http://127.0.0.1:8000/books`.

7. Emails
7. a. Setting up Redis
As the application uses a Redis server to queue the emails, ensure your Redis server is up and running, with the following link:
    `https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/`.
The program uses the following URL for Redis: `redis://localhost:6379/0`. Ensure your port number matches.

7. b. Monitoring the Emails
To view the email activity, START ~TWO~ NEW TERMINALS. Repeat steps 3 & 4 above in EACH OF THE NEW TERMINALS. 
Then in one terminal, run the command:
    `celery -A core beat --loglevel=info`
And, in the other terminal, run the command:
    `celery -A core worker --loglevel=info`