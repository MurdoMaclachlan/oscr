Additional Help and FAQ
========================

| **Where are the config file and data located?**
| On all operating systems, these are stored under ``/home/your_username/.oscr/``, with the data (log and statistics) under the subfolder ``data``.

| **Where is the praw.ini file?**
| On Linux this is under ``/home/your_username/.config/oscr``, it should be under the same folder on MacOS, and on Windows it is under ``C:\Users\your_username\AppData\Roaming\oscr``.

| **What if I already have a praw.ini on my computer?**
| Saving in an ``oscr`` subfolder prevents OSCR from overwriting this ini, and the program is designed to only pull from that file. If you are updating from a version of OSCR that had the praw.ini in just ``.config``, run ``oscr -F`` and it should automatically move the ``oscr`` section from your ``.config`` praw.ini to ``.config/oscr``.

| **How can I contact the developer?**
| I'm reachable through ``murdo@maclachlans.org.uk`` and ``murdomaclachlan@gmail.com`` (the first address is preferred). You can also `open an issue on GitHub <https://github.com/MurdoMaclachlan/oscr/issues>`_ if needed.
