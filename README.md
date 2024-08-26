
# **G:BOT SETUP**

Welcome to the G:Bot repository. The purpose of this readme is to help you set up the repo 
to run locally.


## CLONE THE REPOSITORY

Run `git clone https://github.com/benhga/gbot.git` in the folder that you want the repository.

## SET UP THE ENVIRONMENT

#### Virtual environment
In your terminal, run

`virtualenv venv`

to create a virtual environment with the name venv. 
Activate the environment with

`source venv/bin/activate`

Then install the required dependencies by running

`pip install -r requirements.txt`

#### MSSQL

Microsoft SQL databases requires a driver for connection. The one used in this project 
can be downloaded [here](https://www.microsoft.com/en-us/download/details.aspx?id=56567).

#### Flask environment

Make a copy of the `.env.template` file and save it as `.env`. Declare your environment variables in this file. _DO NOT COMMIT THIS FILE TO GITHUB_.

In the terminal, run the code 

`source .env` 

to set the environment variables.

## Bot Content

The content of the bot is stored in `gresponses.py`.
Change the dictionary keys and values to suit your purpose.
Then, in `bot_view.py`, change the values and logic to suit your needs.
The WebScrape.py file holds the necessary logic for web sraping but must be manipulated depending on the context.

## Seeding the database

The database must already exist. Run the code 

`python manage.py db upgrade`

to create the table in the required database.
## Running the bot

#### Server

For a basic example we run the bot from `ngrok`.
This can be downloaded at https://ngrok.com/download. Remember where the executable is stored.
CD to this directory in a separate terminal and run `./ngrok http 5000` if you are using a Flask development server or 
`./ngrok http 8000` if using a gunicorn server. 
To check functionality, click on the ngrok url and see that the website says "I'm working".

To start the app off a flask server, run 

`python manage.py runserver`.

To start the app of a gunicorn server run

`gunicorn --bind=0.0.0.0 --timeout 600 manage:app`.

#### Twilio

In Twilio, the webhook must be set to `<ngrok link>/message`.


~~~~
All that's left now is to send your bot a message and watch it reply!
~~~~
## DOCS
[Twilio](https://www.twilio.com/docs)

[Flask](https://flask.palletsprojects.com/en/1.1.x/)

