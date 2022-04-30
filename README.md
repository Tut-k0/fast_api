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
/* Change password and create DB */
ALTER USER postgres WITH PASSWORD 'SecurePassHere';
CREATE DATABASE fastapi;
exit
```
After doing so you will need to change the database connection string 
SQLALCHEMY_DATABASE_URL in database.py to reflect the correct database info.
### Start API
```bash
pip install -r requirements.txt
# If psycopg2 fails to install use psycopg2-binary instead.
python -m uvicorn app.main:app
```
Go to http://127.0.0.1:8000/docs once running for documentation.