import os
import requests
import websocket
import json
import random
from requests_oauthlib import OAuth1

SLACK_AUTH_TOKEN = os.environ['SLACK_AUTH_TOKEN']
SLACK_REALTIME_ENDPOINT = 'https://slack.com/api/rtm.start'

YELP_CONSUMER_KEY = os.environ['YELP_CONSUMER_KEY']
YELP_CONSUMER_SECRET = os.environ['YELP_CONSUMER_SECRET']
YELP_TOKEN = os.environ['YELP_TOKEN']
YELP_TOKEN_SECRET = os.environ['YELP_TOKEN_SECRET']

FORECAST_KEY = os.environ['FORECAST_KEY']

YELP_URL = 'http://api.yelp.com/v2/search'
FORECAST_PATTERN = 'https://api.forecast.io/forecast/{0}/{1}'

def getForecast(lat_lon=[]):
    
    if lat_lon:
        lat_lon = ','.join(lat_lon)
    else:
        lat_lon = '41.888666,-87.634702'
    
    req_url = FORECAST_PATTERN.format(FORECAST_KEY,lat_lon)
    forecast = requests.get(req_url)

    icon_text = forecast.json()['currently']['icon']
    summary = forecast.json()['currently']['summary']

    with open('icons/{0}.txt'.format(icon_text), 'r') as f:
        icon = f.read()
    
    return icon, summary

def getLunch(lat_lon=[], 
             search_term='lunch', 
             location=None):
    latitude = '41.888156' 
    longitude = '-87.636209'
    if lat_lon:
        latitude, longitude = lat_lon
    
    header_auth = OAuth1(YELP_CONSUMER_KEY, 
                         YELP_CONSUMER_SECRET, 
                         YELP_TOKEN, 
                         YELP_TOKEN_SECRET, 
                         signature_type='auth_header')

    params = {
        'll': '{0},{1}'.format(latitude, longitude),
        'term': search_term,
        'radius_filter': 1000,
    }
    if location:
        if 'chicago' not in location.lower():
            location = '{0} Chicago IL'.format(location)
        params['location'] = location
        del params['ll']
    lunch = requests.get(YELP_URL, 
                         params=params, 
                         auth=header_auth)
    
    choices = [b for b in lunch.json()['businesses'] if not b['is_closed']]
    if choices:
        choice = random.choice(choices)

        message = "{0}. It's at {1}. Here's some more info: {2}"\
                .format(choice['name'], choice['location']['address'][0], choice['url'])
    else:
        message = None
    
    return message

if __name__ == "__main__":
    params = {'token': SLACK_AUTH_TOKEN}
    socket = requests.get(SLACK_REALTIME_ENDPOINT, params=params)
    
    channel_lookup = {c['id']: c['name'] for c in socket.json()['channels']}
    user_lookup = {u['id']: u['name'] for u in socket.json()['users']}
    
    databot_id = [u['id'] for u in socket.json()['users'] if u['name'] == 'databot']

    ws = websocket.WebSocket()
    ws.connect(socket.json()['url'])

    while True:
        result = json.loads(ws.recv())
        message_id = 1
        if result.get('type') == 'message' and not result.get('subtype'):
            channel_name = channel_lookup.get(result['channel'], 'general')
            user_name = user_lookup.get(result['user'], '')
            lower_text = result['text'].lower()
            print(lower_text)
            if 'databot' in lower_text and 'lunch' in lower_text:
                words = lower_text.split(' ')
                try:
                    search_term = words[words.index('eat') + 1]
                except ValueError:
                    search_term = 'lunch'
                
                try:
                    location = ' '.join(words[words.index('near') + 1:])
                except ValueError:
                    location = None
                
                message = getLunch(location=location, search_term=search_term)
                if message:
                    formatted = "Hey {0}. Why don't you try this place? {1}"\
                                .format(user_name, message)
                else:
                    formatted = "Sorry, {0}. I couldn't find anythin matching that search"\
                                .format(user_name)
                postback = {
                    'id': message_id,
                    'type': 'message',
                    'channel': result['channel'],
                    'text': formatted,
                }
                ws.send(json.dumps(postback))
                message_id += 1
            
            if 'databot' in lower_text and 'weather' in lower_text:
                icon, summary = getForecast()
                postback = {
                    'id': message_id,
                    'type': 'message',
                    'channel': result['channel'],
                    'text': '{0}```{1}```'.format(icon, summary)
                }
                ws.send(json.dumps(postback))
                message_id += 1
