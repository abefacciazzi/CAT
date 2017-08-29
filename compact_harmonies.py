from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]


import Tkinter
global prec_var
global expression_var
global fldRowTxt
global level_var
global grid_var
global bendChkvar
global sameChkvar
global sparseChkvar
global grid_var

def execute():
    global prec_var
    global grid_var
    global form
    prec = str(prec_var.get())
    prec_array = { "H1 > H2 > H3" : { 'main' : 'h1', 'second' : 'h2', 'third' : 'h3' }, \
                   "H1 > H3 > H2" : { 'main' : 'h1', 'second' : 'h3', 'third' : 'h2' }, \
                   "H2 > H1 > H3" : { 'main' : 'h2', 'second' : 'h1', 'third' : 'h3' }, \
                   "H2 > H3 > H1" : { 'main' : 'h2', 'second' : 'h3', 'third' : 'h1' }, \
                   "H3 > H1 > H2" : { 'main' : 'h3', 'second' : 'h1', 'third' : 'h2' }, \
                   "H3 > H2 > H1" : { 'main' : 'h3', 'second' : 'h2', 'third' : 'h1' } }
    prec = prec_array[prec]
    grid = str(grid_var.get())
    grid_array = { '1/32' : 60, '1/64' : 30, '1/128' : 15 }
    grid = grid_array[grid]
    C3toolbox.startup()
    C3toolbox.compact_harmonies(prec, grid) #instrument, level, option, selected
    form.destroy()

def launch():
    global prec_var
    global form
    global grid_var
    
    form = Tkinter.Tk()
    getFld = Tkinter.IntVar()
    form.wm_title('Compact harmonies')
    C3toolbox.startup()
    instrument_name = C3toolbox.get_trackname()
    if instrument_name in C3toolbox.array_dropdownvocals:
        instrument_id = C3toolbox.array_dropdownvocals[instrument_name]
    else:
        instrument_id = 0

    # STEP 1
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)
    
    precLbl = Tkinter.Label(helpLf, text="Select order of processing")
    precLbl.grid(row=0, column=1, sticky='E', padx=5, pady=2)

    OPTIONS = ["H1 > H2 > H3", "H1 > H3 > H2", "H2 > H1 > H3", "H2 > H3 > H1", "H3 > H1 > H2", "H3 > H2 > H1"]

    prec_var = Tkinter.StringVar(helpLf)
    prec_var.set(OPTIONS[0]) # default value

    precOpt = apply(Tkinter.OptionMenu, (helpLf, prec_var) + tuple(OPTIONS))
    precOpt.grid(row=1, column=1, columnspan=1, sticky="WE", pady=3)

    gridLbl = Tkinter.Label(helpLf, text="Select grid")
    gridLbl.grid(row=0, column=2, sticky='E', padx=5, pady=2)

    OPTIONS = ["1/32", "1/64", "1/128"]

    grid_var = Tkinter.StringVar(helpLf)
    grid_var.set(OPTIONS[1]) # default value

    gridOpt = apply(Tkinter.OptionMenu, (helpLf, grid_var) + tuple(OPTIONS))
    gridOpt.grid(row=1, column=2, columnspan=1, sticky="WE", pady=3)

    allBtn = Tkinter.Button(helpLf, text="Compact harmonies", command= lambda: execute()) 
    allBtn.grid(row=0, column=3, rowspan=2, sticky="WENS", padx=5, pady=2)
    
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
    #C3toolbox.compact_harmonies('PART VOCALS', 480) #Do not set SELECTED to 1, it won't work

