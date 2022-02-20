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

    The code in this module was adapted from the example in the PRAW
    documentation, found at the following link:
    https://praw.readthedocs.io/en/stable/tutorials/refresh_token.html

    ----------

    This module contains functions related to Reddit authentication, including
    logging into accounts and authorising using 2FA.
"""

import praw
import random
import sys
import socket
import webbrowser
from configparser import NoSectionError
from praw.exceptions import MissingRequiredAttributeException
from typing import Dict, NoReturn
from .creds import add_refresh_token, create_ini, get_credentials
from .classes import Globals, Log, System
from .log import exit_with_log

global Globals, Log, System


def check_failure(client: object, params: Dict, state: str) -> NoReturn:
    """Checks for an authorisation failure, either due to a state mismatch or Reddit
    throwing an error in the return parameters.

    Arguments:
    - client (object)
    - params (dictionary)
    - state (string)

    No return value.
    """
    if state != params["state"]:
        send_message(
            client, f'State mismatch. Expected: {state} Received: {params["state"]}'
        )
        Log.new([f'State mismatch. Expected: {state} Received: {params["state"]}'])
        sys.exit()
    elif "error" in params:
        send_message(client, params["error"])
        Log.new([params["error"]])
        sys.exit()


def init() -> object:
    """Initialises the Reddit instance, creating a new praw.ini if none is found.

    No arguments.

    Returns: praw.Reddit instance.
    """
    try:
        return login()
    # Catch for invalid praw.ini, will create a new one then restart the program; the
    # restart is required due to current PRAW limitations. :'(
    except (NoSectionError, MissingRequiredAttributeException, KeyError):
        exit_with_log(
            [
                "praw.ini successfully created, program restart required for this"
                + " to take effect."
            ]
        ) if create_ini() else exit_with_log(
            [
                Log.warning(
                    "WARNING: Failed to create praw.ini file, something"
                    + " went wrong."
                )
            ]
        )


def login() -> object:
    """Handles the Reddit login and authorisation using credentials from praw.ini; will
    also handle initial refresh token setup if 2FA is enabled for the account.

    No arguments.

    Returns: praw.Reddit instance.
    """
    creds = get_credentials()

    constants = {
        "user_agent": f"{System.OS}:oscr:v{Globals.VERSION}:by /u/MurdoMaclachlan",
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "username": creds["username"],
    }

    if Globals.get(key="use_refresh_tokens"):

        # Indicates user will not have authorised OSCR yet
        if "refresh_token" not in creds.keys():
            reddit = praw.Reddit(
                password=creds["password"],
                redirect_uri=creds["redirect_uri"],
                **constants,
            )

            try:
                reddit.user.me()

            # If user has 2FA enabled but has not authorised OSCR
            except Exception as e:
                if str(e) != "invalid_grant error processing request":
                    Log.new(Log.warning([f"LOGIN FAILURE, ERROR IS: {e}"]))
                    sys.exit(0)

                # ngl idk wtf this does but it sure does do
                else:
                    state = str(random.randint(0, 65000))
                    scopes = ["history", "read", "edit"]
                    url = reddit.auth.url(scopes, state, "permanent")
                    Log.new(
                        [
                            "2FA enabled, but not authorised. OSCR will now open a"
                            + " tab in your browser to complete the login process."
                        ]
                    )
                    webbrowser.open(url)

                    client = receive_connection()
                    data = client.recv(1024).decode("utf-8")
                    param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
                    params = {
                        key:
                        value for (key, value) in [
                            token.split("=") for token in param_tokens
                        ]
                    }

                    # Check for an authorisation failure
                    check_failure(client, params, state)

                    refresh_token = reddit.auth.authorize(params["code"])
                    add_refresh_token(creds, refresh_token)
                    send_message(
                        client,
                        f"Refresh token: {refresh_token}. Feel free to close"
                        + " this page. This message is simply for success"
                        + " confirmation; it is not necessary to save your"
                        + " refresh_token, as OSCR has automatically done this.",
                    )

        # If user has 2FA enabled and has already authorised OSCR
        else:
            reddit = praw.Reddit(refresh_token=creds["refresh_token"], **constants)

    # If user does not have 2FA enabled
    else:
        reddit = praw.Reddit(password=creds["password"], **constants)

        try:
            reddit.user.me()
        except Exception as e:
            if str(e) != "invalid_grant error processing request":
                Log.new(Log.warning([f"LOGIN FAILURE, ERROR IS: {e}"]))
                sys.exit(0)
            else:
                Log.new(
                    [
                        Log.warning(
                            "2FA detected, but not enabled. Please run 'oscr -S' and"
                            + " set useRefreshTokens to True, then re-run OSCR."
                        )
                    ]
                )
                sys.exit(0)

    return reddit


def receive_connection() -> object:
    """Wait for and then return a connected socket. Opens a TCP connection on port 8080,
    and waits for a single client.

    No arguments.

    Returns: client object.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client: object, message: str) -> NoReturn:
    """Sends a message to the client and closes the connection.

    Arguments:
    - client (object)
    - message (string)

    No return value.
    """
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
    client.close()
