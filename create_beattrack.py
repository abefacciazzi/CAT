import Tkinter
from Tkinter import *
from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]


global form
global root

def execute(sel):
    global form
    C3toolbox.startup()
    if sel == 1:
        C3toolbox.create_beattrack(0,0)
    elif sel == 2:
        C3toolbox.create_beattrack(1,0)
    else:
        C3toolbox.create_beattrack(1,1)
    form.destroy()
    
    
    
    
def launch():
    C3toolbox.startup()
    C3toolbox.PM("\n>>>1")
    global form
    form = Tkinter.Tk()
    form.wm_title('Manage BEAT track')
    C3toolbox.PM("\n>>>2")
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, columnspan=1, rowspan=1, \
                sticky='NS', padx=5, pady=5)
    
    createBtn = Tkinter.Button(helpLf, text="Create BEAT track notes", command= lambda: execute(1)) 
    createBtn.grid(row=0, column=1, sticky="WE", padx=5, pady=2)

    halveBtn = Tkinter.Button(helpLf, text="Halve BEAT track notes", command= lambda: execute(2)) 
    halveBtn.grid(row=0, column=2, sticky="WE", padx=5, pady=2)

    halveselBtn = Tkinter.Button(helpLf, text="Halve selected BEAT track notes", command= lambda: execute(3)) 
    halveselBtn.grid(row=0, column=3, sticky="WE", padx=5, pady=2)

    logo = Tkinter.Frame(form, bg="#000")
    logo.grid(row=1, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)
    C3toolbox.PM("\n>>>3")
    path = os.path.join( sys.path[0], "banner.gif" )
    img = Tkinter.PhotoImage(file=path)
    imageLbl = Tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)
    C3toolbox.PM("\n>>>4")
    form.mainloop()

if __name__ == '__main__':
    launch()
    #C3toolbox.startup()
    #C3toolbox.create_beattrack(0,0)
    
