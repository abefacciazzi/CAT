from reaper_python import *
import C3toolbox
import os
import sys
sys.argv=["Main"]
import Tkinter

global instrument_var
global form

def execute(a):
    
    global instrument_var
    global form
    
    C3toolbox.startup()
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    C3toolbox.copy5laneodtopgb(instrument)
    form.destroy()

def launch():

    global instrument_var
    global form
    form = Tkinter.Tk()
    form.wm_title('5-lane to Pro G/B OD/Solo copy')
    
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    inFileLbl = Tkinter.Label(helpLf, text="Select instrument")
    inFileLbl.grid(row=0, column=1, sticky='E', padx=5, pady=2)

    OPTIONS = ["Pro Guitar", "Pro Bass", "Pro Guitar 22", "Pro Bass 22"]

    instrument_var = Tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[0]) # default value

    instrumentOpt = apply(Tkinter.OptionMenu, (helpLf, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3)
    
    allBtn = Tkinter.Button(helpLf, text="Copy OD/Solo markers", command= lambda: execute(0)) 
    allBtn.grid(row=1, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

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
