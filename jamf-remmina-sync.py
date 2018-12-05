#!/usr/bin/python
from sys import stdout
import getpass
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
from bs4 import BeautifulSoup
from os.path import expanduser

base_path = expanduser("~") + "/.local/share/remmina/"

def save_entry (name, ip_address, username="", password=""):
    config_file_text = """[remmina]
keymap=
ssh_auth=0
quality=9
disableencryption=0
postcommand=
ssh_privatekey=
disableclipboard=0
ssh_charset=
group=JAMF
name=$name
ssh_username=
precommand=
viewonly=0
proxy=
ssh_loopback=0
colordepth=32
protocol=VNC
ssh_server=
ssh_enabled=0
password=
username=
disablepasswordstoring=1
server=$server
showcursor=0
disableserverinput=0
window_height=480
viewmode=1
window_maximize=0
window_width=640""".replace ("$name", name).replace ("$server", ip_address).replace ("$username", username).replace ("$password", password)
    
    save_path = base_path + name + ".remmina"
    f = open (save_path, "w")
    f.write (config_file_text)
    f.close ()
    
server = raw_input ("JAMF server full URL: ")
login_name = raw_input ("JAMF server login name (requires API access permissions): ")
login_password = getpass.getpass ()

# Fix server input if necessary
if server.endswith("/"):
    server = server[:-1]
if not server.lower ().startswith ("h"):
    server = "https://" + server

print ""
print "API Connection URL: " + server + "/JSSResource/computers/"
print "API username: " + login_name
print "Output path: " + base_path
print ""

save_path_okay = raw_input("Use default remmina config directory? y/n: ").upper ()
if not save_path_okay.startswith ("Y"):
    base_path = raw_input("Enter path to remmina config directory: ")

print "Connecting to JSS..."

try:
    response = requests.get (server + "/JSSResource/computers/subset/basic", verify=False, auth=(login_name, login_password))
    bs = BeautifulSoup (response.text, "lxml")
    count = 0.
    total = len(bs.computers)
    for computer in bs.computers:
        count = count + 1
        output_string = "\rWriting number " + str(int(count)) + " of " + str(total) + " (" + str(round((count/total)*100,2)) + "% complete)"
        stdout.write (output_string)
        stdout.flush ()
        # Check for null
        if computer.username:
            computer_username = computer.username.text
            computer_id = computer.id.text
            computer_serial = computer.serial_number.text
            device_detail_response = requests.get (server + "/JSSResource/computers/id/" + computer_id, verify=False, auth=(login_name, login_password))
            device_detail_bs = BeautifulSoup (device_detail_response.text, "lxml")
            last_reported_ip = device_detail_bs.computer.general.last_reported_ip.text
            if last_reported_ip:
                if computer_username:
                    save_entry (computer_username, last_reported_ip)
                elif computer_serial:
                    save_entry (computer_serial, last_reported_ip)
                else:
                    save_entry (computer_id, last_reported_ip)
    print ""
except KeyboardInterrupt:
    print ""
    exit()
except Exception:
    print "Unable to connect to the JAMF server. Please check your credentials and try again."
