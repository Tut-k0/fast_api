# Fast API Implementation
A full-fledged API implementation with Python utilizing FastAPI. 
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

## Docker Setup
This setup still requires setting up the above .env file. 
Also change the postgres environment variables to be correct in the compose file.
```bash
docker-compose -f docker-compose-dev.yml up -d
docker exec fast_api_api_1 "alembic" "upgrade" "head"
```
Go to http://127.0.0.1:8000/docs once running for built-in documentation.