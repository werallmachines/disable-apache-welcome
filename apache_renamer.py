#!/usr/bin/env python

''' 
Script that connects out to servers and comments
out sections of welcome.conf to remove verbose
Apache welcome page
'''

import paramiko, os, re, argparse

servers = []
file_out = ""
credentials = ""

class ServerList():
    server_list = ["204.236.222.215"]

    def parse_server_list(self, servers):
        pass

def connect(hostname, username, password):
    # don't catch exceptions here, let them propagate up to main
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password)

    return ssh_client

def nav_n_edit(ssh_client):
    try:
        #(stdin, stdout, stderr) = ssh_client.exec_command("sudo -H rootsh -i")
        #stdin.write(credentials[1] + "\n")
        # this will make the root directory visible with directory listing
        #(stdin, stdout, stderr) = ssh_client.exec_command("mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.bak")
        (stdin, stdout, stderr) = ssh_client.exec_command("sed -i 's/Alias/#Alias/g' /etc/httpd/conf.d/welcome.conf")

        return True
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
                s = connect(server, credentials[0], credentials[1])
                c = nav_n_edit(s)
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