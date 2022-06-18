"""
    Copyright (C) 2020-present, Murdo B. Maclachlan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.

    Contact me at murdomaclachlan@duck.com

    ----------

    This module contains functions relating to the handling the praw.ini file.
"""

from configparser import ConfigParser
from typing import Dict
from .classes import Globals, System
from .logger import Log

global Globals, Log, System


def add_refresh_token(creds: Dict, refresh_token: str) -> None:
    """Appends a given Reddit refresh token to praw.ini.

    Arguments:
    - refresh_token (string)

    No return value.
    """
    creds["refresh_token"] = refresh_token
    dump_credentials(creds)


def create_ini() -> bool:
    """Creates a new ini file based on user input.

    No arguments.

    Returns: boolean success status.
    """
    Log.new(
        "praw.ini missing, incomplete or incorrect. It will need to be created.",
        "INFO"
    )
    return dump_credentials(
        {
            "client_id": input("Please input your client id:  "),
            "client_secret": input("Please input your client secret:  "),
            # Since createIni is never called before the config is initialised, this is
            # safe to draw from:
            "username": Globals.get(key="user"),
            "password": input("Please input your Reddit password:  "),
            "redirect_uri": "http://localhost:8080/users/auth/reddit/callback",
        }
    )


def dump_credentials(creds: Dict) -> bool:
    """Outputs updated Reddit credentials to praw.ini.

    Arguments:
    - creds (dictionary)

    Returns: boolean success status.
    """
    Parser = ConfigParser()
    Parser["oscr"] = creds
    with open(f"{System.PATHS['config']}/praw.ini", "w+") as dump_file:
        Parser.write(dump_file)
    return True


def get_credentials() -> Dict:
    """Retrieves Reddit credentials from praw.ini.

    No arguments.

    Returns: dictionary containing credentials.
    """
    try:
        Parser = ConfigParser()
        Parser.read(f"{System.PATHS['config']}/praw.ini")
        return dict(Parser["oscr"])
    except FileNotFoundError:
        if create_ini():
            return get_credentials()
        else:
            Log.new(
                "Could not create praw.ini! Encountered a fatal error during ini"
                + " creation.",
                "FATAL"
            )
