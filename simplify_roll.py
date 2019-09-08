from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import Tkinter

global level_var
global instrument_var
global form

def execute(selected):
    level = str(level_var.get())
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]

    if instrument == "PART REAL_KEYS":
        instrument = instrument+C3toolbox.array_levels[level][1]
    C3toolbox.startup()
    C3toolbox.simplify_roll(instrument, C3toolbox.array_levels[level][0], selected)
    #instrument, level, selected, mute (when set to 1, does NOT flip sections that appear
    # to be already flipped without prompting user (used in automatic fixing scripts)

    form.destroy()

def launch():
    global form
    global level_var
    global instrument_var

    C3toolbox.startup()
    form = Tkinter.Tk()
    form.wm_title('Simplify rolls/trills/swells')

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
    if curlevel is None:
        form.destroy()
        return
    
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    inFileLbl = Tkinter.Label(helpLf, text="Select instrument")
    inFileLbl.grid(row=1, column=1, sticky='E', padx=5, pady=2)

    OPTIONS = ["Drums", "Guitar", "Bass", "Keys", "Pro Keys", "2x Drums", "Rhythm"]

    instrument_var = Tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[instrument_id]) # default value

    instrumentOpt = apply(Tkinter.OptionMenu, (helpLf, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)

    levelLbl = Tkinter.Label(helpLf, text="Select level")
    levelLbl.grid(row=1, column=2, sticky='E', padx=5, pady=2)

    OPTIONS = ["Expert", "Hard", "Medium", "Easy"]

    level_var = Tkinter.StringVar(helpLf)
    level_var.set(OPTIONS[C3toolbox.array_levels_id[curlevel]]) # default value

    levelOpt = apply(Tkinter.OptionMenu, (helpLf, level_var) + tuple(OPTIONS))
    levelOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3)

    allBtn = Tkinter.Button(helpLf, text="Simplify all", command= lambda: execute(0)) 
    allBtn.grid(row=0, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    selBtn = Tkinter.Button(helpLf, text="Simplify selected", command= lambda: execute(1)) 
    selBtn.grid(row=1, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    logo = Tkinter.Frame(form, bg="#000")
    logo.grid(row=3, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = Tkinter.PhotoImage(file=path)
    imageLbl = Tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    form.mainloop()

if __name__ == '__main__':
    launch()
    #C3toolbox.startup()
    #C3toolbox.simplify_roll('PART DRUMS', 'e', 0)

