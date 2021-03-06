#!/usr/bin/env python
from sys import argv
import json, signal, shlex
from cmd import Cmd
from b9y import B9y
#from b9y_dev import B9y

b9y_cli_release = "0.1.16"
default_user = "admin"
default_password = "changeme"
default_host="http://localhost:8080"
debug = False

def signal_handler(sig, frame):
        print('Bye!')
        exit(0)

def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]
    return opts

class b9y_prompt(Cmd):
    try:
        args = getopts(argv)
    except:
        exit(1)

    if '-h' in args:
        b9y_host = args['-h']
    else:
        b9y_host = default_host

    if '-u' in args:
        b9y_user = args['-u']
    else:
        b9y_user = default_user

    if '-p' in args:
        b9y_password = args['-p']
    else:
        b9y_password = default_password

    try:
        b9y = B9y(b9y_host, b9y_user, b9y_password)
    except:
        print("ERROR: unable to connect or credentials not valid")
        exit()

    b9y_instance, b9y_release = b9y.info()

    print("Bambleweeny CLI Version " + b9y_cli_release + "\nConnected to " + b9y_instance + " as " + b9y_user)

    prompt = "b9y v" + str(b9y_release) + "> "
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        print("Bye!")
        return True

    def help_exit(self):
        print('Exit the application.')

    def do_set(self, inp):
        items = shlex.split(inp, posix=False)
        if len(items) != 2:
            print("Error: need exactly two arguments.")
            return(None)
        r = self.b9y.set(items[0], items[1])
        if r:
            print("OK")

    def do_push(self, inp):
        items = shlex.split(inp, posix=False)
        if len(items) != 2:
            print("Error: need exactly two arguments.")
            return(None)
        r = self.b9y.push(items[0], items[1])
        if r:
            print("OK")

    def do_incr(self, inp):
        items = shlex.split(inp, posix=False)
        if len(items) != 1:
            print("Error: need exactly one argument.")
            return(None)
        r = self.b9y.incr(items[0])
        if r != None:
            print(str(r))
        else:
            print("Error")

    def do_get(self, inp):
        items = shlex.split(inp, posix=False)
        if len(items) != 1:
            print("Error: need exactly one argument.")
            return(None)
        r = self.b9y.get(items[0])
        print(str(r))

    def do_uget(self, inp):
        items = shlex.split(inp, posix=False)
        if len(items) != 2:
            print("Error: need exactly two arguments.")
            return(None)
        r = self.b9y.uget(items[0], items[1])
        print(str(r))

    def do_keys(self, inp):
        items = shlex.split(inp, posix=False)
        if len(items) == 0:
            r = self.b9y.keys()
        else:
            r = self.b9y.keys(items[0])
        for k in r:
            print(k)

    def do_pop(self, inp):
        items = shlex.split(inp, posix=False)
        if len(items) != 1:
            print("Error: need exactly one argument.")
            return(None)
        r = self.b9y.pop(items[0])
        print(str(r))

    def help_set(self):
        print("Set a Key. Example: set foo bar")

    def help_keys(self):
        print("List all Keys. You may specifiy an oprtional search string, 'grep style'.\nExample: keys\nExample: keys sys")

    def help_get(self):
        print("Get a Key. Example: get foo")

    def help_uget(self):
        print("** for admin use** Get a Key from a userid. Example: get foo 1")

    def help_push(self):
        print("Adds a value to a list / queue. Example: push foo bar")

    def help_pop(self):
        print("Retrieves an item from a list. Example: pop foo")

    def help_incr(self):
        print("Increase Counter. Example: incr ticket_number")

    def default(self, inp):
        if inp == 'q':
            return self.do_exit(inp)

        print "No idea what you want here. Type 'help' for available commands."

def main():
    signal.signal(signal.SIGINT, signal_handler)
    b9y_prompt().cmdloop()

if __name__ == '__main__':
    main()
