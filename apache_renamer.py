#!/usr/bin/env python

''' 
Script that connects out to servers and comments
out sections of welcome.conf to remove verbose
Apache welcome page
'''

import fabric, invoke, os, re, argparse

servers = []
file_out = ""
credentials = ""

class ServerList():
    server_list = ["204.236.222.215"]

    def parse_server_list(self, servers):
        pass

def connect(hostname, username, password):
    # don't catch exceptions here, let them propagate up to main
    ssh_client = fabric.Connection(username@hostname, password="8008weiD!!")
    sudopass = invoke.Responder(
            pattern=r'\[sudo\] password for ', + username,
            response=password + '\n',
    )
    ssh_client.run('su -', pty=True, watchers=[sudopass])

    return ssh_client

def nav_n_edit(ssh_client):
    try:
        ssh_client.run('')
        return True
    except Exception as e:
        print e

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
                c = nav_n_edit(ssh_client)
                if c:
                    print "[+] " + server + " ---> Change made successfully"
                    fo.write("[+] " + server + " ---> Change made successfully")
                else:
                    print "[-] " + server + " ---> Unsuccessful"
                    fo.write("[-] " + server + " ---> Unsuccessful")
            except paramiko.ssh_exception.AuthenticationException as auth_error:
                print "[-] " + server + " ---> " + str(auth_error)
                continue
        except Exception as e:
            print e

main()