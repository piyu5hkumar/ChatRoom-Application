from tkinter import *
from client_file import Client, HOST, PORT, ADDR, FORMAT

client = Client()
try:
    client.connectToServer(ADDR)
    client.runThreads()
except:
    print("unable to connect to the server")
    exit(0)


def sendMessage(event=None):
    msg = myMessageEntry.get()
    msg = msg.strip()
    if len(msg) > 0:
        sendMessageButton.configure(state=DISABLED)
        client.messageToBeSent(msg)

        msg = client.username + '(YOU) > ' + msg
        allMessagesText.configure(state=NORMAL)
        allMessagesText.insert(INSERT, msg + '\n')
        allMessagesText.configure(state=DISABLED)

        myMessageEntry.delete(0, END)
        sendMessageButton.configure(state=NORMAL)


def enterChatRoomWindow():
    if client.state == 'connected':
        client.username = usernameEntry.get()
        subFrame.place_forget()
        mainFrame.geometry('800x800')
        mainFrame.resizable(0, 0)

        allMessagesText.configure(state=DISABLED)
        allMessagesText.place(relx=0.5, anchor='n')
        myMessageEntry.place(relx=0.5, rely=0.85, anchor='nw')
        myMessageEntry.bind('<Return>', sendMessage)
        sendMessageButton.place(relx=0.9, rely=0.9, anchor='n')


def checkUserName():
    usernameEntered = usernameEntry.get().strip().lower()
    usernameEntry.delete(0, END)
    usernameEntry.insert(0, usernameEntered)

    isError = False

    if len(usernameEntered) < 4:
        usernameError = 'username should be atleast 4 characters long'
        enterChatRoomButton.configure(state=DISABLED)
        usernameEntry.configure(fg='red')
        isError = True

    elif usernameEntered.isalnum() == False:
        usernameError = 'username must contain only alpha numeric characters'
        enterChatRoomButton.configure(state=DISABLED)
        usernameEntry.configure(fg='red')
        isError = True

    else:
        enterChatRoomButton.configure(state=NORMAL)
        usernameEntry.configure(fg='black')
        usernameError = None
        isError = False

    if isError:
        wrongUsername.configure(text=usernameError)
        wrongUsername.place(relx=1.0, rely=1.0, anchor='se')
    else:
        wrongUsername.configure(text='')
        client.setWidgets(allMessagesText, enterChatRoomButton,usernameEntry, wrongUsername, checkUsernameButton)
        username = usernameEntry.get()
        client.messageToBeSent(username)


def resetEnterRoomButton(event):
    enterChatRoomButton.configure(state=DISABLED)
    usernameEntry.configure(fg='black')


mainFrame = Tk()
mainFrame.title('ChatRoom')
mainFrame.geometry("500x500")
mainFrame.resizable(0, 0)
windowIcon = PhotoImage(file=r'images/chatRoomIcon.png')
mainFrame.iconphoto(False, windowIcon)

subFrame = Frame(mainFrame)
subFrame.configure(width=200, height=500)
subFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

userNameLabel = Label(subFrame, text='Enter your user name', font=("Calibri 15"))
userNameLabel.grid(row=0, column=0, padx=(0, 50), pady=(20, 20))

usernameEntry = Entry(subFrame, bg='#e6e6e6', font=("Calibri 15"), fg='#000000')
usernameEntry.grid(row=0, column=1)
usernameEntry.bind('<Button>', resetEnterRoomButton)

usernameRequisite = Label(subFrame, text='only non capital\nalphanumeric username allowed\nmin length is 4')
usernameRequisite.configure(font=("Calibri 10"), fg='#94001b')
usernameRequisite.grid(row=1, column=1, pady=(0, 20))


checkUsernameButton = Button(subFrame, text='Check User Name', command=checkUserName)
checkUsernameButton.grid(row=2, column=0, columnspan=2, pady=(0, 20))

enterChatRoomButton = Button(subFrame, text='Enter ChatRoom', state=DISABLED, command=enterChatRoomWindow)
enterChatRoomButton.grid(row=3, column=0, columnspan=2, pady=(0, 20))

wrongUsername = Label(mainFrame, fg='red')

allMessagesText = Text(mainFrame, relief=SUNKEN, width=60, height=35, bd=10)
myMessageEntry = Entry(mainFrame, width=40, relief=SUNKEN, bd=10, bg='#ffffbf')
sendMessageButton = Button(mainFrame, text='send', command=sendMessage)

mainFrame.mainloop()
