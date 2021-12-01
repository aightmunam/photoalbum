# photoalbum

1. Clone this repo
```
git clone https://github.com/aightmunam/photoalbum.git
```
2. Create a virtualenv and activate it
```
virtualenv venv
source venv/bin/activate
```
3. Make sure you have MySQL installed. If not, download it from [here](https://dev.mysql.com/downloads/) and install it.

4. Install all python requirements
```
pip install -r requirements.txt
```
5. Create your MySQL database and user to be used with this project. You will need DB name, DB user with access to this DB, 
and the password. 
```
sudo mysql -u root -p  // This will open the mysql console

mysql> CREATE DATABASE <db_name>;
mysql> CREATE USER <db_user> IDENTIFIED WITH mysql_native_password BY <db_password>;
mysql> GRANT ALL ON <db_name>.* TO <db_user>;
mysql> FLUSH PRIVILEGES;

```
Once all three have been made, we need to export the following variables into our environment as:
```
DATABASE_NAME=<db_name>
DATABASE_USER=<db_user>
DATABASE_PASSWORD=<db_password>
```
You can either export them by doing `export DATABASE_NAME=<db_name>` in the terminal or you can create a `.env` file in 
the root directory of this project containing the above code.

6. You'll need a Redis server. If you don't have one the easiest way is through Docker with the following command:
```
docker run --name my-redis-server -d -p 127.0.0.1:6379:6379 redis
```
7. After the redis server is up, we need to export another variable to the environment or add it to the `.env` file
```
CELERY_BROKER_URL=redis://localhost:6379
```
8. We need to generate and add a variable `SECRET_KEY` to our environment that will act as the project's secret key.
```
python -c "import secrets; print(secrets.token_urlsafe())" 
```
This command will generate a key, now simply export it into the environment or add it to the `.env` file.
```
SECRET_KEY= # Add generated key here
```
9. Now, we need to run the database migrations and run the django server
```
python3 manage.py migrate
python3 manage.py runserver
```

10. Then in a second terminal window, navigate to your project directory, activate the virtual environment again and run
the celery process
```
python3 -m celery -A photoalbum worker -l info -P solo
```

11. Now, open the django shell as:
```
python3 manage.py shell
```
Inside the shell, type the following

```
> from django.contrib.sites.models import Site
> Site.objects.create(name='example.com', domain='example.com')
```
