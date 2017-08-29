from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import Tkinter

global tolerance
global grid_var_h
global bendChkvar_h
global sameChkvar_h
global sparseChkvar_h
global grid_var_m
global bendChkvar_m
global sameChkvar_m
global sparseChkvar_m
global grid_var_e
global bendChkvar_e
global sameChkvar_e
global sparseChkvar_e
global chordsChkvar_h
global chordsChkvar_m
global chordsChkvar_e
global reduceChordsvar
global reduceNotesvar
global mutevar
global form
global instrument_var
global lvlHardvar
global lvlMediumvar
global lvlEasyvar
global level_var
global snareh_var
global snarem_var
global snaree_var


def execute(selected):
    global form
    global instrument_var
    global lvlHardvar
    global lvlMediumvar
    global lvlEasyvar
    global grid_var_h
    global bendChkvar_h
    global sameChkvar_h
    global sparseChkvar_h
    global grid_var_m
    global bendChkvar_m
    global sameChkvar_m
    global sparseChkvar_m
    global grid_var_e
    global bendChkvar_e
    global sameChkvar_e
    global sparseChkvar_e
    global chordsChkvar_h
    global chordsChkvar_m
    global chordsChkvar_e
    global reduceChordsvar
    global reduceNotesvar
    global mutevar
    global tolerance
    global level_var
    global snareh_var
    global snarem_var
    global snaree_var
    array_grid = { "1" : "w", "1/2" : "h", "1/4" : "q", "1/8" : "e", "1/16" : "s" }
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    lvlHardvar = lvlHardvar.get()
    lvlMediumvar = lvlMediumvar.get()
    lvlEasyvar = lvlEasyvar.get()
    grid_var_h = grid_var_h.get()
    grid_var_h = array_grid[grid_var_h]
    grid_var_m = grid_var_m.get()
    grid_var_m = array_grid[grid_var_m]
    grid_var_e = grid_var_e.get()
    grid_var_e = array_grid[grid_var_e]
    bendChkvar_h = bendChkvar_h.get()
    bendChkvar_m = bendChkvar_m.get()
    bendChkvar_e = bendChkvar_e.get()
    sameChkvar_h = sameChkvar_h.get()
    sameChkvar_m = sameChkvar_m.get()
    sameChkvar_e = sameChkvar_e.get()
    sparseChkvar_h = sparseChkvar_h.get()
    sparseChkvar_m = sparseChkvar_m.get()
    sparseChkvar_e = sparseChkvar_e.get()
    chordsChkvar_e = chordsChkvar_e.get()
    chordsChkvar_m = chordsChkvar_m.get()
    chordsChkvar_h = chordsChkvar_h.get()
    reduceChordsvar = reduceChordsvar.get()
    reduceNotesvar = reduceNotesvar.get()
    snareh_var = snareh_var.get()
    snarem_var = snarem_var.get()
    snaree_var = snaree_var.get()
    what_array = { "Don't simplify snare" : 'n', "Any note" : 'a', "Kick" : 's', "Any tom" : 't', "Any cymbal" : 'c' }
    
    level = str(level_var.get())
    mutevar = mutevar.get()
    tolerance = tolerance.get()
    if tolerance == '':
        tolerance = 20
        
    C3toolbox.startup()
    C3toolbox.reduce_5lane(instrument, [lvlHardvar, lvlMediumvar, lvlEasyvar], \
                           [grid_var_h, sameChkvar_h, sparseChkvar_h, bendChkvar_h], \
                           [grid_var_m, sameChkvar_m, sparseChkvar_m, bendChkvar_m], \
                           [grid_var_e, sameChkvar_e, sparseChkvar_e, bendChkvar_e], \
                           [chordsChkvar_e, chordsChkvar_m, chordsChkvar_h], \
                           reduceChordsvar, reduceNotesvar, \
                           [what_array[snareh_var], what_array[snarem_var], what_array[snaree_var]], \
                           mutevar, int(tolerance), C3toolbox.array_levels[level][0])
    #instrument, level, fix, selected
    form.destroy()

def launch(instrument):
    global tolerance
    global grid_var_h
    global bendChkvar_h
    global sameChkvar_h
    global sparseChkvar_h
    global grid_var_m
    global bendChkvar_m
    global sameChkvar_m
    global sparseChkvar_m
    global grid_var_e
    global bendChkvar_e
    global sameChkvar_e
    global sparseChkvar_e
    global mutevar
    global form
    global instrument_var
    global lvlHardvar
    global lvlMediumvar
    global lvlEasyvar
    global level_var
    global chordsChkvar_h
    global chordsChkvar_m
    global chordsChkvar_e
    global reduceChordsvar
    global reduceNotesvar
    global snareh_var
    global snarem_var
    global snaree_var
    
    C3toolbox.startup()
    form = Tkinter.Tk()
    form.wm_title('Reduce 5 lane')

    C3toolbox.startup()
    if instrument == 'PART DRUMS':
        instrument_name = instrument
    else:
        instrument_name = C3toolbox.get_trackname()
        if instrument_name == 'PART DRUMS' or instrument_name == 'PART DRUMS 2X' and instrument == '5LANE':
            instrument_name = 'PART GUITAR'
        
    if instrument_name in C3toolbox.array_dropdownid:
        instrument_id = C3toolbox.array_dropdownid[instrument_name]
    else:
        instrument_id = 0
        
    # LEVEL HARD
    
    lvlHard = Tkinter.LabelFrame(form, text=" HARD reductions: ")
    lvlHard.grid(row=0, columnspan=8, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    lvlHardvar = Tkinter.IntVar(lvlHard)
    lvlHardChk = Tkinter.Checkbutton(lvlHard, \
               text="", onvalue=1, offvalue=0, variable=lvlHardvar)
    lvlHardChk.grid(row=0, column=1, sticky='W', padx=5, pady=2)
    lvlHardChk.select()

    outTblLbl = Tkinter.Label(lvlHard, \
          text="Grid:")
    outTblLbl.grid(row=0, column=2, sticky='W', padx=5, pady=2)

    OPTIONS = ["1", "1/2", "1/4", "1/8", "1/16"]

    grid_var_h = Tkinter.StringVar(lvlHard)
    grid_var_h.set(OPTIONS[3]) # default value

    gridOpt = apply(Tkinter.OptionMenu, (lvlHard, grid_var_h) + tuple(OPTIONS))
    gridOpt.grid(row=0, column=3, sticky="W", pady=3)

    sameChkvar_h = Tkinter.IntVar(lvlHard)
    sameChk_h = Tkinter.Checkbutton(lvlHard, \
               text="Consecutive notes", onvalue=1, offvalue=0, variable=sameChkvar_h)
    sameChk_h.grid(row=0, column=4, sticky='W', padx=5, pady=2)

    sparseChkvar_h = Tkinter.IntVar(lvlHard)
    sparseChk_h = Tkinter.Checkbutton(lvlHard, \
               text="Sparse notes", onvalue=1, offvalue=0, variable=sparseChkvar_h)
    sparseChk_h.grid(row=0, column=5, sticky='W', padx=5, pady=2)
    sparseChk_h.select()

    bendText = "Fix pitch bend"
    if instrument_id == 0 or instrument_id == 5:
        bendText = "Remove kicks paired with percussion"
        
    bendChkvar_h = Tkinter.IntVar(lvlHard)
    bendChk_h = Tkinter.Checkbutton(lvlHard, \
               text=bendText, onvalue=1, offvalue=0, variable=bendChkvar_h)
    bendChk_h.grid(row=0, column=6, sticky='W', padx=5, pady=2)
    if instrument_id != 0 and instrument_id != 5:
        bendChk_h.select()

    chordsChkvar_h = Tkinter.IntVar(lvlHard)

    if instrument_id != 0 and instrument_id != 5:
        chordsChk_h = Tkinter.Checkbutton(lvlHard, \
               text="If reducing chords, enable use of GB and RO when translating from 3-note chords", onvalue=1, offvalue=0, variable=chordsChkvar_h)
        chordsChk_h.grid(row=1, column=2, columnspan=6, sticky='W', padx=5, pady=2)
        chordsChk_h.select()
    elif instrument_id == 0 or instrument_id == 5:
        snarehLbl = Tkinter.Label(lvlHard, \
                           text="Leave only a snare hit when coupled with:")
        snarehLbl.grid(row=1, column=1, columnspan=3, padx=5, pady=2, sticky='W')

    OPTIONS = ["Don't simplify snare", "Any note", "Kick", "Any tom", "Any cymbal"]

    snareh_var = Tkinter.StringVar(lvlHard)
    snareh_var.set(OPTIONS[0]) # default value

    if instrument_id == 0 or instrument_id == 5:
        snarehOpt = apply(Tkinter.OptionMenu, (lvlHard, snareh_var) + tuple(OPTIONS))
        snarehOpt.grid(row=1, column=4, sticky="WE", pady=3) 
    
    # LEVEL MEDIUM
    
    lvlMedium = Tkinter.LabelFrame(form, text=" MEDIUM reductions: ")
    lvlMedium.grid(row=1, columnspan=8, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    lvlMediumvar = Tkinter.IntVar(lvlMedium)
    lvlMediumChk = Tkinter.Checkbutton(lvlMedium, \
               text="", onvalue=1, offvalue=0, variable=lvlMediumvar)
    lvlMediumChk.grid(row=1, column=1, sticky='W', padx=5, pady=2)
    lvlMediumChk.select()

    outTblLbl = Tkinter.Label(lvlMedium, \
          text="Grid:")
    outTblLbl.grid(row=1, column=2, sticky='W', padx=5, pady=2)

    OPTIONS = ["1", "1/2", "1/4", "1/8", "1/16"]

    grid_var_m = Tkinter.StringVar(lvlMedium)
    
    grid_var_m.set(OPTIONS[2]) # default value

    gridOpt = apply(Tkinter.OptionMenu, (lvlMedium, grid_var_m) + tuple(OPTIONS))
    gridOpt.grid(row=1, column=3, sticky="W", pady=3)

    sameChkvar_m = Tkinter.IntVar(lvlMedium)
    sameChk_m = Tkinter.Checkbutton(lvlMedium, \
               text="Consecutive notes", onvalue=1, offvalue=0, variable=sameChkvar_m)
    sameChk_m.grid(row=1, column=4, sticky='W', padx=5, pady=2)
    if instrument_id != 0 and instrument_id != 5:
        sameChk_m.select()

    sparseChkvar_m = Tkinter.IntVar(lvlMedium)
    sparseChk_m = Tkinter.Checkbutton(lvlMedium, \
               text="Sparse notes", onvalue=1, offvalue=0, variable=sparseChkvar_m)
    sparseChk_m.grid(row=1, column=5, sticky='W', padx=5, pady=2)
    sparseChk_m.select()
    
    bendText = "Fix pitch bend"
    if instrument_id == 0 or instrument_id == 5:
        bendText = "Remove kicks paired with percussion"
        
    bendChkvar_m = Tkinter.IntVar(lvlMedium)
    bendChk_m = Tkinter.Checkbutton(lvlMedium, \
               text=bendText, onvalue=1, offvalue=0, variable=bendChkvar_m)
    bendChk_m.grid(row=1, column=6, sticky='W', padx=5, pady=2)
    if instrument_id == 0 or instrument_id == 5:
        bendChk_m.select()
    
    chordsChkvar_m = Tkinter.IntVar(lvlMedium)
    if instrument_id != 0 and instrument_id != 5:
        chordsChk_m = Tkinter.Checkbutton(lvlMedium, \
               text="If reducing chords, enable use of BO chords", onvalue=1, offvalue=0, variable=chordsChkvar_m)
        chordsChk_m.grid(row=2, column=2, columnspan=6, sticky='W', padx=5, pady=2)
        chordsChk_m.select()
    elif instrument_id == 0 or instrument_id == 5:
        snaremLbl = Tkinter.Label(lvlMedium, \
                           text="Leave only a snare hit when coupled with:")
        snaremLbl.grid(row=3, column=1, columnspan=3, padx=5, pady=2, sticky='W')

    OPTIONS = ["Don't simplify snare", "Any note", "Kick", "Any tom", "Any cymbal"]

    snarem_var = Tkinter.StringVar(lvlMedium)
    snarem_var.set(OPTIONS[0]) # default value

    if instrument_id == 0 or instrument_id == 5:
        snaremOpt = apply(Tkinter.OptionMenu, (lvlMedium, snarem_var) + tuple(OPTIONS))
        snaremOpt.grid(row=3, column=4, sticky="WE", pady=3)
        
    # LEVEL EASY
    
    lvlEasy = Tkinter.LabelFrame(form, text=" EASY reductions: ")
    lvlEasy.grid(row=2, columnspan=8, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    lvlEasyvar = Tkinter.IntVar(lvlEasy)
    lvlEasyChk = Tkinter.Checkbutton(lvlEasy, \
               text="", onvalue=1, offvalue=0, variable=lvlEasyvar)
    lvlEasyChk.grid(row=2, column=1, sticky='W', padx=5, pady=2)
    lvlEasyChk.select()

    outTblLbl = Tkinter.Label(lvlEasy, \
          text="Grid:")
    outTblLbl.grid(row=2, column=2, sticky='W', padx=5, pady=2)

    OPTIONS = ["1", "1/2", "1/4", "1/8", "1/16"]

    grid_var_e = Tkinter.StringVar(lvlEasy)
    grid_var_e.set(OPTIONS[1]) # default value
    if instrument_id == 0:
        grid_var_e.set(OPTIONS[2])
    gridOpt = apply(Tkinter.OptionMenu, (lvlEasy, grid_var_e) + tuple(OPTIONS))
    gridOpt.grid(row=2, column=3, sticky="W", pady=3)

    sameChkvar_e = Tkinter.IntVar(lvlEasy)
    sameChk_e = Tkinter.Checkbutton(lvlEasy, \
               text="Consecutive notes", onvalue=1, offvalue=0, variable=sameChkvar_e)
    sameChk_e.grid(row=2, column=4, sticky='W', padx=5, pady=2)
    if instrument_id != 0 and instrument_id != 5:
        sameChk_e.select()

    sparseChkvar_e = Tkinter.IntVar(lvlEasy)
    sparseChk_e = Tkinter.Checkbutton(lvlEasy, \
               text="Sparse notes", onvalue=1, offvalue=0, variable=sparseChkvar_e)
    sparseChk_e.grid(row=2, column=5, sticky='W', padx=5, pady=2)
    sparseChk_e.select()
    
    bendText = "Fix pitch bend"
    if instrument_id == 0 or instrument_id == 5:
        bendText = "Remove kicks paired with anything"
        
    bendChkvar_e = Tkinter.IntVar(lvlEasy)
    bendChk = Tkinter.Checkbutton(lvlEasy, \
               text=bendText, onvalue=1, offvalue=0, variable=bendChkvar_e)
    bendChk.grid(row=2, column=6, sticky='W', padx=5, pady=2)
    if instrument_id == 0 or instrument_id == 5:
        bendChk.select()

    chordsChkvar_e = Tkinter.IntVar(lvlEasy)
    if instrument_id != 0 and instrument_id != 5:
        chordsChk_e = Tkinter.Checkbutton(lvlEasy, \
                   text="If reducing chords, keep the occasional B and O notes", onvalue=1, offvalue=0, variable=chordsChkvar_e)
        chordsChk_e.grid(row=4, column=2, columnspan=6, sticky='W', padx=5, pady=2)
        chordsChk_e.select()
    elif instrument_id == 0 or instrument_id == 5:
        snareeLbl = Tkinter.Label(lvlEasy, \
                           text="Leave only a snare hit when coupled with:")
        snareeLbl.grid(row=5, column=1, columnspan=3, padx=5, pady=2, sticky='W')

    OPTIONS = ["Don't simplify snare", "Any note", "Kick", "Any tom", "Any cymbal"]

    snaree_var = Tkinter.StringVar(lvlEasy)
    snaree_var.set(OPTIONS[0]) # default value

    if instrument_id == 0 or instrument_id == 5:
        snareeOpt = apply(Tkinter.OptionMenu, (lvlEasy, snaree_var) + tuple(OPTIONS))
        snareeOpt.grid(row=5, column=4, sticky="WE", pady=3)
        
    # OPTIONS

    Options_grid = Tkinter.LabelFrame(form, text=" Options: ")
    Options_grid.grid(row=3, columnspan=8, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    toleranceLbl = Tkinter.Label(Options_grid, \
                           text="Tolerance:")
    toleranceLbl.grid(row=0, column=1, padx=5, pady=2, sticky='W')

    tolerance = Tkinter.Entry(Options_grid)
    tolerance.insert(0, "20")
    tolerance.config(width=5)
    tolerance.grid(row=0, column=2, padx=5, pady=2, sticky='W')

    OPTIONS = ["Drums", "Guitar", "Bass", "Keys", "Pro Keys", "2x Drums", "Rhythm"]
    

    instrument_var = Tkinter.StringVar(Options_grid)
    instrument_var.set(OPTIONS[instrument_id]) # default value

    instrumentOpt = apply(Tkinter.OptionMenu, (Options_grid, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=0, column=3, columnspan=1, sticky="W", pady=3)

    mutevar = Tkinter.IntVar(Options_grid)
    muteChk = Tkinter.Checkbutton(Options_grid, \
               text="Overwrite notes", onvalue=1, offvalue=0, variable=mutevar)
    muteChk.grid(row=0, column=4, sticky='W', padx=5, pady=2)
    
    if instrument_id == 0 or instrument_id == 5:
    
        unflipLbl = Tkinter.Label(Options_grid, \
                           text="Unflip disco starting from:")
        unflipLbl.grid(row=0, column=5, padx=5, pady=2, sticky='W')

    OPTIONS = ["Hard", "Medium", "Easy"]

    level_var = Tkinter.StringVar(Options_grid)
    level_var.set(OPTIONS[0]) # default value

    if instrument_id == 0 or instrument_id == 5:
        levelOpt = apply(Tkinter.OptionMenu, (Options_grid, level_var) + tuple(OPTIONS))
        levelOpt.grid(row=0, column=6, sticky="WE", pady=3) 

    okFileBtn = Tkinter.Button(Options_grid, text="      Reduce      ", command= lambda: execute(0))
    okFileBtn.grid(row=0, column=7, columnspan=4, sticky="WE", padx=5, pady=2)

    reduceChordsvar = Tkinter.IntVar(Options_grid)
    
    if instrument_id != 0 and instrument_id != 5:
        reduceChords = Tkinter.Checkbutton(Options_grid, \
               text="Reduce chords (for all levels processed)", onvalue=1, offvalue=0, variable=reduceChordsvar)
        reduceChords.grid(row=1, column=1, columnspan=3, sticky='W', padx=5, pady=2)
        reduceChords.select()
        
    reduceNotesvar = Tkinter.IntVar(Options_grid)
    
    if instrument_id != 0 and instrument_id != 5:
        
        reduceNotes = Tkinter.Checkbutton(Options_grid, \
               text="Simplify Medium and Easy notes (for all levels processed)", onvalue=1, offvalue=0, variable=reduceNotesvar)
        reduceNotes.grid(row=1, column=4, columnspan=5, sticky='W', padx=5, pady=2)
        reduceNotes.select()

    logo = Tkinter.Frame(form, bg="#000")
    logo.grid(row=4, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = Tkinter.PhotoImage(file=path)
    imageLbl = Tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    form.mainloop()

if __name__ == '__main__':
    #launch('')
    C3toolbox.startup()
    C3toolbox.reduce_5lane('PART GUITAR', [0, 1, 1], ['e', 0, 1, 1], ['q', 1, 1, 0], ['h', 1, 1, 0], [1, 1, 1], 1, 1, ['n', 'n', 'a'], 1, 20, 'h')
