#!/usr/bin/python3.7
#coding:utf-8


import os
import pwd
import time
import getpass
import sqlite3
from colorama import Fore, Back, Style


if os.geteuid() != 0:
    print("\n" + Fore.RED + "[!] Use sudo to run your script !\n")
    exit(1)

os.system('clear')

print("\n[#] Password Manager v0.2")

try :
    conn = sqlite3.connect('/root/Documents/Programmes/python/pass_manager.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS keys (pass TEXT PRIMARY KEY, login TEXT, service TEXT)""")
    print("\r\n[+] Database created !")

except :
    print("\r\n[!] Your database already exist.")


time.sleep(2)
os.system('clear')

def menu():
    print("\r\n"+Style.BRIGHT+"         ---------         Menu          ---------         \r\n")
    print("[1] - Show logins saved")
    print("[2] - Add logins")
    print("[3] - Delete / Update logins")
    print("[4] - Find password associated with service")
    print("[5] - Exit\r\n")

    choix = input("Choice : ")

    try :
        choix = int(choix)
    except :
        print("\n" + Fore.RED + "[!] Format not standard" + Style.RESET_ALL)
        exit("...\n")

    if choix == 1:
        print(Style.RESET_ALL)
        show_ids()
    elif choix == 2:
        print(Style.RESET_ALL)
        time.sleep(1)
        os.system('clear')
        save_id()
    elif choix == 3:
        print(Style.RESET_ALL)
        time.sleep(1)
        os.system('clear')
        delete_id()
    elif choix == 4:
        print(Style.RESET_ALL)
        time.sleep(1)
        os.system('clear')
        find_service()
    elif choix == 5 :
        print("\r\n[#] Sortie\r\n")
        time.sleep(1)
        os.system('clear')
        exit()

    else:
        print("\n" + Fore.RED + "[!] Wrong input\n" + Style.RESET_ALL)


def saisie_login_passwd():
    print(Style.BRIGHT)
    print("\r\n[2] - Add logins")
    print(Style.RESET_ALL)
    login = input("\r\nLogin : ")
    mdp = getpass.getpass("Password : ")
    service = input("Service : ")

    return login, mdp, service


def save_id():
    l, m, s = saisie_login_passwd()

    cursor.execute("""INSERT INTO keys(pass, login, service) VALUES(?, ?, ?)""", (m, l, s))
    conn.commit()

    time.sleep(1)
    os.system('clear')
    menu()

def show_ids():
    time.sleep(1)
    os.system('clear')
    print("\n"+ Style.BRIGHT + "[1] - Show logins saved" + Style.RESET_ALL + "\n")

    cursor.execute("""SELECT pass, login, service FROM keys""")

    if cursor.fetchall() != [] :
        cursor.execute("""SELECT pass, login, service FROM keys""")
        for row in cursor:
            print(' # {2}, {1}, ****** '.format(row[0], row[1], row[2]))

        show_pass = input("\nWould you like to see the passwords ? [y/N] - ")

        if (show_pass == "y" or show_pass == "Y"):
            print('')
            cursor.execute("""SELECT pass, login, service FROM keys""")
            for row in cursor:
                print(' # {2}, {1}, {0}'.format(row[0], row[1], row[2]))

        c = input("\r\nBack to menu ? [y/N] - ")

        while ((c == "n") or (c == "N")):
            os.system('clear')
            print("\n"+ Style.BRIGHT + "[1] - Show logins saved\n" + Style.RESET_ALL)

            cursor.execute("""SELECT pass, login, service FROM keys""")
            for row in cursor:
                print(' # {2}, {1}, ******'.format(row[0], row[1], row[2]))

            show_pass = input("\nWould you like to see the passwords ? [y/N] - ")
            print('')
            if (show_pass == "y" or show_pass == "Y"):
                cursor.execute("""SELECT pass, login, service FROM keys""")
                for row in cursor:
                    print(' # {2}, {1}, {0}'.format(row[0], row[1], row[2]))

            c = input("\nBack to menu ? [y/N] - ")

    else:
        print("[!] Empty database")

    time.sleep(1.5)
    os.system('clear')
    menu()

def delete_id():
    print("\n" + Style.BRIGHT + "[3] - Delete / Modify logins\n" + Style.RESET_ALL)

    print("Would you like to : ")
    print("1 - Delete")
    print("2 - Modify\n")
    choice = input("")
    choice = int(choice)

    if choice == 1:
        time.sleep(1)
        os.system('clear')
        print(Style.BRIGHT)
        print("\n[3] - Delete")
        print(Style.RESET_ALL)

        cursor.execute("""SELECT pass, login, service FROM keys""")
        for row in cursor:
            print(' - {2}, {1}, ******'.format(row[0], row[1], row[2]))

        id_del = input("\n[!] Service to delete : ")

        try :
            cursor.execute("""DELETE FROM keys WHERE service = ? """, ((id_del,)))
            conn.commit ()

        except :
            print(Fore.RED+"[!] Service not found" + Style.RESET_ALL)

    elif choice == 2:
        time.sleep(1)
        os.system('clear')
        print(Style.BRIGHT)
        print("[3] - Modifying password\n")
        print(Style.RESET_ALL)
        service_list = []

        # On ré affiche les login / mdp / service
        cursor.execute("""SELECT pass, login, service FROM keys""")
        for row in cursor:
            print(' - {2}, {1}, ******'.format(row[0], row[1], row[2]))
            service_list.append(row[2])

        #Demande de saisir du service pour récuperer la ligne
        # (utilisation d'une liste pour vérifier si le service entré existe ?)

        id_update = input("\n[+] Service's password to modify: ")

        while not id_update in service_list:
            print("\n"+Fore.RED+"Service not found"+ Style.RESET_ALL)

            id_update = input("\n[+] Service's password to modify: ")

        cursor.execute("""SELECT pass, login, service FROM keys""")
        old_pass = ""
        for row in cursor:
            if row[2] == id_update :
                print('\n - {2}, {1}, ******'.format(row[0], row[1], row[2]))
                old_pass = row[0]

        # Saisie du nouveau password
        new_pass = getpass.getpass("\n[!] New password : ")

        try :
            #Update de la bdd :
            cursor.execute("""UPDATE keys SET pass = ? WHERE pass = ? """, ((new_pass, old_pass)))
            print('\nUpdating...')
            time.sleep(1)
            print("\nDone !")
            time.sleep(0.5)

        except :
            print("\n" + Fore.RED + "[!] Error while updating row..")

    time.sleep(1)
    os.system('clear')
    menu()

def find_service():
    print(Style.BRIGHT)
    print("\n[4] - Find password associated with service\n")
    print(Style.RESET_ALL)
    show_service = input("Service : ")

    cursor.execute("""SELECT pass, login, service FROM keys""")
    for row in cursor:
        if row[2] == show_service :
            print('\n # {2}, {1}, {0}'.format(row[0], row[1], row[2]))

    print("\n")
    time.sleep(3)
    os.system('clear')
    menu()

if __name__ == "__main__":
    menu()
