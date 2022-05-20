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
### Clone The Repo
```bash
git clone https://github.com/Tut-k0/fast_api.git
cd fast_api
pip install -r requirements.txt
# If psycopg2 fails to install use psycopg2-binary instead.
```
We now need to seed the database tables and columns from the migrations.
```bash
python -m alembic upgrade head
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
python -m uvicorn app.main:app
```
Go to http://127.0.0.1:8000/docs once running for built-in documentation.
Currently, there aren't any seeded users, so one will need to be manually created. 
This can be done through the DB but is better off done through the API.
Edit user.py under routers and comment out this parameter on the create_user function
```python 
current_user: models.User = Depends(oauth2.get_current_user
```
So you can use that endpoint unauthenticated. Once you create a user you can add that parameter back.