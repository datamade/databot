# DataBot

A Slack bot for DataMade.

### Run it locally

You need an Auth token for the team that you're wanting to post amazing things
into. For the lunch ideas, you'll also need various Yelp tokens.

**To get an auth token**

1. Go here: [https://api.slack.com/web](https://api.slack.com/web), scroll down
to the bottom and find the list of teams that you belong to.
2. Click the button to issue a token for the team that you want to put your bot
in and grab the token.

**Getting Yelp tokens**

1. Go [here](https://www.yelp.com/developers) and get a Consumer Key, Consumer
Secret, Token and Token Secret for the Yelp API.

**Run the app**

This app was developed using Python 3.4.3 but I'm pretty sure it'll work in
Python 2.7.x as well. Either way, get yourself a virtual enviromnent and
install the requirements: 

``` bash
# Using vanilla virtualenv 
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

# Using virtualenvwrapper
$ mkvirtualenv bot
$ pip install -r requirements.txt
```

In order for the app to run, it needs the various keys and tokens that you just
got set as environmental variables. So, before you can run it, you'll need to
set those:

``` bash
$ export SLACK_AUTH_TOKEN='theauthtoken'
$ export YELP_CONSUMER_KEY='key'
$ export YELP_CONSUMER_SECRET='secret'
$ export YELP_TOKEN='token'
$ export YELP_TOKEN_SECRET='token_secret'
```

To make those stick around between terminal sessions, you can add those lines
into your ``.bashrc`` file (or similar) and ``source`` it:

``` bash 
$ vim ~/.bashrc # add those to export statements
$ source ~/.bashrc
```

Now that all that is setup, you can run the app by doing ``python app.py`` with
your virtualenv activated.

