import tkinter as tk
from PIL import ImageTk, Image

window = tk.Tk()

#Text
greeting = tk.Label(text='Hello, world')
greeting.pack()

#Image
image1 = Image.open("avatar.png")
test = ImageTk.PhotoImage(image1)

labelImage = tk.Label(image=test)
labelImage.image = test
labelImage.place(x=0, y=0)

window.mainloop()