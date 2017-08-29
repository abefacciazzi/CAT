from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import Tkinter

global form
global tubespacevar
global compactphrasevar
global trimvar
global grid_var
global cleanupvar
global compactharmoniesvar
global prec_var
global removeinvalidvar
global capitalizevar
global fixtexteventsvar
global text_var
global checkcapsvar
global vocalsvar
global harm1var
global harm2var
global harm3var
global precgrid_var

def execute(selected):
    global form
    global tubespacevar
    global compactphrasevar
    global trimvar
    global grid_var
    global cleanupvar
    global compactharmoniesvar
    global prec_var
    global removeinvalidvar
    global capitalizevar
    global fixtexteventsvar
    global text_var
    global checkcapsvar
    global vocalsvar
    global harm1var
    global harm2var
    global harm3var
    global precgrid_var
    
    tubespacevar = int(tubespacevar.get())
    compactphrasevar = int(compactphrasevar.get())
    trimvar = int(trimvar.get())
    grid_var = grid_var.get()
    grid_array = { 'Quarter grid' : 480, 'Eighth grid' : 240 }
    grid_var = grid_array[grid_var]
    cleanupvar = int(cleanupvar.get())
    compactharmoniesvar = int(compactharmoniesvar.get())
    prec_var = prec_var.get()
    prec_array = { "H1 > H2 > H3" : { 'main' : 'h1', 'second' : 'h2', 'third' : 'h3' }, \
                   "H1 > H3 > H2" : { 'main' : 'h1', 'second' : 'h3', 'third' : 'h2' }, \
                   "H2 > H1 > H3" : { 'main' : 'h2', 'second' : 'h1', 'third' : 'h3' }, \
                   "H2 > H3 > H1" : { 'main' : 'h2', 'second' : 'h3', 'third' : 'h1' }, \
                   "H3 > H1 > H2" : { 'main' : 'h3', 'second' : 'h1', 'third' : 'h2' }, \
                   "H3 > H2 > H1" : { 'main' : 'h3', 'second' : 'h2', 'third' : 'h1' } }
    prec_var = prec_array[prec_var]
    precgrid_var = precgrid_var.get()
    grid_array = { '1/32' : 60, '1/64' : 30, '1/128' : 15 }
    precgrid_var = grid_array[precgrid_var]
    removeinvalidvar = int(removeinvalidvar.get())
    capitalizevar = int(capitalizevar.get())
    fixtexteventsvar = int(fixtexteventsvar.get())
    text_var = text_var.get()
    grid_array_text = { 'Fix all issues' : 0, 'Fix only lyrics marked as text' : 1, 'Fix only text events marked as lyrics' : 2 }
    text_var = grid_array_text[text_var]
    checkcapsvar = int(checkcapsvar.get())
    vocalsvar = int(vocalsvar.get())
    harm1var = int(harm1var.get())
    harm2var = int(harm2var.get())
    harm3var = int(harm3var.get())
    
    #Instruments
    instruments_todo = []
    if vocalsvar:
        instruments_todo.append("PART VOCALS")

    if harm1var:
        instruments_todo.append("HARM1")

    if harm2var:
        instruments_todo.append("HARM2")

    if harm3var:
        instruments_todo.append("HARM3")

    C3toolbox.startup()
    #C3toolbox.PM(instruments_todo)
    #C3toolbox.PM(str(polishvar) + " - " + str(grid) + " - " + str(tolerance) + " - " + str(invalidmarkersvar) + " - " + str(sustains_var) + " - " +
    #str(sustainsvar) + " - " + str(odsolovar) + " - " + str(pedalvar) + " - " + str(rollsvar))
    
    C3toolbox.auto_vocalscleanup(instruments_todo, compactphrasevar, trimvar, grid_var, tubespacevar, cleanupvar, compactharmoniesvar, prec_var, precgrid_var, removeinvalidvar, capitalizevar, fixtexteventsvar, text_var, checkcapsvar)
    form.destroy()

def launch():
    global form
    global tubespacevar
    global compactphrasevar
    global trimvar
    global grid_var
    global cleanupvar
    global compactharmoniesvar
    global prec_var
    global removeinvalidvar
    global capitalizevar
    global fixtexteventsvar
    global text_var
    global checkcapsvar
    global vocalsvar
    global harm1var
    global harm2var
    global harm3var
    global precgrid_var
    
    form = Tkinter.Tk()
    form.wm_title('Vocals clean-up')
      
    # PHRASES AND NOTES
    
    general = Tkinter.LabelFrame(form, text=" Phrase markers and notes: ")
    general.grid(row=0, columnspan=3, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    tubespacevar = Tkinter.IntVar(general)
    tubespacevarChk = Tkinter.Checkbutton(general, \
               text="Fix long phrase tubes", onvalue=1, offvalue=0, variable=tubespacevar)
    tubespacevarChk.grid(row=0, column=1, sticky='W', padx=5, pady=2)
    tubespacevarChk.select()

    compactphrasevar = Tkinter.IntVar(general)
    compactphrasevarChk = Tkinter.Checkbutton(general, \
               text="Compact harmonies phrase markers", onvalue=1, offvalue=0, variable=compactphrasevar)
    compactphrasevarChk.grid(row=0, column=2, columnspan=2, sticky='W', padx=5, pady=2)
    compactphrasevarChk.select()
    
    trimvar = Tkinter.IntVar(general)
    trimvarChk = Tkinter.Checkbutton(general, \
               text="Trim phrase markers to a downbeat", onvalue=1, offvalue=0, variable=trimvar)
    trimvarChk.grid(row=1, column=1, sticky='W', padx=5, pady=2)
    trimvarChk.select()
    
    OPTIONS = ["Quarter grid", "Eighth grid"]

    grid_var = Tkinter.StringVar(general)
    grid_var.set(OPTIONS[0]) # default value

    gridOpt = apply(Tkinter.OptionMenu, (general, grid_var) + tuple(OPTIONS))
    gridOpt.grid(row=1, column=2, columnspan=2, sticky="WE", pady=3)

    cleanupvar = Tkinter.IntVar(general)
    cleanupvarChk = Tkinter.Checkbutton(general, \
               text="Clean up empty phrase markers (WARNING: empty H1 markers covering H3 notes WILL be deleted)", onvalue=1, offvalue=0, variable=cleanupvar)
    cleanupvarChk.grid(row=2, column=1, columnspan=3, sticky='W', padx=5, pady=2)
    cleanupvarChk.select()

    compactharmoniesvar = Tkinter.IntVar(general)
    compactharmoniesvarChk = Tkinter.Checkbutton(general, \
               text="Compact harmonies", onvalue=1, offvalue=0, variable=compactharmoniesvar)
    compactharmoniesvarChk.grid(row=3, column=1, sticky='W', padx=5, pady=2)
    compactharmoniesvarChk.select()
    
    OPTIONS = ["H1 > H2 > H3", "H1 > H3 > H2", "H2 > H1 > H3", "H2 > H3 > H1", "H3 > H1 > H2", "H3 > H2 > H1"]

    prec_var = Tkinter.StringVar(general)
    prec_var.set(OPTIONS[0]) # default value

    precOpt = apply(Tkinter.OptionMenu, (general, prec_var) + tuple(OPTIONS))
    precOpt.grid(row=3, column=2, sticky="WE", pady=3)

    OPTIONS = ["1/32", "1/64", "1/128"]

    precgrid_var = Tkinter.StringVar(general)
    precgrid_var.set(OPTIONS[1]) # default value

    precgrid_varOpt = apply(Tkinter.OptionMenu, (general, precgrid_var) + tuple(OPTIONS))
    precgrid_varOpt.grid(row=3, column=3, sticky="WE", pady=3)

    #LYRICS AND EVENTS

    lyrics = Tkinter.LabelFrame(form, text=" Lyrics and Events: ")
    lyrics.grid(row=1, columnspan=3, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    removeinvalidvar = Tkinter.IntVar(lyrics)
    removeinvalidvarChk = Tkinter.Checkbutton(lyrics, \
               text="Remove invalid characters", onvalue=1, offvalue=0, variable=removeinvalidvar)
    removeinvalidvarChk.grid(row=0, column=1, sticky='W', padx=5, pady=2)
    removeinvalidvarChk.select()

    capitalizevar = Tkinter.IntVar(lyrics)
    capitalizevarChk = Tkinter.Checkbutton(lyrics, \
               text="Capitalize first word in phrases", onvalue=1, offvalue=0, variable=capitalizevar)
    capitalizevarChk.grid(row=0, column=2, sticky='W', padx=5, pady=2)
    capitalizevarChk.select()
    
    fixtexteventsvar = Tkinter.IntVar(lyrics)
    fixtexteventsvarChk = Tkinter.Checkbutton(lyrics, \
               text="Fix text events", onvalue=1, offvalue=0, variable=fixtexteventsvar)
    fixtexteventsvarChk.grid(row=1, column=1, sticky='W', padx=5, pady=2)
    fixtexteventsvarChk.select()
    
    OPTIONS = ["Fix all issues", "Fix only lyrics marked as text", "Fix only text events marked as lyrics"]

    text_var = Tkinter.StringVar(lyrics)
    text_var.set(OPTIONS[0]) # default value

    textOpt = apply(Tkinter.OptionMenu, (lyrics, text_var) + tuple(OPTIONS))
    textOpt.grid(row=1, column=2, sticky="WE", pady=3)

    checkcapsvar = Tkinter.IntVar(lyrics)
    checkcapsvarChk = Tkinter.Checkbutton(lyrics, \
               text="Prompt to fix any uncapitalized first word in phrase and capitalized mid-phrase word", onvalue=1, offvalue=0, variable=checkcapsvar)
    checkcapsvarChk.grid(row=2, column=1, columnspan=2, sticky='W', padx=5, pady=2)
    checkcapsvarChk.select()    
    
    #INSTRUMENTS

    instruments = Tkinter.LabelFrame(form, text=" Instruments: ")
    instruments.grid(row=2, columnspan=3, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    C3toolbox.startup()
    vocalsvar = Tkinter.IntVar(instruments)
    if C3toolbox.tracks_array["PART VOCALS"] != 999:
        
        vocalsvarChk = Tkinter.Checkbutton(instruments, \
                   text="Vocals", onvalue=1, offvalue=0, variable=vocalsvar)
        vocalsvarChk.grid(row=0, column=1, sticky='NS', padx=5, pady=2)
        vocalsvarChk.select()
        
    harm1var = Tkinter.IntVar(instruments)    
    if C3toolbox.tracks_array["HARM1"] != 999:
        
        harm1varChk = Tkinter.Checkbutton(instruments, \
                   text="Harm 1", onvalue=1, offvalue=0, variable=harm1var)
        harm1varChk.grid(row=0, column=2, sticky='NS', padx=5, pady=2)
        harm1varChk.select()
        
    harm2var = Tkinter.IntVar(instruments)  
    if C3toolbox.tracks_array["HARM2"] != 999:
        
        harm2varChk = Tkinter.Checkbutton(instruments, \
                   text="Harm 2", onvalue=1, offvalue=0, variable=harm2var)
        harm2varChk.grid(row=0, column=3, sticky='NS', padx=5, pady=2)
        harm2varChk.select()

    harm3var = Tkinter.IntVar(instruments)  
    if C3toolbox.tracks_array["HARM3"] != 999:
        
        harm3varChk = Tkinter.Checkbutton(instruments, \
                   text="Harm 3", onvalue=1, offvalue=0, variable=harm3var)
        harm3varChk.grid(row=0, column=4, sticky='NS', padx=5, pady=2)
        harm3varChk.select()
        
        
    proceed = Tkinter.LabelFrame(form, text=" Execute: ")
    proceed.grid(row=4, columnspan=3, sticky='WE', \
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
