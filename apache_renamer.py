#!/usr/bin/env python

''' 
Script that connects out to servers and comments
out sections of welcome.conf to remove verbose
Apache welcome page
'''

import fabric, invoke, os, argparse

file_out = ""
credentials = ""

class ServerList():
    def __init__(self, unparsed_server_list):
        self.unparsed_server_list = unparsed_server_list
        self.server_list = []


def connect(hostname, username, password):
    # don't catch exceptions here, let them propagate up to main
    ssh_client = fabric.Connection(host=hostname, user=username, connect_kwargs={'password': password})
    sudopass = invoke.Responder(
            pattern=r'Password:',
            response=password + '\n',
    )
    ssh_client.run('sudo -H rootsh -i', pty=True, watchers=[sudopass])

    return ssh_client

def nav_n_edit(ssh_client, fo):
    try:
        exists = os.path.isfile("/etc/httpd/conf.d/welcome.conf")
        if exists:
            ssh_client.run("sed -i 's/Alias/#Alias/g' /etc/httpd/conf.d/welcome.conf")
            return True
        else:
            return False
    except:
        return False

def parse_args():
    global preparsed_server_list
    global credentials
    global file_out

    parser = argparse.ArgumentParser(description="Comment out Apache welcome pages")
    #parser.add_argument("filein", help="Full path to server list")
    parser.add_argument("--fileout", help="Path to save output to file")
    parser.add_argument("username", help="SSH username w/ rights")
    parser.add_argument("password", help="SSH password")

    args = parser.parse_args()

    #servers = args.filein
    file_out = args.fileout
    credentials = (args.username, args.password)

def main():
    parse_args()
    servers = ServerList()

    fo = open(file_out, "a")

    for server in servers.server_list:
        try:
            try:
                ssh_client = connect(server, credentials[0], credentials[1])
                edits = nav_n_edit(ssh_client, fo)
                if edits:
                    print "[+] " + server + " ---> Change made successfully"
                    fo.write("[+] " + server + " ---> Change made successfully")
                else:
                    print "[-] " + server + " ---> Unsuccessful"
                    fo.write("[-] " + server + " ---> Unsuccessful")
            except Exception as e:
                print e
        except Exception as e:
            print e

main()