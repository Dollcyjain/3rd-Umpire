import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
from time import sleep

SET_WIDTH = 650
SET_HEIGHT = 368
flag = True
clip = "clip.mp4"
stream = cv2.VideoCapture(clip)

def pending(decision):
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    sleep(3)

    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    sleep(1.5)

    if decision == 'out':
        frame = cv2.cvtColor(cv2.imread("out.png"), cv2.COLOR_BGR2RGB)

    else:
        frame = cv2.cvtColor(cv2.imread("not_out.png"), cv2.COLOR_BGR2RGB)

    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

def play(speed):
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    global flag
    if flag:
        canvas.create_text(150, 25, fill="yellow", font="Times 27 italic bold", text="Decision Pending...")
    flag = not flag

def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()

def notout():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()

window = tkinter.Tk()
window.title("Third Umpire Decision Review Kit")
cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()

btn = tkinter.Button(window, text=" << Previous (Fast) ", width=75, height=2, command=partial(play, -15))
btn.pack()

btn = tkinter.Button(window, text=" << Previous (Slow) ", width=75, height=2, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text=" Forward (Fast) >> ", width=75, height=2, command=partial(play, 15))
btn.pack()

btn = tkinter.Button(window, text=" Forward (Slow) >> ", width=75, height=2, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text=" Give 'Out' ", width=75, height=2, command=out)
btn.pack()

btn = tkinter.Button(window, text=" Give 'Not Out' ", width=75, height=2, command=notout)
btn.pack()

window.mainloop()
