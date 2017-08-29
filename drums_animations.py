from reaper_python import *
import C3toolbox
import os
import sys
sys.argv=["Main"]
import Tkinter

global level_var
global instrument_var
global crashChkvar
global softChkvar
global flamChkvar
global tolerance
global form

def execute(a):

    global level_var
    global instrument_var
    global crashChkvar
    global softChkvar
    global flamChkvar
    global tolerance
    global form
    
    C3toolbox.startup()
    #C3toolbox.drums_animations('PART DRUMS', 0, 0, 0, 'e', 4, 10)
    level = str(level_var.get())
    grid_array = { '1/16' : 'e', '1/32' : 's' }
    grid = grid_array[level]
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    crash = crashChkvar.get()
    soft = softChkvar.get()
    flam = flamChkvar.get()
    tolerance = tolerance.get()
    C3toolbox.drums_animations(instrument, int(crash), int(soft), int(flam), grid, int(tolerance), 20, 0)
    form.destroy()

def launch():
    
    global level_var
    global instrument_var
    global crashChkvar
    global softChkvar
    global flamChkvar
    global tolerance
    global form
    form = Tkinter.Tk()
    form.wm_title('Automatic drums animations')
    
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    inFileLbl = Tkinter.Label(helpLf, text="Select instrument")
    inFileLbl.grid(row=0, column=1, sticky='E', padx=5, pady=2)

    OPTIONS = ["Drums", "2x Drums"]

    instrument_var = Tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[0]) # default value

    instrumentOpt = apply(Tkinter.OptionMenu, (helpLf, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=1, column=1, columnspan=1, sticky="WE", pady=3)

    levelLbl = Tkinter.Label(helpLf, text="Select grid")
    levelLbl.grid(row=2, column=1, sticky='WE', padx=5, pady=2)

    OPTIONS = ["1/16", "1/32"]

    level_var = Tkinter.StringVar(helpLf)
    level_var.set(OPTIONS[0]) # default value

    levelOpt = apply(Tkinter.OptionMenu, (helpLf, level_var) + tuple(OPTIONS))
    levelOpt.grid(row=3, column=1, columnspan=1, sticky="WE", pady=3) 

    crashChkvar = Tkinter.IntVar(helpLf)
    crashChk = Tkinter.Checkbutton(helpLf, \
               text="CRASH1 as default crash", onvalue=1, offvalue=0, variable=crashChkvar)
    crashChk.grid(row=0, column=2, sticky='W', padx=5, pady=2)

    softChkvar = Tkinter.IntVar(helpLf)
    softChk = Tkinter.Checkbutton(helpLf, \
               text="Soft as default for snare/crash", onvalue=1, offvalue=0, variable=softChkvar)
    softChk.grid(row=1, column=2, sticky='W', padx=5, pady=2)

    toleranceLbl = Tkinter.Label(helpLf, \
                           text="Min. cymbals hits:")
    toleranceLbl.grid(row=2, column=2, padx=5, pady=2, sticky='W')

    tolerance = Tkinter.Entry(helpLf)
    tolerance.insert(0, "4")
    tolerance.config(width=5)
    tolerance.grid(row=3, column=2, padx=5, pady=2, sticky='W')

    flamChkvar = Tkinter.IntVar(helpLf)
    flamChk = Tkinter.Checkbutton(helpLf, \
               text="Make snare+Y toms flams", onvalue=1, offvalue=0, variable=flamChkvar)
    flamChk.grid(row=0, column=3, sticky='W', padx=5, pady=2)
    flamChk.select()
    
    allBtn = Tkinter.Button(helpLf, text="Create animations", command= lambda: execute(0)) 
    allBtn.grid(row=1, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

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
    #C3toolbox.startup()
    #C3toolbox.drums_animations('PART DRUMS', 0, 0, 0, 'e', 4, 10, 0)
    
