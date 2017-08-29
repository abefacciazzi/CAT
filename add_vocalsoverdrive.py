from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]


import Tkinter
global instrument_var
global expression_var
global fldRowTxt
global level_var
global grid_var
global bendChkvar
global sameChkvar
global sparseChkvar
global grid_var
global tolerance

def execute():
    global tolerance
    global instrument_var
    global grid_var
    global form
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    tolerance = tolerance.get()
    if tolerance == '':
        tolerance = 4
    C3toolbox.startup()
    C3toolbox.add_vocalsoverdrive(instrument, int(tolerance), 0) #instrument, level, option, selected
    form.destroy()

def launch():
    global instrument_var
    global form
    global grid_var
    global tolerance
    
    form = Tkinter.Tk()
    getFld = Tkinter.IntVar()
    form.wm_title('Create overdrive phrases')
    C3toolbox.startup()
    instrument_name = C3toolbox.get_trackname()
    if instrument_name in C3toolbox.array_dropdownvocals:
        instrument_id = C3toolbox.array_dropdownvocals[instrument_name]
    else:
        instrument_id = 0

    # STEP 1
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)
    
    OPTIONS = ["Vocals", "Harmony 1"]

    instrument_var = Tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[0]) # default value

    instrumentOpt = apply(Tkinter.OptionMenu, (helpLf, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)

    toleranceLbl = Tkinter.Label(helpLf, \
                           text="Create an overdrive phrase for every number of phrases:")
    toleranceLbl.grid(row=0, column=2, padx=5, pady=2, sticky='W')

    tolerance = Tkinter.Entry(helpLf)
    tolerance.insert(0, "4")
    tolerance.config(width=5)
    tolerance.grid(row=0, column=3, padx=5, pady=2, sticky='W')

    allBtn = Tkinter.Button(helpLf, text="Create overdrive phrases", command= lambda: execute()) 
    allBtn.grid(row=0, column=4, rowspan=1, sticky="WE", padx=5, pady=2)
    
    logo = Tkinter.Frame(form, bg="#000")
    logo.grid(row=8, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = Tkinter.PhotoImage(file=path)
    imageLbl = Tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)
    
    form.mainloop()

if __name__ == '__main__':
    launch()
    #C3toolbox.startup()
    #C3toolbox.add_vocalsoverdrive('PART VOCALS', 4, 0) #Do not set SELECTED to 1, it won't work

