from reaper_python import *
import C3toolbox
import os
import sys
sys.argv=["Main"]
import Tkinter

global tuningE
global tuningA
global tuningD
global tuningG
global tuningB
global tuninge
global instrument_var
global form

def execute(a):

    global tuningE
    global tuningA
    global tuningD
    global tuningG
    global tuningB
    global tuninge
    global instrument_var
    global form
    
    C3toolbox.startup()
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    stringE = tuningE.get()
    stringA = tuningA.get()
    stringD = tuningD.get()
    stringG = tuningG.get()
    stringB = tuningB.get()
    stringe = tuninge.get()
    C3toolbox.pg_root_notes(instrument, int(stringE), int(stringA), int(stringD), int(stringG), int(stringB), int(stringe))
    form.destroy()

def launch():

    global tuningE
    global tuningA
    global tuningD
    global tuningG
    global tuningB
    global tuninge
    global instrument_var
    global form
    form = Tkinter.Tk()
    form.wm_title('Root Notes Generator')
    
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    inFileLbl = Tkinter.Label(helpLf, text="Select instrument")
    inFileLbl.grid(row=0, column=1, sticky='E', padx=5, pady=2)

    OPTIONS = ["Pro Guitar", "Pro Bass", "Pro Guitar 22", "Pro Bass 22"]

    instrument_var = Tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[0]) # default value

    instrumentOpt = apply(Tkinter.OptionMenu, (helpLf, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3)

    tuningLbl = Tkinter.Label(helpLf, \
                           text="Tuning:")
    tuningLbl.grid(row=0, column=3, padx=0, pady=2, sticky='W')

    tuningE = Tkinter.Entry(helpLf)
    tuningE.insert(0, "0")
    tuningE.config(width=2)
    tuningE.grid(row=0, column=4, padx=0, pady=0, sticky='W')

    tuningA = Tkinter.Entry(helpLf)
    tuningA.insert(0, "0")
    tuningA.config(width=2)
    tuningA.grid(row=0, column=5, padx=0, pady=0, sticky='W')

    tuningD = Tkinter.Entry(helpLf)
    tuningD.insert(0, "0")
    tuningD.config(width=2)
    tuningD.grid(row=0, column=6, padx=0, pady=0, sticky='W')

    tuningG = Tkinter.Entry(helpLf)
    tuningG.insert(0, "0")
    tuningG.config(width=2)
    tuningG.grid(row=0, column=7, padx=0, pady=0, sticky='W')

    tuningB = Tkinter.Entry(helpLf)
    tuningB.insert(0, "0")
    tuningB.config(width=2)
    tuningB.grid(row=0, column=8, padx=0, pady=0, sticky='W')

    tuninge = Tkinter.Entry(helpLf)
    tuninge.insert(0, "0")
    tuninge.config(width=2)
    tuninge.grid(row=0, column=9, padx=0, pady=0, sticky='W')
    
    allBtn = Tkinter.Button(helpLf, text="Generate Root Notes", command= lambda: execute(0)) 
    allBtn.grid(row=1, column=4, rowspan=1, columnspan=6, sticky="WE", padx=5, pady=2)

    logo = Tkinter.Frame(form, bg="#000")
    logo.grid(row=4, column=0, columnspan=3, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = Tkinter.PhotoImage(file=path)
    imageLbl = Tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    form.mainloop()

if __name__ == '__main__':
    launch()
    

