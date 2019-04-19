# Packages
import requests

# Locals
from oauthcord.user import User
from oauthcord.application import Application
    
class App(object):
    """
    The main oauth class.
    """

    __slots__ = ("client_id", "client_secret", "scope", "redirect_uri", "discord_login_url", "discord_token_url", "discord_api_url","users")

    def __init__(self, **kwargs):
        # Cache
        self.users = {}

        # Discord Client Stuff
        self.client_id = kwargs.get("client_id")
        self.client_secret = kwargs.get("client_secret")
        self.scope = kwargs.get("scope")
        self.redirect_uri = kwargs.get("redirect_uri")

        # Discord base links
        self.discord_login_url = "https://discordapp.com/api/oauth2/authorize?client_id={0.client_id}&redirect_uri={0.redirect_uri}&response_type=code&scope={0.scope}".format(self)
        self.discord_token_url = "https://discordapp.com/api/v6/oauth2/token"
        self.discord_api_url = "https://discordapp.com/api/v6"

    def get_access_token(self, code, option=None) -> dict:
        """
        Get a user's access token.
        Can be used to get user objects.
        """
        payload = {
            'client_id':self.client_id,
            'client_secret':self.client_secret,
            'grant_type': 'authorization_code',
            'code':code,
            'redirect_uri':self.redirect_uri,
            'scope':self.scope
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        access_token = requests.post(url=self.discord_token_url, data=payload, headers=headers)
        json = access_token.json()
        return json.get("access_token") if option is None else json.get(option)
    
    def refresh_token(self, refresh_token) -> dict:
        """
        Refresh the token if the `expires_in` ends.
        """
        payload = {
            'client_id':self.client_id,
            'client_secret':self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token':refresh_token,
            'redirect_uri':self.redirect_uri,
            'scope':self.scope
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        res = requests.post(url=self.discord_token_url, data=payload, headers=headers)
        return res.json()
     
    def get_user(self, token_or_id) -> User:
        """
        Return the user object for an access token.
        """
        if isinstance(token_or_id, str):
            url = [self.discord_api_url+"/users/@me"]
            if "guild" in self.scope:
                url.append(self.discord_api_url+"users/@me/guilds")

            headers = {
                'Authorization': f"Bearer {token_or_id}"
            }

            user_object = requests.get(url=url, headers=headers)    
            user_json = user_object.json()
            id = user_json["id"]
            self.users[id] = user_json
            return User(user_json) if user_json.get("message") != "401: Unauthorized" else user_json
        elif isinstance(token_or_id, int):
            for item in self.users.keys():
                if item != str(token_or_id): 
                    continue
                else:
                    u = self.users[item]
                    return User(u)
        else:
            got = type(token_or_id)
            raise ValueError("Expected type str or int, got %s" % got)
    
    def get_current_application(self, access_token) -> Application:
        """
        Get current application.
        """
        url = self.discord_api_url+"oauth2/applications/@me"

        headers = {
            'Authorization': f"Bearer {access_token}"
        }

        application_object = requests.get(url=url, headers=headers)
        application_json = application_object.json()
        return Application(application_json) if application_json.get("message") != "401: Unauthorized" else application_json
