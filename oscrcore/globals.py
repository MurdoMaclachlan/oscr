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

    This module contains the basic global variables used by OSCR.
"""

from sys import platform
global DEFAULT_CONFIG, VERSION

DEFAULT_CONFIG = {
    "blacklist": [
        "claim",
        "claiming",
        "claim -- this was a automated action. please contact me with any questions.",
        "dibs",
        "done",
        "done -- this was a automated action. please contact me with any questions.",
        "unclaim",
        "unclaiming",
        "unclaim -- this was a automated action. please contact me with any questions.",
    ],
    "case_sensitive": False,
    "cutoff": 1,
    "cutoff_unit": 3600,
    "debug": False,
    "limit": 100,
    "log_updates": True,
    "os": platform,
    "print_logs": True,
    "recur": True,
    "regex_list": ["^(claim|done|dibs|unclaim)(?!(.|\n)*(treasure[\s-]*hunt|save))"],
    "report_totals": True,
    "subreddit_list": ["transcribersofreddit"],
    "unit": ["minute", "minutes", 60],
    "use_refresh_tokens": False,
    "use_regex": False,
    "user_list": ["transcribersofreddit"],
    "wait": 10,
}
VERSION = "2.2.0.9"
