from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import Tkinter

global form
global level_var
global instrument_var
global crashChkvar
global softChkvar
global flamChkvar
global tolerance
global form
global expression_var
global fldRowTxt
global mutevar
global beattrack_var
global keysvar

def execute(selected):
    global beattrack_var
    global level_var
    global instrument_var
    global crashChkvar
    global softChkvar
    global flamChkvar
    global tolerance
    global form
    global expression_var
    global fldRowTxt
    global mutevar
    global keysvar
    
    C3toolbox.startup()
    
    expression = str(expression_var.get())
    pause = str(fldRowTxt.get())
    if pause == 'default':
        pause = 0
    
    level = str(level_var.get())
    grid_array = { '1/16' : 'e', '1/32' : 's' }
    grid = grid_array[level]
    crash = crashChkvar.get()
    soft = softChkvar.get()
    flam = flamChkvar.get()
    keysvar = int(keysvar.get())
    tolerance = tolerance.get()
    if tolerance == '':
        tolerance = 4
    
    mutevar = mutevar.get()
    beattrack = beattrack_var.get()
    if beattrack == 'Normal BEAT track':
        beattrack = 0
    else:
        beattrack = 1
        
    
    #C3toolbox.PM(str(beattrack) + " - " + str(expression) + " - " + str(pause) + " - " + str(grid) + " - " + str(crash) + " - " + str(soft) + " - " + str(flam) + " - " + str(tolerance) + " - " + str(mutevar))
    C3toolbox.startup()
    C3toolbox.auto_animations(beattrack, expression, pause, grid, crash, soft, flam, tolerance, keysvar, mutevar)
    form.destroy()

def launch():
    global beattrack_var
    global level_var
    global instrument_var
    global crashChkvar
    global softChkvar
    global flamChkvar
    global tolerance
    global form
    global expression_var
    global fldRowTxt
    global mutevar
    global keysvar
    
    form = Tkinter.Tk()
    form.wm_title('Auto animations')

    C3toolbox.startup()
      
    # GENERAL
    
    general = Tkinter.LabelFrame(form, text=" General animations: ")
    general.grid(row=0, columnspan=4, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    OPTIONS = ["Normal BEAT track", "Halved BEAT track"]

    beattrack_var = Tkinter.StringVar(general)
    beattrack_var.set(OPTIONS[0]) # default value

    beattrackOpt = apply(Tkinter.OptionMenu, (general, beattrack_var) + tuple(OPTIONS))
    beattrackOpt.grid(row=0, column=1, sticky="W", pady=3)

    OPTIONS = ["play", "mellow", "intense"]

    expression_var = Tkinter.StringVar(general)
    expression_var.set(OPTIONS[0]) # default value

    expressionOpt = apply(Tkinter.OptionMenu, (general, expression_var) + tuple(OPTIONS))
    expressionOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3)

    fldLbl = Tkinter.Label(general, \
                           text="Ticks to trigger idle:")
    fldLbl.grid(row=0, column=3, padx=5, pady=2, sticky='W')
    var = Tkinter.StringVar()
    fldRowTxt = Tkinter.Entry(general, textvariable=var)
    var.set('default')
    fldRowTxt.grid(row=0, column=4, columnspan=1, padx=5, pady=2, sticky='W')

    # KEYS

    keysanim = Tkinter.LabelFrame(form, text=" Pro keys animations: ")
    keysanim.grid(row=3, columnspan=5, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    keysvar = Tkinter.IntVar(keysanim)
    keysvarChk = Tkinter.Checkbutton(keysanim, \
               text="Create pro keys animations from Real Keys X", onvalue=1, offvalue=0, variable=keysvar)
    keysvarChk.grid(row=0, column=1, sticky='W', padx=5, pady=2)
    if C3toolbox.tracks_array['PART REAL_KEYS_X'] != 999:
        keysvarChk.select()
    
    # DRUMS
    
    drumsanim = Tkinter.LabelFrame(form, text=" Drums animations: ")
    drumsanim.grid(row=4, columnspan=5, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    levelLbl = Tkinter.Label(drumsanim, text="Select grid")
    levelLbl.grid(row=0, column=1, sticky='WE', padx=5, pady=2)

    OPTIONS = ["1/16", "1/32"]

    level_var = Tkinter.StringVar(drumsanim)
    level_var.set(OPTIONS[0]) # default value

    levelOpt = apply(Tkinter.OptionMenu, (drumsanim, level_var) + tuple(OPTIONS))
    levelOpt.grid(row=1, column=1, sticky="WE", pady=3)

    crashChkvar = Tkinter.IntVar(drumsanim)
    crashChk = Tkinter.Checkbutton(drumsanim, \
               text="CRASH1 as default crash", onvalue=1, offvalue=0, variable=crashChkvar)
    crashChk.grid(row=0, column=2, sticky='W', padx=5, pady=2)
    
    softChkvar = Tkinter.IntVar(drumsanim)
    softChk = Tkinter.Checkbutton(drumsanim, \
               text="Soft as default for snare/crash", onvalue=1, offvalue=0, variable=softChkvar)
    softChk.grid(row=1, column=2, sticky='W', padx=5, pady=2)    

    toleranceLbl = Tkinter.Label(drumsanim, \
                           text="Min. cymbals hits:")
    toleranceLbl.grid(row=0, column=3, padx=5, pady=2, sticky='W')

    tolerance = Tkinter.Entry(drumsanim)
    tolerance.insert(0, "4")
    tolerance.config(width=5)
    tolerance.grid(row=1, column=3, padx=5, pady=2, sticky='W')

    mutevar = Tkinter.IntVar(drumsanim)
    muteChk = Tkinter.Checkbutton(drumsanim, \
               text="Overwrite notes", onvalue=1, offvalue=0, variable=mutevar)
    muteChk.grid(row=2, column=1, sticky='W', padx=5, pady=2)

    flamChkvar = Tkinter.IntVar(drumsanim)
    flamChk = Tkinter.Checkbutton(drumsanim, \
               text="Make snare+Y toms flams", onvalue=1, offvalue=0, variable=flamChkvar)
    flamChk.grid(row=2, column=2, sticky='W', padx=5, pady=2)
    flamChk.select()

    allBtn = Tkinter.Button(drumsanim, text="Create animations", command= lambda: execute(0)) 
    allBtn.grid(row=2, column=3, sticky="WE", padx=5, pady=2)
    
    logo = Tkinter.Frame(form, bg="#000")
    logo.grid(row=5, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = Tkinter.PhotoImage(file=path)
    imageLbl = Tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    form.mainloop()

if __name__ == '__main__':
    launch()
    #C3toolbox.startup()
    #C3toolbox.reduce_5lane('PART BASS', [1, 1, 1], ['e', 0, 1, 1], ['q', 1, 1, 0], ['h', 1, 1, 0], 0, 10)
