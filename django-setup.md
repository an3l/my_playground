---
title: "Getting started with django"
author: Anel Husakovic
date: January 18, 2020
output: project
---

### Install virtualenv
Install packages using pip (python package manager used to install and update packages) and virtual [env1](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

Latest version of pip
```
>> python3 -m pip install --user --upgrade pip
>> python3 -m pip --version
pip 19.1.1 from /home/anel/.local/lib/python3.6/site-packages/pip (python 3.6)
```

When using python3 or newer it is better to use [venv](https://docs.python.org/3.6/library/venv.html#module-venv).
```
$ sudo apt install python3-venv
$ python3 -m venv -h
```

* python2
```
$ sudo apt instal virtualenv (ili je pip install)
```
additionally (pip install virtualenwrapper) (see bellow more or in Project: django and nginx)

### 1) Create virtualenvironment
---
* python3 (`-m` => module script)
  This will place virtual env (a `bin/`, `lib/`, `lib64/`, `share/`, etc) in folder
 `python3 -m venv /home/anel/workspace/eacon/web-workspace/django/my_projects`
  Better to use shorter name `env` from current working directory in order to delete `rm -rf /path/to/env`
  So to create it use:
  `python3 -m venv env`
* python2
 `virtualenv project-flights`
 `virtualenv -h`
### 2) Get into virtualenvironment
----
`source env/bin/activate` # to get into (project-flights) environment and modify shell ; 
`echo $PATH /home/anel/ENV/bin`
* `which python && which python3`
  ```
  (env) anel@anel:~/my_playground/django/my_projects$ which python
  /home/anel/my_playground/django/my_projects/env/bin/python
  (env) anel@anel:~/my_playground/django/my_projects$ which python3
  /home/anel/my_playground/django/my_projects/env/bin/python3

  ```
Inside `env/bin` there are python2 and python3 exectuables.

**Note additinoally** Using [virtualenwrapper.sh](https://virtualenvwrapper.readthedocs.io/en/latest/)
```
$ mkvirtualenv env1
$ ls $WORKON_HOME
$ mkvirtualenv env2
$ workon env1
$ (env1)$ echo $VIRTUAL_ENV
```
### 3) Install django => "django-admin.py"
---
* Before starting the new project make sure you are in `env` and you have installed module django.
```
$ pip3 install django
$ python -m django --version # python3 is not working here
$ django-admin version
3.0.2
```
* Older tests:

  `$ (env)$ pip install django`
  // python3 (installed via pip install django without --upgrade django, but pip is updated (see above))\
  `$ python -m django --version`\
  2.2.1\
  // python 2\
  `$ python -m django --version`\
  1.11.20\
  `$(env)$ lssitepackages `# see the new packages\
  postmkvirtualenv is run when a new environment is created, letting you automatically install commonly-used tools.
  ```
  $ (env2)$ echo 'pip install sphinx' >> $WORKON_HOME/postmkvirtualenv
  $ (env2)$ mkvirtualenv env3
  $ (env3)$ which sphinx-build
  ```
* To start the [new project](https://docs.djangoproject.com/en/3.0/intro/tutorial01/#creating-a-project) we will have to be in `env`.
```
$(env) django-admin startproject enroll_students
$ (env) anel@anel:~/my_playground/django/my_projects/enroll_students$ pwd
/home/anel/my_playground/django/my_projects/enroll_students
$ (env) anel@anel:~/my_playground/django/my_projects/enroll_students$ ls -l
total 8
drwxr-xr-x 2 anel anel 4096 Jan 18 08:46 enroll_students
-rwxr-xr-x 1 anel anel  635 Jan 18 08:46 manage.py
$ (env) anel@anel:~/my_playground/django/my_projects/enroll_students/enroll_students$ ls -la
total 24
drwxr-xr-x 2 anel anel 4096 Jan 18 08:46 .
drwxr-xr-x 3 anel anel 4096 Jan 18 08:46 ..
-rw-r--r-- 1 anel anel  407 Jan 18 08:46 asgi.py
-rw-r--r-- 1 anel anel    0 Jan 18 08:46 __init__.py
-rw-r--r-- 1 anel anel 3115 Jan 18 08:46 settings.py
-rw-r--r-- 1 anel anel  757 Jan 18 08:46 urls.py
-rw-r--r-- 1 anel anel  407 Jan 18 08:46 wsgi.py
```
We will get directory with some auto-generated code. Top directory is name of project, and the same name bellow is for the application directory.



### 4) Run the application
---

When running this parent a [django-admin](https://docs.djangoproject.com/en/1.11/ref/django-admin)

* Start django application (`enroll_student`)
- Name of project `enroll_students` cannot be the same as name of app `enroll_student`
```
(env) anel@anel:~/my_playground/django/my_projects$ python enroll_students/manage.py startapp enroll_students
CommandError: 'enroll_students' conflicts with the name of an existing Python module and cannot be used as an app name. Please try another name.
(env) anel@anel:~/my_playground/django/my_projects$ python enroll_students/manage.py startapp enroll_student
(env) anel@anel:~/my_playground/django/my_projects$ ls
enroll_student  enroll_students  env  mysite_fligths
```
- Better run the starting the app from directory of the project `enroll_students`:
```
(env) anel@anel:~/my_playground/django/my_projects/enroll_students$ python3 manage.py startapp tet
(env) anel@anel:~/my_playground/django/my_projects/enroll_students$ ls
enroll_students  manage.py  tet
```
Even better is to create name of app with prefix `_app`: `_enroll_student_app`.
  This project directory has `settings.py` where can be foudn variable `INSTALLED_APPS` where we need to register our app.
  - Delete the app [link](https://stackoverflow.com/questions/35745220/how-to-remove-an-app-from-a-django-projects-and-all-its-tables):
    - If app is not registered, just `rm -rf`.
    - If yes we have to delete it from `settings.py`.

* Development server, automatic reload\
	`python manage.py runserver 0:8000  # for all hosts on network; without 0: only localhost`
  ```
    (env) anel@anel:~/my_playground/django/my_projects/enroll_students$ python manage.py runserver
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).

    You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.

    January 18, 2020 - 08:12:08
    Django version 3.0.2, using settings 'enroll_students.settings'
  ```
* Migrate tables from `INSTALLED_APPS` (`django.contrib.admin` etc), change `Time_zone` to `Europe/Sarajevo` \
`python manage.py migrate`
```
(env) anel@anel:~/my_playground/django/my_projects/enroll_students$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying sessions.0001_initial... OK
  # Start server again:
  (env) anel@anel:~/my_playground/django/my_projects/enroll_students$ python manage.py runserver
  Watching for file changes with StatReloader
  Performing system checks...

  System check identified no issues (0 silenced).
  January 18, 2020 - 09:48:02
  Django version 3.0.2, using settings 'enroll_students.settings'
  Starting development server at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.
```
We will later specify for which app we want migration ex. `python manage.py migrate _enroll_student_app`.
* Setting up the datebase:
- In order to use `mariadb` install : `pip install django mysqlclient` 
/// not working with pip3 /// mysqlclient-1.4.6
[digital-ocean-link](https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04)
- Change to mysql: [set database](https://docs.djangoproject.com/en/3.0/ref/settings/#databases) (support for [MariaDB](https://docs.djangoproject.com/en/dev/ref/databases/#mariadb-notes) in `django 3.0`) in `<project>/settings.py`\
  - change configuration for [auth-plugin](https://stackoverflow.com/a/54072297) in `/etc/mysql/conf.d`
  - For [not-auth-plugin solution](https://mariadb.com/kb/en/error-logging-in/).
- For `sqlite`:\
	`sudo apt-get install sqlite3 libsqlite3-dev`
- Start the mysql (mariadb) [how to install](https://linuxize.com/post/how-to-install-mariadb-on-ubuntu-18-04/), [mariadb repo](https://downloads.mariadb.org/mariadb/repositories/#distro=Ubuntu&distro_release=bionic--ubuntu_bionic&mirror=yongbok&version=10.4)
- Had some problems in configuring mariadb:
    Workaround:
    - Stop the service: `sudo systemctl stop mysql`
    - Start `mysqld_safe`
    ```
    sudo mysqld_safe --skip-grant-tables &
    ```
    - Log in into unprotected server `mysql`
    - Run: `flush privileges`;
    - Create new user: 
    ```
    $ create user eco_anel identified by `a`; # host=`%`
    $ select user,host from mysql.user \G 
    $ select * from mysql.global_priv\G 
    # we will have to add grants to user here
    $ show grants for 'eco_anel'@'%';
    $ select * from mysql.user where user='eco_anel'\G
    $ grant all privileges on *.* to 'eco_anel'@'%';
    $
    ```
    - Stop the mysqld_safe (or `sudo kill -9 PID`):
    `sudo mysqladmin shutdown`
    - Start the client: `mysql -u eco_anel -p`
    - `$create database`
    https://mariadb.org/authentication-in-mariadb-10-4/
- Guard settings using environment variable or [python-decouple](https://github.com/henriquebastos/python-decouple)
  - [talk about pass on github](https://www.youtube.com/watch?v=2uaTPmNvH0I&feature=youtu.be)
  - pip install what needed (`unipath`, `dj_database_url`) and change `settings.py`
  - exit scale mode and full screen ubuntu VM - `F11`
* From `_my_app/apps.py` add `MyAppConfig` to `settings.py`
* It is good to create a custom urls.py per application
* Django looks project-fligths/urls.py not our specific one, so we have to link it.
### 5) Minimal working Examples
  ```
  ./manage.py runserver
  ```

7) Migration => modification of your data in app.models.py
  configuration => settings.py INSTALLED_APPS

  '_flight_app.apps.FligthsAppConfig' see app/apps.py
  ./manage.py makemigrations will automtaically generate migrations (create databse table or similar)
  all changes made to database. Created 0001_initial.py file.
  id added automtically
  ```
  ./manage.py makemigrations
Migrations for '_fligths_app':
  _fligths_app/migrations/0001_initial.py
    - Create model Flight

    class Migration(migrations.Migration):

        initial = True

        dependencies = [
        ]

        operations = [
            migrations.CreateModel(
                name='Flight',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('origin', models.CharField(max_length=64)),
                    ('destination', models.CharField(max_length=64)),
                    ('duration', models.IntegerField()),
                ],
            ),
        ]

  ```
* ./manage.py migrate
* To see the list of commands use this:
    ```
    ./manage.py sqlmigrate _fligths_app 0001
    BEGIN;
    --
    -- Create model Flight
    --
    CREATE TABLE "_fligths_app_flight" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "origin" varchar(64) NOT NULL, "destination" varchar(64) NOT NULL, "duration" integer NOT NULL);
    COMMIT;

    ```
* settings.py
  DATABASES dictionary {}

8) ADD custom data
* python manage.py shell
    ```
      >>> from _fligths_app.models import Flight
      >>> f = Flight(origin="NY", destination="Sarajevo", duration=480)
      >>> f.save()
      >>> Flight.objects.all()
      >>> f=Flight.objects.first() # access flight f.origin
      >>> f.delete()
    ```
9) Add new Model and foreign keys and migrat
./manage.py makemigrations
 ```
 - Create model Airport
- Alter field destination on flight
- Alter field origin on flight
 ```
./manage.py migrate #apply migration
* Test it in Shell
  >>> a1 = Airport(code="NYC", city="New York")
  >>> a1
  <Airport: New York (NYC)>
  >>> a1.save()
  >>> a2.save()
  >>> Airport.objects.all()
  <QuerySet [<Airport: New York (NYC)>, <Airport: Sarajevo (SA)>]>
  >>> f=Flight(origin=a1, destination=a2, duration=343)
  >>> f
  <Flight: from New York (NYC) to Sarajevo (SA)>
  >>> a1.departures.all()
  <QuerySet [<Flight: from New York (NYC) to Sarajevo (SA)>]>
  >>> a2.departures.all()
  >>> a2.arrivals.all()
  <QuerySet [<Flight: from New York (NYC) to Sarajevo (SA)>]>

10) Using admin interface app/admin.py =>
    * register models we want to use
    * create user (login into admin site)
        ./manage.py createsuperuser anel


11) Redirecting reverse() and adding the name of routes
12) Template inheritance (Django Template Language DTL not Jinja2)
13) ManyToManyField
    * ./manage.py sqlmigrate _fligths_app 0003
    * Create custom user in shell
    >>> from _fligths_app.models import Flight, Airport, Passenger
    >>> f=Flight.objects.get(pk=1)
    >>>Passenger(first='Anel', last='Husakovic')
    >>> p.save()
    >>> p.flights.add(f)
    >>> p
    <Passenger: Anel Husakovic>
    >>> p.flights.all()
14) Forms
  csrf (403 error ) cross site request forgery
  * note that HttpResponseRedirect(reverse(is accepting tuple is argument (coma is needed)))
15) Login and authentication system
  * authentication and authorization app
        groups and users classes are visible in admin.site
  django.contrib.auth import authenticate, login, logout
  if not request.user.is_authenticated => display login.html page
  else user=request.user => render user.html with context

  def login_view(request):
    username=request.POST["username"] same pass
    user =authenticate(request, username=username, pasword=pass) # built in
    if user is not None:
      login(request, user) #built in function
  def logout_view(request):
    logout(request) #built in no need for session
    return render(request, "users/login.html", {"message","Logout"})
    user is a model built in with user.name, etc
    from django.contrib.auth.models import user
    user=User.objects.create_user("name", "mail","pass")
    user.save()
session: django.contrib.sessions (settings.py)

16) rm -rf .git uninitialize git
    Using `sqlite db browser GUI` nice
    Using LOGIN_REDIRECT_URL='home/' -> implied from django.contrib.url.views import login (built in variable when login)

17) django.db.models.signals import signal
    Using pass from view
    https://docs.djangoproject.com/en/2.2/ref/signals/
================== Old tutorial =============
Add app to settings.py
	'polls.apps.PollsConfig'
	python manage.py makemigrations polls
	(ENV) webuser@ubuntu:~/ENV/mysite$ python manage.py check
	System check identified no issues (0 silenced).

	python manage.py sqlmigrate polls 0001
BEGIN;
--
-- Create model Choice
--
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL);
--
-- Create model Question
--
CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
--
-- Add field question to choice
--
ALTER TABLE "polls_choice" RENAME TO "polls_choice__old";
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" integer NOT NULL REFERENCES "polls_question" ("id"));
INSERT INTO "polls_choice" ("choice_text", "votes", "id", "question_id") SELECT "choice_text", "votes", "id", NULL FROM "polls_choice__old";
DROP TABLE "polls_choice__old";
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
COMMIT;

Shell
	python manage.py shell
	>> from polls.models import Question, Choice
	>> Question.objects.all()
	>> from django.utils import timezone
	>>> q = Question(question_text="What's new?", pub_date=
)
	# Save the object into the database. You have to call save() explicitly.
	>>> q.save()

Adding __str__()
https://docs.djangoproject.com/en/1.11/ref/models/instances/#django.db.models.Model.__str__
https://docs.python.org/3/library/datetime.html#module-datetime
https://docs.djangoproject.com/en/1.11/ref/utils/#module-django.utils.timezone
https://docs.djangoproject.com/en/1.11/topics/i18n/timezones/

https://docs.djangoproject.com/en/1.11/intro/tutorial02/
shell:
>>> from polls.models import Question, Choice
>>> Question.objects.all()
# Make sure our custom method worked.
>>> q = Question.objects.get(pk=1)
>>> q.choice_set.all()
>>> q.choice_set.create(choice_text='Not much', votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text='The sky', votes=0)
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)

Databases
https://docs.djangoproject.com/en/1.11/ref/models/relations/
https://docs.djangoproject.com/en/1.11/topics/db/queries/#field-lookups-intro
https://docs.djangoproject.com/en/1.11/topics/db/queries/
https://docs.djangoproject.com/en/1.11/ref/models/fields/#foreign-key-arguments




Create a super user
python manage.py createsuperuser



Tutorial 3
https://docs.djangoproject.com/en/1.11/intro/tutorial03/
https://docs.djangoproject.com/en/1.11/ref/urlresolvers/#module-django.urls
https://docs.djangoproject.com/en/1.11/topics/templates/

Tutorial 4
https://docs.djangoproject.com/en/1.11/intro/tutorial04/
https://docs.djangoproject.com/en/1.11/topics/class-based-views/

Tutorial 5 tests-driven development
https://docs.djangoproject.com/en/1.11/intro/tutorial05/
https://docs.djangoproject.com/en/1.11/topics/testing/advanced/#django.test.utils.setup_test_environment
https://docs.djangoproject.com/en/1.11/topics/testing/tools/#django.test.LiveServerTestCase


=========================================
Project: How to use django with nginx
=========================================
Detailed procedures:

apt install python
apt install python-pip
apt install nginx
pip install virtualenv
pip install virtualenvwrapper
pip install uwsgi

adduser deploy
su - deploy
## for virtualenv projects
mkdir projects
## for django webpages
mkdir web

## add virtualenv environment variables to user deploy
which virtualenvwrapper.sh
/home/anel/.local/bin/virtualenvwrapper.sh
/home/webuser/.local/bin/virtualenvwrapper.sh

vi /home/deploy/.bashrc
...
export WORKON_HOME=~/projects
source /home/webuser/.local/bin/virtualenvwrapper.sh

mkvirtualenv p1
pip install django

## Test django version (django == module)
webuser@ubuntu:~/web$ workon p1
(p1) webuser@ubuntu:~/web$ python -m django --version
1.11.20

cd ~/web/
django-admin.py startproject d1
cd d1
./manage.py migrate
vi d1/settings.py

ALLOWED_HOSTS = ['localhost'] # see /sbin/ifconfig for the right address
...
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


./manage.py collectstatic
./manage.py runserver 0.0.0.0:5000
##open web brower to test

## quit virtualenv
deactivate

## change back to root or sudo -i
=========================================
mkdir -p /etc/uwsgi/sites_anel/

## create config file for uwsgi
vi /etc/uwsgi/sites_anel/p1.ini
[uwsgi]
uid = webuser
base = /home/%(uid)

chdir = %(base)/web/d1
home = %(base)/projects/p1
module = d1.wsgi:application

master = true
processes = 5

socket = /run/uwsgi/p1.sock
chown-socket = %(uid):www-data
chmod-socket = 660
vacuum = true

## test uwsgi with django
uwsgi --master --http :5000 --home /home/webuser/projects/p1 --chdir /home/webuser/web/d1 --module d1.wsgi:application
## open web brower to test, and you will find the images and styles are gone,
as uwsgi doesn't know where to service the static content from django.  We will get to that in nginx configuration part.
which uwsgi
/home/anel/.local/bin/uwsgi


## create a service to start uwsgi automatically
vi /etc/systemd/system/uwsgi.service
[Unit]
Description=uWSGI Emperor

[Service]
ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown webuser:www-data /run/uwsgi'
ExecStart=/home/anel/.local/bin/uwsgi --emperor /etc/uwsgi/sites-anel/
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target


systemctl daemon-reload
systemctl restart uwsgi.service
systemctl status uwsgi.service


=========================
nginx

sudo vim /etc/nginx/sites-available/p1.conf?

server {
  listen 9090;
  server_name 127.0.0.1;
  location = /favicon.ico { access_log off; log_not_found off; }
  location /static/ {
    root /home/webuser/web/d1;
  }
  location / {
    include uwsgi_params;
    uwsgi_pass unix:/run/uwsgi/p1.sock;
  }
}


sudo mkdir /etc/nginx/sites-enable
sudo ln -s /etc/nginx/sites-available/p1 /etc/nginx/sites-enable/


=================================================
502 gateway error

sudo tail -10 /var/log/nginx/error.log

change uwsgi.ini from 660 to 664 => nothing
change /etc/uwsgi/sites-anel/p1.ini from uid webuser to www-data, nothing

netstat -natup | grep LISTEN

Needed to add user www-data to nginx.conf



Reference:
http://logch.blogspot.com/2017/02/django-uwsgi-nginx-setup-in-ubuntu-16.html
https://www.youtube.com/watch?v=TYZfHn0MoXg



=======================
