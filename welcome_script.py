from tkinter import *
import socket
import time
from tkinter import messagebox as mb
SingIn = None

def clicked():
    #Отправляет логин и проверяет его наличие у сервера
    global SingIn
    global login
    global labelError
    global window
    try:
        #Обрабатываем ответ сервера
        text= login.get()
        text = text.replace(" ", "")
        if text =='':
            labelError['text'] ="Неправильный логин!"
        else:
            sock = socket.socket()
            sock.connect(('25.95.4.168', 10001))
            sock.send(text.encode('utf-8'))
            data = sock.recv(1024)
            while not data:
                data = sock.recv(1024)
            if data.decode('utf-8') == 'ok\n':
                #Конец исполнения welcome_script и передача исправного логина в mainloop
                SingIn = text
                window.destroy()
            else:
                labelError['text'] ="Неправильный логин!"
    except:
        labelError['text'] ="Нет соединения!"
def welcome_script():
    global SingIn
    global labelError
    global login
    global window
    global ok
    #Создание и настройка окна tk
    window = Tk()
    window.title("Авторизация")
    window.geometry('375x200')
    message = StringVar()
    #Начало цикла ожидания правильного логина
    while SingIn is None:
        labelName = Label(window, text="Введите логин",font=('Arial Bold',40))
        labelError = Label(window,text="",font=('Arial Bold',20))
        labelError.grid(column=0,row=1)
        labelName.grid(column=0,row=0)
        login = Entry(window,width=40,textvariable=message)
        login.grid(column=0,row=2)
        btn = Button(window,text='Зайти',font=('Arial Bold',20),command=clicked)
        btn.grid(column=0,row=3)
        window.mainloop()
    #После получения корректного логина - возвращяем логин
    return SingIn