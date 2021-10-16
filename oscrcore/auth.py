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
    
    The code in this module was adapted from the example in the PRAW
    documentation, found at the following link:
    https://praw.readthedocs.io/en/stable/tutorials/refresh_token.html
"""

import praw
import random
import sys
import socket
import webbrowser
from configparser import NoSectionError
from praw.exceptions import MissingRequiredAttributeException
from typing import Dict, NoReturn
from .globals import Globals, Log, System
from .ini import addRefreshToken, createIni, getCredentials
from .log import exitWithLog
global Globals, Log, System


def checkFailure(client: object, params: Dict, state: str) -> NoReturn:
    if state != params['state']:
        sendMessage(client, f'State mismatch. Expected: {state} Received: {params["state"]}')
        Log.new([f'State mismatch. Expected: {state} Received: {params["state"]}'])
        sys.exit()
    elif 'error' in params:
        sendMessage(client, params['error'])
        Log.new([params['error']])
        sys.exit()


def init() -> object:
    try:
        return login()

    # Catch for invalid praw.ini, will create a new one then restart the program;
    # the restart is required due to current PRAW limitations. :'(
    except (NoSectionError, MissingRequiredAttributeException, KeyError):
        exitWithLog(
            ["praw.ini successfully created, program restart required for this to take effect."]
        ) if createIni() else exitWithLog(
            [Log.warning("WARNING: Failed to create praw.ini file, something went wrong.")]
        )


# I don't know how half of this shit works but it does work so I don't care
def login() -> object:
    
    creds = getCredentials()

    constants = {
        "user_agent": f"{System.OS}:oscr:v{Globals.VERSION}(by /u/MurdoMaclachlan)",
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "username": creds["username"],
    }

    if Globals.config["useRefreshTokens"]:

        # Indicates user will not have authorised OSCR yet
        if "refresh_token" not in creds.keys():
            reddit = praw.Reddit(
                password = creds["password"],
                redirect_uri = creds["redirect_uri"],
                **constants
            )

            try: reddit.user.me()

            # If user has 2FA enabled but has not authorised OSCR
            except Exception as e:
                if (str(e) != 'invalid_grant error processing request'):
                    Log.new(Log.warning([f"LOGIN FAILURE, ERROR IS: {e}"]))
                    sys.exit(0)

                # ngl idk wtf this does but it sure does do
                else:
                    state = str(random.randint(0, 65000))
                    scopes = ['history', 'read', 'edit']
                    url = reddit.auth.url(scopes, state, 'permanent')
                    Log.new(["2FA enabled, but not authorised. OSCR will now open a tab in your browser to complete the login process."])
                    webbrowser.open(url)

                    client = receiveConnection()
                    data = client.recv(1024).decode('utf-8')
                    paramTokens = data.split(' ', 2)[1].split('?', 1)[1].split('&')
                    params = {key: value for (key, value) in [token.split('=') for token in paramTokens]}

                    # Check for an authorisation failure
                    checkFailure(client, params, state)

                    refreshToken = reddit.auth.authorize(params["code"])
                    addRefreshToken(refreshToken)
                    sendMessage(
                        client,
                        f"Refresh token: {refreshToken}. Feel free to close this page. This message is simply for success confirmation; " +
                        "it is not necessary to save your refresh_token, as OSCR has automatically done this."
                    )

        # If user has 2FA enabled and has already authorised OSCR
        else:
            reddit = praw.Reddit(
                refresh_token = creds["refresh_token"],
                **constants
            )

    # If user does not have 2FA enabled
    else:
        reddit = praw.Reddit(
            password = creds["password"],
            **constants
        )

        try: reddit.user.me()
        except Exception as e:
            if (str(e) != 'invalid_grant error processing request'):
                Log.new(Log.warning([f"LOGIN FAILURE, ERROR IS: {e}"]))
                sys.exit(0)
            else:
                Log.new([Log.warning("2FA detected, but not enabled. Please run 'oscr -S' and set useRefreshTokens to True, then re-run OSCR.")])
                sys.exit(0)

    return reddit


# This connects to a server or something I don't know
def receiveConnection() -> object:
    """
    Wait for and then return a connected socket..
    Opens a TCP connection on port 8080, and waits for a single client.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


# Sends a message to the client I suppose
def sendMessage(client: object, message: str) -> NoReturn:
    """
    Send message to client and close the connection.
    """
    client.send(f'HTTP/1.1 200 OK\r\n\r\n{message}'.encode('utf-8'))
    client.close()
