from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import Tkinter

global form
global level_var
global instrument_var
global tolerance
global form
global expression_var
global fldRowTxt
global mutevar
global beattrack_var
global polishvar
global invalidmarkersvar
global sustainsvar
global sustains_var
global odsolovar
global pedalvar
global rollsvar
global guitarvar
global bassvar
global drumsvar
global vocalsvar
global keysvar
global prokeysvar
global drums2xvar
global rhythmvar

def execute(selected):
    global beattrack_var
    global level_var
    global instrument_var
    global tolerance
    global form
    global expression_var
    global fldRowTxt
    global mutevar
    global polishvar
    global invalidmarkersvar
    global sustainsvar
    global sustains_var
    global odsolovar
    global pedalvar
    global rollsvar
    global guitarvar
    global bassvar
    global drumsvar
    global vocalsvar
    global keysvar
    global prokeysvar
    global drums2xvar
    global rhythmvar
    


    #Polish
    polishvar = polishvar.get()
    
    grid_array = { "1/16" : "s", "1/32" : "t", "1/64" : "f" }
    expression = str(expression_var.get())
    grid = grid_array[expression]
    tolerance = str(fldRowTxt.get())

    #Invalid markers
    invalidmarkersvar = invalidmarkersvar.get()
    
    #Fix sustains
    sustainsvar = sustainsvar.get()
    
    sustains_var = sustains_var.get()
    if sustains_var == "Fix only stubby sustains":
        sustains_var = 0
    else:
        sustains_var = 1
    
    #OD and solo
    odsolovar = odsolovar.get()
    
    #5 Lane
    pedalvar = pedalvar.get()
    rollsvar = rollsvar.get()
    
    #Instruments
    instruments_todo = []
    guitarvar = guitarvar.get()
    if guitarvar:
        instruments_todo.append("PART GUITAR")
    bassvar = bassvar.get()
    if bassvar:
        instruments_todo.append("PART BASS")
    drumsvar = drumsvar.get()
    if drumsvar:
        instruments_todo.append("PART DRUMS")
    vocalsvar = vocalsvar.get()
    if vocalsvar:
        instruments_todo.append("PART VOCALS")
    keysvar = keysvar.get()
    if keysvar:
        instruments_todo.append("PART KEYS")
    prokeysvar = prokeysvar.get()
    if prokeysvar:
        instruments_todo.append("PART REAL_KEYS")
    drums2xvar = drums2xvar.get()
    if drums2xvar:
        instruments_todo.append("PART DRUMS 2X")
    rhythmvar = rhythmvar.get()
    if rhythmvar:
        instruments_todo.append("PART RHYTHM")
    C3toolbox.startup()
    #C3toolbox.PM(instruments_todo)
    #C3toolbox.PM(str(polishvar) + " - " + str(grid) + " - " + str(tolerance) + " - " + str(invalidmarkersvar) + " - " + str(sustains_var) + " - " +
    #str(sustainsvar) + " - " + str(odsolovar) + " - " + str(pedalvar) + " - " + str(rollsvar))
    
    C3toolbox.auto_generalcleanup(instruments_todo, int(polishvar), grid, tolerance, int(invalidmarkersvar), int(sustainsvar), int(sustains_var), int(odsolovar), int(pedalvar), int(rollsvar))
    form.destroy()

def launch():
    global beattrack_var
    global level_var
    global instrument_var
    global tolerance
    global form
    global expression_var
    global fldRowTxt
    global mutevar
    global polishvar
    global invalidmarkersvar
    global sustainsvar
    global sustains_var
    global odsolovar
    global pedalvar
    global rollsvar
    global guitarvar
    global bassvar
    global drumsvar
    global vocalsvar
    global keysvar
    global prokeysvar
    global drums2xvar
    global rhythmvar
    
    form = Tkinter.Tk()
    form.wm_title('Auto clean-up')
      
    # POLISH
    
    general = Tkinter.LabelFrame(form, text=" Polish notes (excluding vocals): ")
    general.grid(row=0, columnspan=3, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    polishvar = Tkinter.IntVar(general)
    polishvarChk = Tkinter.Checkbutton(general, \
               text="", onvalue=1, offvalue=0, variable=polishvar)
    polishvarChk.grid(row=0, column=1, sticky='W', padx=5, pady=2)
    polishvarChk.select()

    expressionLbl = Tkinter.Label(general, text="Select grid")
    expressionLbl.grid(row=0, column=2, sticky='E', padx=5, pady=2)

    OPTIONS = ["1/16", "1/32", "1/64"]

    expression_var = Tkinter.StringVar(general)
    expression_var.set(OPTIONS[1]) # default value

    expressionOpt = apply(Tkinter.OptionMenu, (general, expression_var) + tuple(OPTIONS))
    expressionOpt.grid(row=0, column=3, sticky="WE", pady=3)

    fldLbl = Tkinter.Label(general, \
                           text="Precision:")
    fldLbl.grid(row=1, column=2, padx=5, pady=2, sticky='E')
    var = Tkinter.StringVar()
    
    fldRowTxt = Tkinter.Entry(general, textvariable=var)
    var.set('20')
    fldRowTxt.grid(row=1, column=3, padx=5, pady=2, sticky='W')

    # FIX NOTES
    
    fixmarkers = Tkinter.LabelFrame(form, text=" Remove invalid markers: ")
    fixmarkers.grid(row=0, column=4, columnspan=1, sticky='NSWE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    invalidmarkersvar = Tkinter.IntVar(fixmarkers)
    invalidmarkersvarChk = Tkinter.Checkbutton(fixmarkers, \
               text="Fix all invalid markers", onvalue=1, offvalue=0, variable=invalidmarkersvar)
    invalidmarkersvarChk.grid(row=0, column=1, sticky='NS', padx=5, pady=2)
    invalidmarkersvarChk.select()
    
    # FIX SUSTAINS


    fixsustains = Tkinter.LabelFrame(form, text=" Fix sustains: ")
    fixsustains.grid(row=1, column=1, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    sustainsvar = Tkinter.IntVar(fixsustains)
    sustainsvarChk = Tkinter.Checkbutton(fixsustains, \
               text="", onvalue=1, offvalue=0, variable=sustainsvar)
    sustainsvarChk.grid(row=0, column=1, sticky='W', padx=5, pady=2)
    sustainsvarChk.select()    

    OPTIONS = ["Fix only stubby sustains", "Fix stubby and too long sustains"]

    sustains_var = Tkinter.StringVar(fixsustains)
    sustains_var.set(OPTIONS[1]) # default value

    sustainsOpt = apply(Tkinter.OptionMenu, (fixsustains, sustains_var) + tuple(OPTIONS))
    sustainsOpt.grid(row=0, column=2, sticky="WE", pady=3)    
    
    # OD SOLO
    
    odsolo = Tkinter.LabelFrame(form, text=" Copy OD and solo markers: ")
    odsolo.grid(row=1, column=4, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    odsolovar = Tkinter.IntVar(odsolo)
    odsolovarChk = Tkinter.Checkbutton(odsolo, \
               text="Copy missing OD and solo\nmarkers to pro keys", onvalue=1, offvalue=0, variable=odsolovar)
    odsolovarChk.grid(row=0, column=1, sticky='NS', padx=5, pady=2)
    odsolovarChk.select()

    # DRUMS

    drums = Tkinter.LabelFrame(form, text=" 5-lane fixes: ")
    drums.grid(row=2, column=1, columnspan=4, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    rollsvar = Tkinter.IntVar(drums)
    rollsvarChk = Tkinter.Checkbutton(drums, \
               text="Simplify rolls/swells/trills/tremolos", onvalue=1, offvalue=0, variable=rollsvar)
    rollsvarChk.grid(row=0, column=1, sticky='NS', padx=5, pady=2)
    rollsvarChk.select()
    
    pedalvar = Tkinter.IntVar(drums)
    pedalvarChk = Tkinter.Checkbutton(drums, \
               text="Reduce double drum kicks to single pedal", onvalue=1, offvalue=0, variable=pedalvar)
    pedalvarChk.grid(row=0, column=2, sticky='NS', padx=5, pady=2)
    pedalvarChk.select()

    #INSTRUMENTS

    instruments = Tkinter.LabelFrame(form, text=" Instruments: ")
    instruments.grid(row=3, column=1, columnspan=8, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    C3toolbox.startup()
    guitarvar = Tkinter.IntVar(instruments)
    if C3toolbox.tracks_array["PART GUITAR"] != 999:
        
        guitarvarChk = Tkinter.Checkbutton(instruments, \
                   text="Guitar", onvalue=1, offvalue=0, variable=guitarvar)
        guitarvarChk.grid(row=0, column=1, sticky='NS', padx=5, pady=2)
        guitarvarChk.select()
    bassvar = Tkinter.IntVar(instruments)
    if C3toolbox.tracks_array["PART BASS"] != 999:
        
        bassvarChk = Tkinter.Checkbutton(instruments, \
                   text="Bass", onvalue=1, offvalue=0, variable=bassvar)
        bassvarChk.grid(row=0, column=2, sticky='NS', padx=5, pady=2)
        bassvarChk.select()
    drumsvar = Tkinter.IntVar(instruments)
    if C3toolbox.tracks_array["PART DRUMS"] != 999:
        
        drumsvarChk = Tkinter.Checkbutton(instruments, \
                   text="Drums", onvalue=1, offvalue=0, variable=drumsvar)
        drumsvarChk.grid(row=0, column=3, sticky='NS', padx=5, pady=2)
        drumsvarChk.select()
    vocalsvar = Tkinter.IntVar(instruments)
    if C3toolbox.tracks_array["PART VOCALS"] != 999:
        
        vocalsvarChk = Tkinter.Checkbutton(instruments, \
                   text="Vocals", onvalue=1, offvalue=0, variable=vocalsvar)
        vocalsvarChk.grid(row=0, column=4, sticky='NS', padx=5, pady=2)
        vocalsvarChk.select()
    keysvar = Tkinter.IntVar(instruments)    
    if C3toolbox.tracks_array["PART KEYS"] != 999:
        
        keysvarChk = Tkinter.Checkbutton(instruments, \
                   text="Keys", onvalue=1, offvalue=0, variable=keysvar)
        keysvarChk.grid(row=0, column=5, sticky='NS', padx=5, pady=2)
        keysvarChk.select()
    prokeysvar = Tkinter.IntVar(instruments)
    if C3toolbox.tracks_array["PART REAL_KEYS_X"] != 999:
        
        prokeysvarChk = Tkinter.Checkbutton(instruments, \
                   text="Pro Keys", onvalue=1, offvalue=0, variable=prokeysvar)
        prokeysvarChk.grid(row=0, column=6, sticky='NS', padx=5, pady=2)
        prokeysvarChk.select()
    drums2xvar = Tkinter.IntVar(instruments)
    if C3toolbox.tracks_array["PART DRUMS 2X"] != 999:
        
        drums2xvarChk = Tkinter.Checkbutton(instruments, \
                   text="Drums 2X", onvalue=1, offvalue=0, variable=drums2xvar)
        drums2xvarChk.grid(row=0, column=7, sticky='NS', padx=5, pady=2)
        drums2xvarChk.select()
    rhythmvar = Tkinter.IntVar(instruments)
    if C3toolbox.tracks_array["PART RHYTHM"] != 999:
        
        rhythmvarChk = Tkinter.Checkbutton(instruments, \
                   text="Rhythm", onvalue=1, offvalue=0, variable=rhythmvar)
        rhythmvarChk.grid(row=0, column=8, sticky='NS', padx=5, pady=2)
        rhythmvarChk.select()
        
    proceed = Tkinter.LabelFrame(form, text=" Execute (all difficulty levels of selected instruments will be processed): ")
    proceed.grid(row=4, column=1, columnspan=8, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)
    
    allBtn = Tkinter.Button(proceed, text="Clean up all issues", command= lambda: execute(0)) 
    allBtn.grid(row=0, column=5, sticky="W", padx=5, pady=2)
        
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
    #C3toolbox.auto_generalcleanup('PART BASS', [1, 1, 1], ['e', 0, 1, 1], ['q', 1, 1, 0], ['h', 1, 1, 0], 0, 10)
