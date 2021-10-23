Additional Help and FAQ
========================

| **Where are the praw.ini, config file and data located?**
| On Linux and Mac, these are stored under ``/home/your_username/.oscr/``, with the data (log and statistics) under the subfolder ``data``. On Windows, they are stored under ``C:\Users\your_username\AppData\Roaming\oscr``, with the data under a ``data`` subfolder.

| **What if I already have a praw.ini on my computer?**
| Saving in an ``oscr`` subfolder prevents OSCR from overwriting any ini you might already have, and the program is designed to only pull from that file.
| If you are updating to 2.0.0 from a version of OSCR that had the praw.ini in just ``.config``, run ``oscr -F`` and it should automatically move the ``oscr`` section from your ``.config`` praw.ini to ``.config/oscr``, but note that this functionality was removed in version 2.1.0.

| **How can I contact the developer?**
| I'm reachable through ``murdomaclachlan@duck.com``. You can also `open an issue on GitHub <https://github.com/MurdoMaclachlan/oscr/issues>`_ if needed.
