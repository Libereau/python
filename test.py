#!/usr/bin/python3.7
#coding:utf-8

import os
import pwd
import time
import getpass
import sqlite3

user = pwd.getpwuid(os.getuid()).pw_name

if os.geteuid() != 0:
    print("\n[!] Use sudo to run your script !\n")
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
#else :
#    exit("\n[!] Wrong password !\n")

time.sleep(2)
os.system('clear')

def menu():
    print("\r\n         ---------         Menu          ---------         \r\n")
    print("[1] - Show logins saved")
    print("[2] - Add logins")
    print("[3] - Delete logins")
    print("[4] - Exit\r\n")

    choix = input("Choice : ")

    try :
        choix = int(choix)
    except :
        print("[!] Format not standard")
        exit("[#] Exit")

    if choix == 1:
        show_ids()
    elif choix == 2:
        time.sleep(1)
        os.system('clear')
        save_id()
    elif choix == 3:
        time.sleep(1)
        os.system('clear')
        delete_id()
    elif choix == 4 :
        print("\r\n[#] Sortie\r\n")
        time.sleep(1)
        os.system('clear')
        exit()

    else:
        print("\n[!] Wrong input\n")


def saisie_login_passwd():
    print("\r\n[2] - Add logins")
    login = input("\r\nLogin : ")
    mdp = input("Password : ")
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

    print("\n[1] - Show logins saved\n")

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
        print("\n[1] - Show logins saved\n")

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

    time.sleep(1)
    os.system('clear')
    menu()

def delete_id():
    print("\n[3] - Delete logins\n")

    cursor.execute("""SELECT pass, login, service FROM keys""")
    for row in cursor:
        print(' - {2}, {1}, ******'.format(row[0], row[1], row[2]))

    id_del = input("\n[!] Service to delete : ")

    try :
        cursor.execute("""DELETE FROM keys WHERE service = ? """, ((id_del,)))
        conn.commit ()

    except :
        print("[!] Service not found")

    time.sleep(1)
    os.system('clear')
    menu()

menu()
