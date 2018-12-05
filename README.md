# Jamf Remmina Sync

## Description
This is a basic Python script that lets you connect to a Jamf Server's API endpoint in order to create configuration
files for each computer in your JSS.

This makes it easy for Mac sysadmins who prefer Linux as their platform of choice (an admittedly tiny market) to have all
their devices in Remmina (and searchable) so they can easily be connected to via VNC screen sharing.

## How To Use It
Just run the python script (without any arguments) and it will ask you for the Jamf URL, a login name, and password.

The first time you run the script it will create new configurations for all your devices. Each subsequent time you run it, it
will overwrite the old configuration files, so last known IP addresses can easily be kept up to date. It will also add any
additional devices that were added to your JSS since the last time the script ran.

### Default Save Location
By default, this tool automatically saves configuration files to `~/.local/share/remmina`

Remmina will automatically scan this directory and load configuration files on each load.

### Naming
Configurations are named in the following order, based on whether or not the field is set in the Jamf database:
1. Computer's Assigned User (easiest for lookups from help support requests)
2. Computer Serial Number
3. Computer ID number

### Groups
This tool automatically places all generated configurations into a group named "JAMF", so in Remmina you can sort by group name
(or hide these entries altogether using the tree view).

## Future Improvements
* I plan to add command line argument parsing so this can be added to a chron job (or similar tool) to automatically 
keep entries updated on a regular interval. As of right now, this must be done manually.

* I also plan to add options for preferred naming conventions. The assigned user -> serial -> ID setup is ideal for my school
district's set-up, but I realize that is not necessarily the best for everyone as a default.

* I plan to add support for setting default VNC usernames and passwords for one-click connections
