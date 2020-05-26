from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]

import Tkinter
global h2Chkvar
global h3Chkvar
global h1Chkvar

def execute():
    global form

    h2 = h2Chkvar.get()
    h3 = h3Chkvar.get()
    h1 = h1Chkvar.get()

    if h2 == 1:
        C3toolbox.create_singalong("HARM2")
    if h3 == 1:
        C3toolbox.create_singalong("HARM3")
    if h1 == 1:
        C3toolbox.create_singalong("HARM1")

    form.destroy()

def launch():
    global h2Chkvar
    global h3Chkvar
    global h1Chkvar
    global form

    form = Tkinter.Tk()
    getFld = Tkinter.IntVar()
    form.wm_title('Create sing-a-long notes')
    C3toolbox.startup()

    # Setup options

    userOpts = Tkinter.LabelFrame(form, text=" Select the harmony parts to generate notes for: ")
    userOpts.grid(row=0, columnspan=5, sticky="WE", \
            padx=5, pady=5, ipadx=5, ipady=5)

    h2Chkvar = Tkinter.IntVar(userOpts)
    h2Chk = Tkinter.Checkbutton(userOpts, \
            text="Harmony 2 (guitarist)", onvalue=1, offvalue=0, variable=h2Chkvar)
    h2Chk.grid(row=1, column=1, sticky='W', padx=5, pady=2)
    h2Chk.select()

    h3Chkvar = Tkinter.IntVar(userOpts)
    h3Chk = Tkinter.Checkbutton(userOpts, \
            text="Harmony 3 (bassist)", onvalue=1, offvalue=0, variable=h3Chkvar)
    h3Chk.grid(row=2, column=1, sticky='W', padx=5, pady=2)
    h3Chk.select()

    h1Chkvar = Tkinter.IntVar(userOpts)
    h1Chk = Tkinter.Checkbutton(userOpts, \
            text="Harmony 1 (drummer)", onvalue=1, offvalue=0, variable=h1Chkvar)
    h1Chk.grid(row=3, column=1, sticky='W', padx=5, pady=2)

    # HELP

    helpLf = Tkinter.LabelFrame(form, text=" Quick Help ")
    helpLf.grid(row=0, column=9, columnspan=1, rowspan=2, \
            sticky='NS', padx=5, pady=5)
    helpLbl = Tkinter.Label(helpLf, text="Keys sings the missing\nguitar or bass part.\n\n")
    helpLbl.grid(row=0, columnspan=1, column=9, sticky='W')

    okFileBtn = Tkinter.Button(helpLf, text="Run", command= lambda: execute())
    okFileBtn.grid(row=1, column=9, sticky="WE", padx=5, pady=2)

    logo = Tkinter.Frame(form, bg="#000")
    logo.grid(row=5, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = Tkinter.PhotoImage(file=path)
    imageLbl = Tkinter.Label(logo, image=img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    form.mainloop()

if __name__ == '__main__':
    launch()
    #C3toolbox.startup()
    #C3toolbox.create_singalong("HARM2")

