# WIP

## Install/Run Instructions
These instructions are based on running off a Debian based distro.
### Install/Start Database
```bash
# We will now need a postgresql database
sudo apt install postgresql -y
sudo systemctl start postgresql

# Switch to the postgres user and enter the psql shell.
sudo su - postgres
psql
```
```sql
/* Change password and create DB, the name can be whatever you want. */
ALTER USER postgres WITH PASSWORD 'SecurePassHere';
CREATE DATABASE fastapi;
exit
```
### Start API
After setting up the database, you will need to create a .env file in the project root directory with all the environment
variables set correctly. Here is an example:
```dotenv
DB_HOSTNAME=localhost
DB_PORT=5432
DB_PASSWORD=SecurePassHere
DB_NAME=fastapi
DB_USERNAME=postgres
SECRET_KEY=549e20314db0f2fbc78705c6b6d9ab5367d34ece54d90c4cf6c655e9dda0
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
Now we are ready to start the API. Make sure you have all the requirements, 
and you should be good to go.
```bash
pip install -r requirements.txt
# If psycopg2 fails to install use psycopg2-binary instead.
python -m uvicorn app.main:app
```
Go to http://127.0.0.1:8000/docs once running for built-in documentation.