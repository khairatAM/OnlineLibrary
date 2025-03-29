ONLINE LIBRARY MANAGEMENT SYSTEM (--KHAIRAT MONGUNO)

TOOLS:
This web system was developed using the following technologies:
- Django (A Python MVT web development framework)
- SQLite (As the primary database)
- Redis (To queue tasks)

HOW TO RUN:
1. Ensure Python 3 is install on your system. If it is not, follow the official documentation to install it, avaible here:
    `https://www.python.org/downloads/`.

2. Clone the project repo via the URL https://github.com/khairatAM/OnlineLibrary.git file to a chosen directory and cd to the project folder. 

3. SETTING UP THE VIRTUAL ENVIRONMENT 
3.a. Install virtualenv if not already installed with the command: `pip install virtualenv` or `pip3 install virtualenv`
3.b. Create your environment (called venv) with the command: `virtualenv venv`
3.c. Enter the environment using: `source venv/bin/activate`
3.d. Install the necessary requirements in the environment using: `pip install -r requirements.txt`

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

7. Default Admin Credentials
The application comes with a default admin user with the following log in details:
- Username: admin001
- Password: Password123
However, you will need to create a reader (non-admin user) by registering.

8. Emails
8. a. Setting up Redis
As the application uses a Redis server to queue emails, ensure your Redis server is up and running by following the official documentation, available at:
    `https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/`.
The program uses the following URL for Redis: `redis://localhost:6389/0`. Ensure your port number matches.

8. b. Monitoring the Emails
To view the email activity, START ~TWO~ NEW TERMINALS. Repeat steps 3.b., 3.c. & 4 ONLY in EACH OF THE NEW TERMINALS. 
Then in one terminal, run the command:
    `celery -A core beat --loglevel=info`
And, in the other terminal, run the command:
    `celery -A core worker --loglevel=info`
The mailing activity can then be observed accordingly from both terminals.
