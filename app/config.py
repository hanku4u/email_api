""" Configure the fast API settings here """
import os
from pathlib import Path
from functools import lru_cache
from typing import List
from pydantic import BaseSettings, Field

# bucket settings
bucket_prod = "emailAPI"
bucket_dev = "emailAPI"
s3_user = os.getenv("USER")
prod_bucket = f"/mnt/{s3_user}/s3/{bucket_prod}"
dev_bucket = f"/mnt/{s3_user}/s3/{bucket_dev}"

# migrate options
migrate_opt = os.getenv("MIGRATE_OP", None)


class Settings(BaseSettings):
    PROJECT_NAME: str = "emailAPI"
    PROJECT_VERSION: str = "0.0.0"  # WARNING!  DO NOT TOUCH! tbump will update this automatically.

    # security settings
    API_TOKEN_EXPIRE_MINUTES: int = Field(None, env="API_TOKEN_EXPIRE_MINUTES")

    # cache settings
    CACHE_CLEAR_TIME: int = Field(
        None, env="CACHE_CLEAR_TIME"
    )  # seconds to hold the cache
    CACHE_MAX_RESULTS: int = Field(
        None, env="CACHE_MAX_RESULTS"
    )  # count of cache items

    # database settings
    DATABASE_URI: str = Field("sqlite:///./emails.sqlite")

    class Config:
        # choose the .env file depending on how the api is being executed
        hostname = os.getenv("HOSTNAME")

        # check if there are migration options being passed to the setting through the env
        if migrate_opt:
            if migrate_opt == "prod":
                env_file =  f"{prod_bucket}/.env"
            elif migrate_opt == "dev":
                env_file = f"{dev_bucket}/.env"
            else:
                raise ValueError("wrong migrate option!")

        # proceed with the normal setting checks
        elif hostname and "vscode" in hostname:
            # the api is being run in local/dev mode
            env_file = Path(__file__).resolve().parent / ".env"

        elif hostname == "fastapi-data.clouddev":
            # its running on the dev cluster
            env_file = f"{dev_bucket}/.env"

        else:
            # its running on the dev cluster
            env_file =  f"{prod_bucket}/.env"

        # .env located in the same directory as this file
        env_file_encoding = "utf-8"


# use the cache for settings to cut down on i/o
@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()
