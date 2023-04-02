import logging

from dotenv import dotenv_values

from lib.enums import DefaultConfig


class Configuration:
    def __init__(self):
        # Load env variables
        env_config = dotenv_values()

        # Set debug property
        _debug = env_config.get("DEBUG") if env_config.get("DEBUG") else DefaultConfig.DEBUG
        logging.basicConfig(level=logging.INFO if _debug else logging.WARNING)

        logging.info(
            f"{len([el for el in env_config.values() if el])} out of {env_config.__len__()} parameters successfully"
            " loaded. Using default variables for the remaining ones"
        )
        if not env_config.get("DB_PASSWORD") or env_config.get("DB_PASSWORD") == DefaultConfig.DB_PASSWORD:
            logging.warning("Using default database password")

        # Build configuration with env variables they are set or with default ones
        self._host = env_config.get("HOST") if env_config.get("HOST") else DefaultConfig.HOST
        self._debug = _debug
        self._db_user = env_config.get("DB_USER") if env_config.get("DB_USER") else DefaultConfig.DB_USER
        self._db_password = env_config.get("DB_PASSWORD") if env_config.get("DB_PASSWORD") else DefaultConfig.DB_PASSWORD
        self._db_name = env_config.get("DB_NAME") if env_config.get("DB_NAME") else DefaultConfig.DB_NAME
        self._db_port = env_config.get("DB_PORT") if env_config.get("DB_PORT") else DefaultConfig.DB_PORT

        self._db_uri = f"postgresql://{self._db_user}:{self._db_password}@{self._host}:{self._db_port}/{self._db_name}"

        logging.info("Storing variables to .env file")
        with open("../.env", mode="w+") as env_f:
            env_f.writelines(
                [
                    "# environment variables\n",
                    "\n# app\n",
                    f"HOST = {self._host}\n",
                    f"DEBUG = {self._debug}\n",
                    "\n# database variables\n",
                    f"DB_USER = {self._db_user}\n",
                    f"DB_PASSWORD = {self._db_password}\n",
                    f"DB_NAME = {self._db_name}\n",
                    f"DB_PORT = {self._db_port}\n",
                ]
            )

        logging.info("Configuration completed")

    # All configuration attributes are read-only. Attribute values are set at initialization only
    @property
    def host(self):
        return self._host

    @property
    def debug(self):
        return self._debug

    @property
    def db_user(self):
        return self._db_user

    @property
    def db_password(self):
        return self._db_password

    @property
    def db_name(self):
        return self._db_name

    @property
    def db_port(self):
        return self._db_port

    @property
    def db_uri(self):
        return self._db_uri


c = Configuration()
