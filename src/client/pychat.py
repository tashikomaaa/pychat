#!/usr/bin/env python3
import tkinter
import tkinter.simpledialog
import subprocess

class MyDialog(tkinter.simpledialog.Dialog):

    def body(self, master):
        tkinter.Label(master, text="HOST:").grid(row=0)
        tkinter.Label(master, text="PORT:").grid(row=1)

        self.e1 = tkinter.Entry(master)
        self.e2 = tkinter.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        self.e1.insert(tkinter.END, '159.89.236.235')
        self.e2.insert(tkinter.END, '33000')
        return self.e1 # initial focus

    def apply(self):
        host = self.e1.get()
        port = self.e2.get()
        subprocess.Popen("./client.py " + host + " " + port, shell=True)


root = tkinter.Tk()
root.title("PY-CHAT")
d = MyDialog(root)