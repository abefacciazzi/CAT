from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]

import Tkinter

def execute():
    global form

    instrument_name = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument_name]

    diff_name = str(diff_var.get())
    diff = C3toolbox.array_levels[diff_name][0]

    C3toolbox.startup()
    C3toolbox.PM("inst: {}\n".format(instrument))
    C3toolbox.PM("diff: {}\n".format(diff))

    try:
        C3toolbox.reduce_by_pattern(instrument, diff)
    except Exception as e:
        C3toolbox.exit_exception(e)
    form.destroy()

def launch():
    global instrument_var
    global diff_var
    global form

    form = Tkinter.Tk()
    getFld = Tkinter.IntVar()
    form.wm_title("Reduce by pattern")
    C3toolbox.startup()
    instrument_name = C3toolbox.get_trackname()
    if instrument_name in C3toolbox.array_dropdownid:
        instrument_id = C3toolbox.array_dropdownid[instrument_name]
    else:
        instrument_id = 0

    # Instrument selection to apply to
    # Pro instrument reductions can be applied from 5-lane, so only
    # 5-lane for now.
    instSelect = Tkinter.LabelFrame(form, text="Select instrument")
    instSelect.grid(row=0, columnspan=4, sticky='WE',
            padx=5, pady=5, ipadx=5, ipady=5)

    INST_OPTIONS = ["Drums", "Guitar", "Bass", "Keys"]

    if instrument_id > len(INST_OPTIONS) - 1:
        instrument_id = 0

    instrument_var = Tkinter.StringVar(instSelect)
    instrument_var.set(INST_OPTIONS[instrument_id])

    instOpt = apply(Tkinter.OptionMenu, (instSelect, instrument_var) + tuple(INST_OPTIONS))
    instOpt.grid(row=0, column=1, columnspan=1, padx=5, sticky='WE', pady=3) 

    # Select difficulty to apply the reduction to

    diffSel = Tkinter.LabelFrame(form, text="Select difficulty to apply to")
    diffSel.grid(row=1, columnspan=4, sticky='WE',
            padx=5, pady=5, ipadx=5, ipady=5)

    DIFF_OPTIONS = ["Hard", "Medium", "Easy"]

    diff_var = Tkinter.StringVar(diffSel)
    diff_var.set(DIFF_OPTIONS[0])

    diffOpt = apply(Tkinter.OptionMenu, (diffSel, diff_var) + tuple(DIFF_OPTIONS))
    diffOpt.grid(row=1, column=1, columnspan=1, padx=5, sticky='WE', pady=3)

    # HELP

    helpLf = Tkinter.LabelFrame(form, text=" Quick Help ")
    helpLf.grid(row=0, column=9, columnspan=1, rowspan=2, \
                sticky='NS', padx=5, pady=5)
    helpLbl = Tkinter.Label(helpLf, 
            text="Reduce one or more measures, select those measures on\nexpert, and then run to apply the same reduction on every\nidentical set of measures.\n\n\n",
            justify='left')
    helpLbl.grid(row=0, columnspan=1, column=9, sticky='W')

    okFileBtn = Tkinter.Button(helpLf, text="Reduce by selected pattern", command= lambda: execute())
    okFileBtn.grid(row=1, column=9, sticky="WE", padx=5, pady=2)

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
    #C3toolbox.reduce_by_pattern("PART GUITAR", "h")

