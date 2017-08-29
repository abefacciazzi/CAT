from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]


import Tkinter
global instrument_var
global form
global level_var
global measure_var
global beat_var
global ticks_var
global greenvar
global redvar
global yellowvar
global bluvar
global orangevar

def execute(sel):
    global instrument_var
    global form
    global level_var
    global measure_var
    global beat_var
    global ticks_var
    global greenvar
    global redvar
    global yellowvar
    global bluvar
    global orangevar
    C3toolbox.startup()

    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    level = str(level_var.get())
    measure_var = str(measure_var.get())
    measure_var = 100
    
    beat_var = str(beat_var.get())
    if beat_var == "Any":
        beat_var = 100
    else:
        beat_var = int(beat_var)
        
    ticks_var = str(ticks_var.get())
    if ticks_var == "Any":
        ticks_var = 100
    else:
        ticks_var = int(ticks_var)

    ticks_grid = { 100 : 100, 0 : 0, 8 : 40, 12: 60, 16 : 80, 25 : 120, 33 : 160, 37 : 180, 50 : 240, 58 : 280, 62: 300, 66 : 320, 75 : 360, 83 : 400, 87 : 420, 91 : 440 }
    ticks = ticks_grid[ticks_var]
    notes = []
    greenvar = greenvar.get()
    if greenvar == 1:
        notes.append('G')
    redvar = redvar.get()
    if redvar == 1:
        notes.append('R')
    yellowvar = yellowvar.get()
    if yellowvar == 1:
        notes.append('Y')
    bluvar = bluvar.get()
    if bluvar == 1:
        notes.append('B')
    orangevar = orangevar.get()
    if orangevar == 1:
        notes.append('O')
    
    C3toolbox.edit_by_mbt(instrument, C3toolbox.array_levels[level][0], measure_var, beat_var, ticks, notes, sel) #instrument, level, option, selected
    form.destroy()

def launch():
    global instrument_var
    global form
    global level_var
    global measure_var
    global beat_var
    global ticks_var
    global greenvar
    global redvar
    global yellowvar
    global bluvar
    global orangevar
    
    form = Tkinter.Tk()
    getFld = Tkinter.IntVar()
    form.wm_title('Remove notes by MBT')
    C3toolbox.startup()
    instrument_name = C3toolbox.get_trackname()
    if instrument_name in C3toolbox.array_dropdownid:
        instrument_id = C3toolbox.array_dropdownid[instrument_name]
    else:
        instrument_id = 0
    instrument_track = C3toolbox.get_trackid()
    array_instrument_data = C3toolbox.process_instrument(instrument_track)
    array_instrument_notes = array_instrument_data[1]
    array_notesevents = C3toolbox.create_notes_array(array_instrument_notes)
    curlevel = C3toolbox.level(array_notesevents[0], instrument_track)
    
    # STEP 1
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    inFileLbl = Tkinter.Label(helpLf, text="Select instrument")
    inFileLbl.grid(row=0, column=1, sticky='WE', padx=5, pady=2)    
    
    OPTIONS = ["Drums", "Guitar", "Bass", "Keys", "2x Drums", "Rhythm"]

    if instrument_id >= len(OPTIONS):
        instrument_id = 0

    instrument_var = Tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[instrument_id]) # default value

    instrumentOpt = apply(Tkinter.OptionMenu, (helpLf, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=1, column=1, sticky="WE", pady=3)

    levelLbl = Tkinter.Label(helpLf, text="Select difficulty")
    levelLbl.grid(row=0, column=2, columnspan=2, sticky='WE', padx=5, pady=2)

    OPTIONS = ["Expert", "Hard", "Medium", "Easy"]

    level_var = Tkinter.StringVar(helpLf)
    level_var.set(OPTIONS[C3toolbox.array_levels_id[curlevel]]) # default value

    levelOpt = apply(Tkinter.OptionMenu, (helpLf, level_var) + tuple(OPTIONS))
    levelOpt.grid(row=1, column=2, columnspan=2, sticky="WE", pady=3)

    measureLbl = Tkinter.Label(helpLf, text="Measure")
    measureLbl.grid(row=2, column=1, sticky='WE', padx=5, pady=2)

    OPTIONS = ["Any"]

    measure_var = Tkinter.StringVar(helpLf)
    measure_var.set(OPTIONS[0]) # default value

    measureOpt = apply(Tkinter.OptionMenu, (helpLf, measure_var) + tuple(OPTIONS))
    measureOpt.grid(row=3, column=1, sticky="WE", pady=3)

    beatLbl = Tkinter.Label(helpLf, text="Beat")
    beatLbl.grid(row=2, column=2, sticky='WE', padx=5, pady=2)

    max_beat = 0
    for x in range(0, len(C3toolbox.measures_array)):
        beat = C3toolbox.measures_array[x][2]
        if beat > max_beat:
            max_beat = beat
            
    OPTIONS = ["Any"]
    for x in range(1, max_beat+1):
        OPTIONS.append(str(x))
        
    beat_var = Tkinter.StringVar(helpLf)
    beat_var.set(OPTIONS[0]) # default value

    beatOpt = apply(Tkinter.OptionMenu, (helpLf, beat_var) + tuple(OPTIONS))
    beatOpt.grid(row=3, column=2, sticky="WE", pady=3)

    ticksLbl = Tkinter.Label(helpLf, text="Ticks")
    ticksLbl.grid(row=2, column=3, sticky='WE', padx=5, pady=2)

    OPTIONS = ["Any", "0", "12", "25", "50", "75", "8", "16", "33", "37", "58", "62", "66", "83", "87", "91"]

    ticks_var = Tkinter.StringVar(helpLf)
    ticks_var.set(OPTIONS[0]) # default value

    ticksOpt = apply(Tkinter.OptionMenu, (helpLf, ticks_var) + tuple(OPTIONS))
    ticksOpt.grid(row=3, column=3, sticky="WE", pady=3)

    notesLbl = Tkinter.Label(helpLf, text="Select the notes to be removed")
    notesLbl.grid(row=4, column=1, columnspan=3, sticky='WE', padx=5, pady=2)

    greenvar = Tkinter.IntVar(helpLf)
    greenChk = Tkinter.Checkbutton(helpLf, \
               text="Green", onvalue=1, offvalue=0, variable=greenvar)
    greenChk.grid(row=5, column=1, sticky='W', padx=5, pady=2)

    redvar = Tkinter.IntVar(helpLf)
    redChk = Tkinter.Checkbutton(helpLf, \
               text="Red", onvalue=1, offvalue=0, variable=redvar)
    redChk.grid(row=5, column=2, sticky='W', padx=5, pady=2)

    yellowvar = Tkinter.IntVar(helpLf)
    yellowChk = Tkinter.Checkbutton(helpLf, \
               text="Yellow", onvalue=1, offvalue=0, variable=yellowvar)
    yellowChk.grid(row=5, column=3, sticky='W', padx=5, pady=2)

    bluvar = Tkinter.IntVar(helpLf)
    bluChk = Tkinter.Checkbutton(helpLf, \
               text="Blu", onvalue=1, offvalue=0, variable=bluvar)
    bluChk.grid(row=6, column=1, sticky='W', padx=5, pady=2)

    orangevar = Tkinter.IntVar(helpLf)
    orangeChk = Tkinter.Checkbutton(helpLf, \
               text="Orange (Kick for drums", onvalue=1, offvalue=0, variable=orangevar)
    orangeChk.grid(row=6, column=2, columnspan=2, sticky='W', padx=5, pady=2)    
    
    allBtn = Tkinter.Button(helpLf, text="Remove notes", command= lambda: execute(0)) 
    allBtn.grid(row=7, column=1, sticky="WE", padx=5, pady=2)

    selBtn = Tkinter.Button(helpLf, text="Remove from selected measures", command= lambda: execute(1)) 
    selBtn.grid(row=7, column=2, columnspan=2, sticky="WE", padx=5, pady=2)
    
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
    #C3toolbox.edit_by_mbt('PART GUITAR', 'x', 100, 1, 100, ['G'], 0) #Do not set SELECTED to 1, it won't work

