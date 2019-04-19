class Application(object):
    """
    Much like a user object, but for the current application
    """

    __slots__ = ("id", "name", "icon", "description", "rpc_origins", "bot_public", "bot_require_code_grant", "owner")

    def __init__(self, dict):
        # Take out everything that we inherited from the GET /oauth2/applications/@me
        # Application info
        self.id = dict.get("id")
        self.name = dict.get("name")
        sef.icon = dict.get("icon")
        self.description = dict.get("description")

        # Rpc
        self.rpc_origins = dict.get("rpc_origins")

        # Bot
        self.bot_public = dict.get("bot_public")
        self.bot_require_code_grant = dict.get("bot_require_code_grant")

        # Owner
        self.owner = dict.get("owner")