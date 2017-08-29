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

def execute():
    global instrument_var
    global grid_var
    global form
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    grid = str(grid_var.get())
    grid_array = { 'Quarter grid' : 480, 'Eighth grid' : 240 }
    grid = grid_array[grid]
    C3toolbox.startup()
    C3toolbox.trim_phrase_markers(instrument, grid) #instrument, level, option, selected
    form.destroy()

def launch():
    global instrument_var
    global form
    global grid_var
    
    form = Tkinter.Tk()
    getFld = Tkinter.IntVar()
    form.wm_title('Trim phrase markers')
    C3toolbox.startup()
    instrument_name = C3toolbox.get_trackname()
    if instrument_name in C3toolbox.array_dropdownvocals:
        instrument_id = C3toolbox.array_dropdownvocals[instrument_name]
    else:
        instrument_id = 0

    # STEP 1
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)
    
    OPTIONS = ["Vocals", "Harmony 1", "Harmony 2"]

    instrument_var = Tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[instrument_id]) # default value

    instrumentOpt = apply(Tkinter.OptionMenu, (helpLf, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)

    OPTIONS = ["Quarter grid", "Eighth grid"]

    grid_var = Tkinter.StringVar(helpLf)
    grid_var.set(OPTIONS[0]) # default value

    gridOpt = apply(Tkinter.OptionMenu, (helpLf, grid_var) + tuple(OPTIONS))
    gridOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3)

    allBtn = Tkinter.Button(helpLf, text="Trim phrase markers", command= lambda: execute()) 
    allBtn.grid(row=0, column=3, rowspan=1, sticky="WE", padx=5, pady=2)
    
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
    #C3toolbox.trim_phrase_markers('PART VOCALS', 480) #Do not set SELECTED to 1, it won't work

