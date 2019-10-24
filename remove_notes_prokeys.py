from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]


import Tkinter
global instrument_var
global fldRowTxt
global level_var
global grid_var
global hChkvar
global mChkvar
global eChkvar

def execute(sel):
    global form
    array_grid = { "1" : "w", "1/2" : "h", "1/4" : "q", "1/8" : "e", "1/16" : "s" }
    #RPR_ShowConsoleMsg(sel)
    tolerance = 20
    hard = hChkvar.get()
    medium = mChkvar.get()
    easy = eChkvar.get()

    #RPR_ShowConsoleMsg(array_grid[grid]+" - "+array_levels[level][0]+" - "+instrument+" - "+tolerance+" - "+same+" - "+sparse+" - "+bend+" - "+str(sel))
    #RPR_ShowConsoleMsg(instrument+" - "+level+" - "+grid+" - "+tolerance+" - "+bend+" - "+same+" - "+sparse)

    C3toolbox.startup()
    C3toolbox.PM("hard: ")
    C3toolbox.PM(str(hard))
    C3toolbox.PM("medium: ")
    C3toolbox.PM(str(medium))
    C3toolbox.PM("easy: ")
    C3toolbox.PM(str(easy))
    if hard:
        C3toolbox.PM("go hard")
        C3toolbox.remove_notes_prokeys('s','h','PART REAL_KEYS_H',20,0)

    if medium:
        C3toolbox.PM("go medium")
        C3toolbox.remove_notes_prokeys('s','m','PART REAL_KEYS_M',20,0)

    if easy:
        C3toolbox.PM("go easy")
        C3toolbox.remove_notes_prokeys('s','e','PART REAL_KEYS_E',20,0)
        
    #(what,level,instrument,how,same,sparse,bend,selected)
    #C3toolbox.remove_notes('q', 'x', '', 10, 0, 0, 0, 0)
    form.destroy()

def launch():
    global instrument_var
    global fldRowTxt
    global hChkvar
    global mChkvar
    global eChkvar
    global form
    
    form = Tkinter.Tk()
    getFld = Tkinter.IntVar()
    form.wm_title('Reduce notes')
    C3toolbox.startup()

    # STEP 1    

    stepThree = Tkinter.LabelFrame(form, text=" Select levels to reduce: ")
    stepThree.grid(row=0, columnspan=5, sticky='WE', \
                   padx=5, pady=5, ipadx=5, ipady=5)
    hChkvar = Tkinter.IntVar(stepThree)
    hChk = Tkinter.Checkbutton(stepThree, \
               text="Hard", onvalue=1, offvalue=0, variable=hChkvar)
    hChk.grid(row=1, column=1, sticky='W', padx=5, pady=2)
    hChk.select()
    
    mChkvar = Tkinter.IntVar(stepThree)
    mChk = Tkinter.Checkbutton(stepThree, \
               text="Medium", onvalue=1, offvalue=0, variable=mChkvar)
    mChk.grid(row=1, column=2, sticky='W', padx=5, pady=2)    
    mChk.select()
    
    eChkvar = Tkinter.IntVar(stepThree)
    eChk = Tkinter.Checkbutton(stepThree, \
               text="Easy", onvalue=1, offvalue=0, variable=eChkvar)
    eChk.grid(row=1, column=3, sticky='W', padx=5, pady=2)
    eChk.select()


    # HELP

    helpLf = Tkinter.LabelFrame(form, text=" Quick Help ")
    helpLf.grid(row=0, column=9, columnspan=1, rowspan=2, \
                sticky='NS', padx=5, pady=5)
    helpLbl = Tkinter.Label(helpLf, text="Check documentation\nfor configuration switches\n\n\n\n\n")
    helpLbl.grid(row=0, columnspan=1, column=9, sticky='W')

    okFileBtn = Tkinter.Button(helpLf, text="Reduce", command= lambda: execute(0))
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
    #C3toolbox.remove_notes_prokeys('e','e','PART REAL_KEYS_E',20,0)
    #(what,level,instrument,how,same,sparse,bend,selected)
    #example: C3toolbox.remove_notes('q', 'x', '', 10, 0, 0, 0, 0)
