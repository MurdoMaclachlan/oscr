Installation and Use
=====================

.. note:: OSCR was created on Linux and, given the developer has no access to other operating systems, support for Windows is limited and there is no support for MacOS.

Requirements
-------------

In order to install OSCR, you will need a version of Python installed. The original framework was written in 3.7, and current development uses 3.9, but anything 3.x onwards should work.

OSCR also relies on several python packages; configparser, PRAW, and alive_progress. Any version of configparser will do, but for PRAW you will need 7.1.2 or over, and for alive_progress you will need 1.6.1 or over.

Installation
-------------

To install OSCR,

1. Run either ``python -m pip install oscr`` or ``pip install oscr`` in your command line. It should automatically install the program as well as any dependencies.
2. Before doing anything else, you should now create an app for your Reddit account. You can do this by going to `the apps page in preferences <https://www.reddit.com/prefs/apps/>`_ and creating a new app:

    * Give it a name ("Oscar" or "OSCR" are easy to remember).
    * Choose "script".
    * Give it a description (which can really be anything you want).
    * Set an about url and redirect uri. The about url doesn't matter (I just linked the project's repository), and the redirect uri will not matter either; it is related to refresh tokens, which OSCR does not currently support.
    
3. Now, in your console, run the command ``oscr`` and you will be prompted to enter information for both config.json and praw.ini. The praw.ini will ask for your client id and client secret, which you can see on `the apps page <https://www.reddit.com/prefs/apps/>`_.

    Go to the page and scroll down until you find the bot you created. Underneath its name should be "personal use script", and below that a string of random characters. This is your client id. If you can't see a field that labeled "secret" with another, longer string of random characters after it, then click the edit button and it should appear (along with other fields you filled out when you were creating the bot).
    
    Once praw.ini is created, the program will exit and you will need to rerun it (this is because PRAW currently can't reload praw.ini files once Reddit() has been initialised).

Once it has been created, the contents of your praw.ini file should look something like this:

```
[oscr]
client_id=lI3fAkE7x82LiE
client_secret=4lS0f4Ke1234567894NdN0tR3aL
username=testuser
password=yourpasswordhere
```

You can check if they are correct by navigating to your config folder, which should be .config on Linux and Mac, and AppData on Windows.

4. Once you've rerun the program, each comment older than the cutoff should be deleted. By default, it will search every 10 minutes, and you can then either leave the program running in the background to delete posts in real time as they reach the cutoff, or you could turn recur off in your config file and manually run it every now and then.

Updating
---------

To update the program to a newer version, run ``python -m pip install --upgrade oscr`` or ``pip install --upgrade oscr`` in your command line.

Using the Latest Testing Version
---------------------------------

To use the latest testing version, download the `2.x branch files <https://github.com/MurdoMaclachlan/oscr/tree/2.x>`_, extract the archive you have downloaded, and use ``pip install .`` after navigating into the directory the files were extracted to.
