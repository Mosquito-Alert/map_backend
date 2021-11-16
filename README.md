# README

This repository includes the back-end for the Mosquito Alert web map. It is used to feed the data to the front-end apps.

## Setup

### Development setup

* Clone the repo
* Create a virtual environment
* Install dependencies (`pip install -r requirements.txt`)
* Run migrations (`python manage.py migrate`)
* Run the development web server (`python manage.py runserver`)

### Django structure

The back-end includes the following key directories:

* **project**. Includes the project settings and the main entry point for all URLs.
* **api**. Includes HTTP endpoints to feed the data to the front-end.

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact
