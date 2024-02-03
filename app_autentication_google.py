# The user details get print in the console.
# so you can do whatever you want to do instead
# of printing it

from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!/
xd5\xa2\xa0\x9fR"\xa1\xa8'

'''
  Set SERVER_NAME to localhost as twitter callback
  url does not accept 127.0.0.1
  Tip : set callback origin(site) for facebook and twitter
  as http://domain.com (or use your domain name) as this provider
  don't accept 127.0.0.1 / localhost
'''

app.config['SERVER_NAME'] = 'localhost:5000'
oauth = OAuth(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/google/')
def google():

  # Google Oauth Config
  # Get client_id and client_secret from environment variables
  # For developement purpose you can directly put it 
  # here inside double quotes
  GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
  GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

  CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
  oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={
      'scope': 'openid email profile'
    }
  )

  # Redirect to google_auth function
  redirect_uri = url_for('google_auth', _external=True)
  return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
  token = oauth.google.authorize_access_token()
  user = oauth.google.parse_id_token(token)
  print(" Google User ", user)
  return redirect('/')

if __name__ == "__main__":
  app.run(debug=True)
