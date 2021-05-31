Runtime Arguments
==================

OSCR presents a number of runtime arguments that can be passed in order to give the user more power over the way they run the program and provide certain unique functionalities. The arguments are as follows:

.. list-table::
   :header-rows: 1
   
   * - Name
     - Description
     - Priority
   * - --credits, -c
     - Lists everyone who has helped with the creation of the program.
     - 3
   * - --force-regex, -f
     - Forces OSCR to enable regex for one instance regardless of 'useRegex' configuration.
     - 8
   * - --format-old, -F
     - Rename old .cdremover directories, etc. to fit OSCR's new name, and move old praw.ini to new location. Only required if updating from the 0.x or 1.x branches.
     - 5
   * - --help, -h
     - Displays the list of runtime arguments in the console.
     - 1
   * - --no-recur, -n
     - Forces OSCR to run only one cycle regardless of 'recur' configration.
     - 8
   * - --print-logs, -p
     - Forces OSCR to print logs for one instance regardless of 'printLogs' configuration.
     - 8
   * - --reset-config, -R
     - Resets the config file to defaults.
     - 6
   * - --report-totals, -r
     - Forces OSCR to report total statistics for one instance regardless of 'reportTotals' configuration.
     - 8
   * - --settings, -S
     - Runs the settings menu.
     - 7
   * - --show-config, -s
     - Displays the contents of the config file.
     - 4
   * - --version, -v
     - Displays the currently installed version.
     - 2

The priority of each argument refers to how OSCR prioritises which ones to run, if there are any conflicting arguments passed. A lower number means higher priority. For example, if both --version and --credits are passed, --version will process first because it is higher priority. Similarly, if both --help and --print-logs are passed, --print-logs will have no effect, as --help is a "closing argument", meaning it stops the main program from running.

The lowest priority is 8; these are all arguments that affect the main program and will not have an effect if they are accompanied by any closing arguments. They are processed in alphabetical order.
