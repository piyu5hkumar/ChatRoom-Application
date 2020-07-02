from tkinter import *

mainFrame  = Tk()
mainFrame.title('ChatRoom')
mainFrame.geometry("500x500")
mainFrame.resizable(0, 0) 
windowIcon = PhotoImage(file = r'images/chatRoomIcon.png') 
mainFrame.iconphoto(False, windowIcon)

subFrame = Frame(mainFrame)
subFrame.configure(width = 200, height = 500)
subFrame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

userNameLabel = Label(subFrame, text = 'Enter your user name', font=("Calibri 15"))
userNameLabel.grid(row = 0, column = 0, padx = (0, 50), pady = (20, 20))

userNameEntry = Entry(subFrame, bg = '#e6e6e6', font=("Calibri 15"), fg = '#000000')
userNameEntry.grid(row = 0, column = 1)

userNameRequisite = Label(subFrame, text = 'only non capital\nalphanumeric user name allowed')
userNameRequisite.configure( font = ("Calibri 10"), fg = '#94001b')
userNameRequisite.grid(row = 1,column = 1, pady = (0, 20))


checkUserNameButton = Button(subFrame, text = 'Check User Name')
checkUserNameButton.grid(row = 2, column = 0, columnspan = 2, pady = (0, 20))

enterRoomButton = Button(subFrame, text = 'Enter ChatRoom', state = DISABLED)
enterRoomButton.grid(row = 3, column = 0, columnspan = 2, pady = (0, 20))

wrongUserName = Label(subFrame, text = 'error')
wrongUserName.grid(row = 4, column = 0, columnspan = 2)
wrongUserName.grid_remove()
mainFrame.mainloop()