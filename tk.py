import tkinter as tk
from tkinter import messagebox

def display_purpose():
    messagebox.showinfo("Purpose", "This GUI demonstrates the simplicity of tkinter!")

window = tk.Tk()
window.title("Simple GUI")
window.geometry("300x200")  

label = tk.Label(window, text="Hello, Welcome to the Simple GUI!", fg="blue", bg="yellow")
label.pack(pady=20)

name_label = tk.Label(window, text="Names: Suzana and Ghadeer", fg="red")
name_label.pack(pady=10)

button = tk.Button(window, text="Click Me", command=display_purpose)
button.pack(pady=10)

window.mainloop()