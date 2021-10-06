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
import webbrowser
import sys
import socket
from typing import NoReturn
from .globals import Globals, Log, System
from .ini import addRefreshToken, getCredentials
global Globals, Log, System


# I don't know how half of this shit works but it does work so I don't care
def login() -> object:
    
    credentials = getCredentials()
    if "refresh_token" not in credentials.keys():
        
        reddit = praw.Reddit(
            user_agent = f"{System.OS}:oscr:v{Globals.VERSION}(by /u/MurdoMaclachlan)",
            client_id = credentials["client_id"],
            client_secret = credentials["client_secret"],
            username = credentials["username"],
            password = credentials["password"],
            redirect_uri = credentials["redirect_uri"]
        )
    
        try:
            reddit.user.me()
            return reddit
        
        except Exception as err:
            if (str(err) != 'invalid_grant error processing request'):
                print('LOGIN FAILURE')
            else:
                state = str(random.randint(0, 65000))
                scopes = ['history', 'read', 'edit']
                url = reddit.auth.url(scopes, state, 'permanent')
                Log.new(["2FA detected. OSCR will now open a window in your browser to complete the login process."])
                webbrowser.open(url)
    
                client = receiveConnection()
                data = client.recv(1024).decode('utf-8')
                paramTokens = data.split(' ', 2)[1].split('?', 1)[1].split('&')
                params = {key: value for (key, value) in [token.split('=') for token in paramTokens]}
    
                if state != params['state']:
                    sendMessage(client, f'State mismatch. Expected: {state} Received: {params["state"]}')
                    Log.new([f'State mismatch. Expected: {state} Received: {params["state"]}'])
                    sys.exit()
                elif 'error' in params:
                    sendMessage(client, params['error'])
                    Log.new([params['error']])
                    sys.exit()
    
                refreshToken = reddit.auth.authorize(params["code"])
                
                addRefreshToken(refreshToken)
                sendMessage(
                    client,
                    f"Refresh token: {refreshToken}. Feel free to close this page. This message is simply for success confirmation; " +
                    "it is not necessary to save your refresh_token, as OSCR has automatically done this."
                )
                
                return reddit
    else:
        reddit = praw.Reddit(
            user_agent = f"{System.OS}:oscr:v{Globals.VERSION}(by /u/MurdoMaclachlan)",
            client_id = credentials["client_id"],
            client_secret = credentials["client_secret"],
            username = credentials["username"],
            refresh_token=credentials["refresh_token"]
        )
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