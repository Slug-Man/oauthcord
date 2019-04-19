# This example uses flask, but any other library is fine
from flask import redirect, request
from oauthcord import oauth

# Create a basic app
app = oauth.App(client_id="id", client_secret="secret", scope="scope", redirect_uri="redirect uri")

# R=Direct the user to login. Using the flask redirect() function for this example
redirect(app.discord_login_url)

# Once the user has logged in, a code will appear in their url bar. This is what we use for the App.get_access_code function.
login_code = request.args.get("code")

# Get the access token for a user, this is needed
access_token = app.get_access_token(code=login_code)

# You are now able to get the user. App.get_user takes a user id (required to be in the cache) or a valid access token.
user = app.get_user(access_token)

# Out variable `user` is an oathcord.User() object. This has all the attributes discord sends us. Also comes with some functions.
# For now we will just get the user's info as a dict.
print(user.to_json())

# Once you are done with the user, you can log them out.
user.logout()



