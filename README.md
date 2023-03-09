# EZ Approve Lite Django Project

A Simple Django project to support process of selling client's items. Client was not available to review items in person. Designed to be deployed with NGINX on an EC2 instance with AWS.

## Python Module Dependencies
- python3.10.6
- python3-venv
- Django4.1.7
- djano-crispy-forms
- crispy-bootstrap4
- gunicorn20.1.0
- Pillow9.4.0

## Services
- supervisor4.2.1
- nginx1.22.1

## Other
- jQuery3.6.3
- bootstrap4

Thanks to the Django team for the great documentation. https://docs.djangoproject.com/en/4.1/

Thanks to Cloud With Django YouTube channel for a step by step guide on EC2 deployment and getting started with gunicorn and supervisor. https://www.youtube.com/@cloudwithdjango

Thanks as well as Jaysha on OrdinaryCoders blog for the guides on authentication and login. Great how-to's and explanations: https://ordinarycoders.com/blog/Jaysha


## Setting Up the Environment on Linux

Ensure you have python3.10.6

If you do not have python virtual environment run `sudo apt install python3-venv`

Create a virtual environment using `python3 -m venv <env_name>`

Inside the virtual environment run the following to install required packages:
- `pip install django`
- `pip install django-crispy-forms`
- `pip install crispy-bootstrap4`
- `pip install pillow`
- `pip install gunicorn`

Download NGINX by running `sudo apt-get -y install nginx`

Verify NGINX is running by entering your machines IP address into a browser and see the NGINX welcome page

If you don't know your IP, run `ifconfig`

You may need to run `sudo apt install net-tools` if runnign `ifconfig` gives you an error

Run `sudo apt install supervisor` to install supervisor to manage server background processes

To create a configuration file run `cd /etc/supervisor/conf.d/`

Then run `sudo touch gunicorn.conf`

Open the file in your editor of choice. I chose to run `sudo vim gunicorn.conf`

Paste the following code into your file:
```
[program:gunicorn]
directory=/home/<user>/<project_folder>
command=/home/<user>/<env_name>/bin/gunicorn --workers 3 --bind unix:/home/<user>/<project_folder_path>/app.sock <project_name>.wsgi:application  
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/gunicorn.err.log
stdout_logfile=/var/log/gunicorn/gunicorn.out.log

[group:guni]
programs:gunicorn
```
When pasting the above code, make sure to replace `<user>`, `<env>`, `<project_folder>`, `<project_folder_path>`, and `<project_name>` with the appropriate replacements.
For the example project directory inside of my /home/user/
```
ezApprove
.
|____ezApprove
|  |______init__.py
|  |____app.sock    <-- [see 1.]
|  |____asgi.py
|  |____settings.py    <-- [see 2.]
|  |____urls.py
|  |____wsgi.py
|
|____env    <-- [see 3]
|  |____virtual environment files.....
|
|____store
|  |____store app files.....
|
|____.gitattributes
|____.gitignore
|____manage.py
|____README.md    <-- if you are reading this, you are here :)
```

For above:

1. So my .conf file will have "--bind unix:/home/jingram/ezApprove/ezApprove/app.sock"

2. This is where you will see "WSGI_APPLICATION = 'ezApprove.wsgi.application'" so I will have "ezApprove.wsgi:application" in my .conf file

3. This is my environment name so in my .conf file I have "command=/home/jingram/env/bin/gunicorn"

Once the .conf file is created return to the user directory with `cd`

Run `cd /var/log/` to begin creating log files for supervisor

Run `sudo mkdir gunicorn` to make the directory

Run `cd gunicorn` to enter the directory

Run `sudo touch gunicorn.err.log gunicorn.out.log` to make the log files

To start supervisor running on your .conf file, run `sudo supervisorctl reread`

Then `sudo supervisorctl update`

And finally `sudo supervisor status`

The terminal should say `guni:gunicorn                    RUNNING   pid 19537, uptime 0:54:20` with your unique service uptime and pid

If the terminal says `STARTING`, `FATAL`, or `BACKOFF` your .conf file may be wrong.

Run `cd ..` until you are in the `/etc` directory

Run `cd nginx`

To modify NGINX configuration file run `sudo vim nginx.conf`

At the top of the file change user from `www-data` to `root` or a user of your chosing

Now `cd sites-available`

And `sudo touch django.conf`

Open for editing with `sudo vim django.conf`

Paste the following into the file:

```
server{
	listen 80;
	server_name <server ip>;
	location / {
		include proxy_params;
		proxy_pass http://unix:/home/<user>/<project_folder_path>/app.sock;
	}
}
```
The `<project_folder_path>` and `<user>` should be the same as in supervisor's gunicorn.conf file

The `<server_ip>` should be your machine ip if you are running this locally, or your EC2 instance public ip address. There are also other ways of setting this up with DNS and https.

To allow nginx to test nginx.conf file, run `sudo nginx -t`

If successful, run `sudo ln django.conf /etc/nginx/sites-enabled` this creates a symlink between your sites-available django.conf and django.conf that will appear in sites-enabled. This is basically creating a 'shortcut' in sites-enabled to our django.conf in site-available.

Next reload NGINX with `sudo systemctl reload nginx`

Using a browser, point it to your IP address and now you should see the django site. The ezApprove site doesn't use the / url so make sure to navigate to `http://<your_IP>/store` to see the login page. This may change in future commits.

## Notes

After you have all this set up, you will need to apply migrations to the database. To do this navigate to the directory containing manage.py and run `python manage.py migrate`. You may run into permissions errors so check the database permissions or consider running everything as the root user from the start especially if you are setting this up on an EC2 instance.

You will need to create a superuser to be the site admin. To do this run `python manage.py createsuperuser` and follow the prompts.

Lastly if you are deploying your Django app to production make sure to avoid security issues by reading https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment

Many other helpful tips can be found at https://docs.djangoproject.com/en/4.1/howto/deployment/