import socket
import tkinter as Tk
from tkinter import *
import datetime
from functools import partial
def send():
    global entry
    global send_to
    global author
    sock =socket.socket()
    sock.connect(('localhost', 10001))
    t = entry.get()
    t = t.replace(' ','')
    if t!='':
        time = str(datetime.datetime.utcnow()+datetime.timedelta(hours=3))
        sock.send(("send "+author+"\\"+t+"\\"+time[:19]+" "+send_to).encode('utf-8'))
        sock.close
        update(author,send_to)
def update(by,to):
    global window
    global myframe
    global txt
    global send_to
    send_to= to
    if send_to == None:
        pass
    else:
        sock = socket.socket()
        sock.connect(('localhost', 10001))
        sock.send((by + ' make connected update '+to).encode('utf-8'))
        data = list(sock.recv(1000000).decode('utf-8'))
        sock.close()
        strings = []
        while "\n" in data:
            string_index = data.index("\n")
            string_list = data[:string_index]
            data = data[string_index + 1:]
            string_text = ""
            for i in string_list:
                string_text = string_text + i
            strings.append(string_text)
        messages = {}
        n = 0
        for i in strings:
            string_list = list(i)
            name_index = string_list.index('\\')
            name_list = string_list[:name_index]
            name = ""
            for a in name_list:
                name = name + a
            string_list = string_list[name_index + 1:]
            time_list = string_list[:19]
            text_list = string_list[20:]
            time = ""
            for t in time_list:
                time = time + t
            text = ""
            for t in text_list:
                text = text + t
            messages[n] = (name, time, text)
            n += 1
        n=0
        txt.delete(1.0,END)
        for i in messages:
            n+=1
            t= messages[i][2]+'('+messages[i][1]+')-'+messages[i][0]+"\n"
            txt.insert(float(n),t)
def quit():
    global window
    window.destroy()
def mainloop(file):
    global window
    global entry
    global txt
    global author
    global send_to
    send_to = None
    author= file
    sock = socket.socket()
    sock.connect(('localhost', 10001))
    sock.send((file+' connect').encode('utf-8'))
    data = sock.recv(1024).decode('utf-8')
    sock.close()
    window = Tk()
    window.resizable(False,False)
    window.title(file)
    window.geometry("800x800")
    while True:
        quit_btn = Button(window,text="Выйти", command=quit, bg="red")
        send_btn = Button(window, text="Отправить", command=send, bg="green")
        data = data.replace(file,"")
        accounts =data.split()
        frame= Frame(window)
        frame.place(x=200,y=0,width=600,height=600)
        txt = Text(frame,width=580,height=600,wrap=NONE)
        txt.pack(side="left")
        n=0
        for i in accounts:
            funk = partial(update,file,i)
            Button(window,command=funk,text=i).place(x=0,y=n*120,width=200,height=120)
            n+=1
        scroll = Scrollbar(frame,command=txt.yview,orient=VERTICAL,width=20)
        scroll.pack(side=RIGHT, fill=Y)
        txt.config(yscrollcommand=scroll.set)
        entry = Entry(window)
        quit_btn.place(x=200,y=695,width=100,height=50)
        send_btn.place(x=500,y=695,width=100,height=50)
        entry.place(x=200,y=600,width=600,height=40)
        window.mainloop()
        update(file,send_to)
