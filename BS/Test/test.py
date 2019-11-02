from Tkinter import *

def counter(btn):

    global count

    a = count

    i=int(a)

    i+=1

    a=str(i)

    count = a

    btn.config(text = a)


window = Tk()

frame = Frame(window)

frame.pack()

#global count

count = StringVar()

count = '0'

botton = Button(frame,text = count ,command = lambda:counter(botton))
print(count)

botton.pack()

window.mainloop()