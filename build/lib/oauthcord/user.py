class User(object):
    """
    A user object, like the normal discord user object.
    """

    __slots__ = ("id", "name", "discriminator", "avatar_url", "flags", "premium_type", "mfa", "bot", "locale", "__dict__")

    def __init__(self, dict=None):
        # Take out everything that we inherited from the GET /users/@me
        # Account Info
        self.id = dict.get("id")
        self.name = dict.get("username")
        self.discriminator = dict.get("discriminator")
        self.avatar_url = "https://cdn.discordapp.com/avatars/{0}/{1}".format(self.id, dict.get("avatar"))

        # Profile
        self.flags = dict.get("flags")
        self.premium_type = dict.get("premium_type")
        self.mfa = dict.get("mfa_enabled")

        # Bot / User
        self.bot = dict.get("bot")

        # Location
        self.locale = dict.get("locale")
    
    def __str__(self):
        """
        Returns `name#discrim`
        """
        return "{0.name}#{0.discriminator}".format(self)
    
    def is_bot(self):
        """
        Returns a `bool`. Identical to `discord.Member.bot`
        """
        return self.bot