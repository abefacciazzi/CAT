from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import Tkinter

global instrument_var
global expression_var
global fldRowTxt
global form

def execute(selected):
    global instrument_var
    global expression_var
    global fldRowTxt
    global form
    grid_array = { "1/16" : "s", "1/32" : "t", "1/64" : "f" }
    instrument = str(instrument_var.get())
    expression = str(expression_var.get())
    grid = grid_array[expression]
    instrument = C3toolbox.array_instruments[instrument]
    if instrument == "PART REAL_KEYS":
        instrument = "PART REAL_KEYS_X"
    tolerance = str(fldRowTxt.get())

    C3toolbox.startup()
    C3toolbox.polish_notes(instrument, grid, int(tolerance), selected) #instrument, grid, tolerance, selected
    form.destroy()


def launch():
    global instrument_var
    global expression_var
    global fldRowTxt
    global form
    C3toolbox.startup()
    form = Tkinter.Tk()
    form.wm_title('Polish notes')

    instrument_name = C3toolbox.get_trackname()

    if instrument_name in C3toolbox.array_dropdownid:
        instrument_id = C3toolbox.array_dropdownid[instrument_name]
    else:
        instrument_id = 0
    
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    inFileLbl = Tkinter.Label(helpLf, text="Select instrument")
    inFileLbl.grid(row=0, column=1, columnspan=2, sticky='E', padx=5, pady=2)

    OPTIONS = ["Drums", "Guitar", "Bass", "Keys", "Pro Keys", "2x Drums", "Rhythm"]

    if instrument_id >= len(OPTIONS):
        instrument_id = 0
    instrument_var = Tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[instrument_id]) # default value

    instrumentOpt = apply(Tkinter.OptionMenu, (helpLf, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=0, column=3, columnspan=2, sticky="WE", pady=3)

    expressionLbl = Tkinter.Label(helpLf, text="Select grid")
    expressionLbl.grid(row=0, column=5, columnspan=2, sticky='E', padx=5, pady=2)

    OPTIONS = ["1/16", "1/32", "1/64"]

    expression_var = Tkinter.StringVar(helpLf)
    expression_var.set(OPTIONS[1]) # default value

    expressionOpt = apply(Tkinter.OptionMenu, (helpLf, expression_var) + tuple(OPTIONS))
    expressionOpt.grid(row=0, column=7, sticky="WE", pady=3)

    fldLbl = Tkinter.Label(helpLf, \
                           text="Snap to grid notes off by +/- this or less:")
    fldLbl.grid(row=1, column=1, columnspan=6, padx=5, pady=2, sticky='E')
    var = Tkinter.StringVar()
    fldRowTxt = Tkinter.Entry(helpLf, textvariable=var)
    var.set('20')
    fldRowTxt.grid(row=1, column=7, padx=5, pady=2, sticky='W')

    allBtn = Tkinter.Button(helpLf, text="Polish all notes", command= lambda: execute(0)) 
    allBtn.grid(row=0, column=8, sticky="WE", padx=5, pady=2)

    allBtn = Tkinter.Button(helpLf, text="Polish selected notes", command= lambda: execute(1)) 
    allBtn.grid(row=1, column=8, sticky="WE", padx=5, pady=2)

    logo = Tkinter.Frame(form, bg="#000")
    logo.grid(row=2, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = Tkinter.PhotoImage(file=path)
    imageLbl = Tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    form.mainloop()
    
if __name__ == '__main__':
    launch()
    #C3toolbox.startup()
    #C3toolbox.polish_notes("PART VOCALS", "t", 20, 0)
    
