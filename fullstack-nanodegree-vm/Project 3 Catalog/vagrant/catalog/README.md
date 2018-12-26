# Project 3: Item Catalog
### by Stephen Harris
Item Catalog project, part of the Udacity [Full Stack Web Developer
Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## What it is and does
Runs a web App named Software Development Languages Reference that is a reference to
software development languages that are categorized by language type.  A logged in user
based on their Facebook credentials can perform CRUD to maintain the reference data.

The backend code mainly refers to items, while the front talks about animals. Items
were used as a requirement from Udacity of the URLs that were required to be
functional.

## Required Libraries and Dependencies
The project code requires the following software:

* Python 2.7.x
* [SQLAlchemy](http://www.sqlalchemy.org/) 0.8.4 or higher (a Python SQL toolkit)
* [Flask](http://flask.pocoo.org/) 0.10.1 or higher (a web development microframework)
* The following Python packages:
    * oauth2client
    * requests
    * httplib2
    
You can run the project in a Vagrant managed virtual machine (VM) which includes all the
required dependencies (see below for how to run the VM). For this you will need
[Vagrant](https://www.vagrantup.com/downloads) and
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) software installed on your
system.

## Project contents
This project consists for the following files in the `catalog` directory:

* `README.md` - This file.
* `application.py` - The main entry point for the solution.
* `fb_client_secrets.json` - Client secrets for Facebook OAuth login.
* `/catalog` - Directory containing the `catalog` package.
    * `/static` - Directory containing CSS and Javascript for the website.
        Includes a copy of the [Material Design Lite](http://www.getmdl.io/)
        web framework by Google and
        [JavaScript Cookie](https://github.com/js-cookie/js-cookie/), a JavaScript
        API for handling cookies.
    * `/templates` - Directory containing the HTML templates for the website, using
        the [Jinja 2](http://jinja.pocoo.org/docs/dev/) templating language for Python.
		* `home.html` - Home page, displays the latest 6 languages details.
		* `login.html` -  Enables a user to login using their Facebook credentials.	
		* `item.html` - Displays a individual language and it's details.
		* `items.html` - Displays all languages associated with a language category.
		* `myItems.html` - Displays all languages that were added by a user.
		* `itemAdd.html` - Allows a logged in user to add a new language.
		* `itemDelete.html` - Allows a logged in user to delete a language.
		* `itemEdit.html` - Allows a logged in user to edit a language.
		* `layout.html` - Provides a common layout for all other HTML pages.
    * `__init__.py` - Initialises the Flask libraries and exposes routes.
    * `authenicate.py` - Handles the login and logout of users using OAuth.
    * `dbConnect.py` - Function for connecting to the database.
    * `model.py` - Defines the database classes and creates an empty database.
    * `apis.py` - JSON response restful.
    * `createSampleDB.py` - creates a default database with 12 categories/6 languages.
    * `views.py` - Provides the views of the data and forms for creating, editing and 
	deleting languages.

## How to Run the Project
Clone the repository to your desktop.  Open the GIT Bash and navigate to the project 
"catalog" directory and then enter the `vagrant` directory.

### Bringing the VM up
Bring up the VM with the following command:

```bash
vagrant up
```

The first time you run this command it will take awhile, as the VM image needs to
be downloaded.

You can then log into the VM with the following command:

```bash
vagrant ssh
```

More detailed instructions for installing the Vagrant VM can be found
[here](https://www.udacity.com/wiki/ud197/install-vagrant).

### Make sure you're in the right place
Once inside the VM, navigate to the tournament directory with this command:

```bash
cd /vagrant/catalog
```

### OAuth setup
In order to log in to the web app, you will need to get  a Facebook
OAuth app ID and secret. Facebook, go to [Facebook Login]
(https://developers.facebook.com/products/login).

Once you have your credentials, put the IDs and secrets in the `fbClientSecrets.json`.

You will now be able to log in to the app.

### Run application.py
On the first run of `application.py` there will be no database present, so it creates
one and populates it with the 12 categories/6 languages. On the command line do:

```bash
python application.py
```

It then starts a web server that serves the application. To view the application,
go to the following address using a browser on the host system:

```
http://localhost:8000/
```

You should see the 6 latest languages that were added to the database. Login using
your facebook credentials to perform CRUD operations to maintain the reference database.


### Shutting the VM down
When you are finished with the VM, press `Ctrl-D` to logout of it and shut it down
with this command:

```bash
vagrant halt
```

## Extra Credit Description
The following features are present to earn an extra credit from Udacity.

### Several JSON Endpoints to retrieve data based on RestFul APIs
* http://localhost:8000/catalog/categorys.json/ - returns all categories.
* http://localhost:8000/catalog/category/3.json/ - returns a single category based on ID.
* http://localhost:8000/catalog/categoryname/Interpreted%20languages.json/ - returns a single category by name.
* http://localhost:8000/catalog/items.json/ - returns all languages with details on each.
* http://localhost:8000/catalog/item/1.json/ - returns a single item and details based on ID.
* http://localhost:8000/catalog/itemname/Ada.json/ - returns a single item and details based on name.

## README
This README document is based on a template suggested by PhilipCoach in this
Udacity forum [post](https://discussions.udacity.com/t/readme-files-in-project-1/23524).
