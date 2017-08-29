from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import Tkinter

global level_var
global form

def execute(selected):
    global level_var
    global form
    level = str(level_var.get())

    C3toolbox.startup()
    C3toolbox.single_pedal(C3toolbox.array_levels[level][0], 20, selected)
    #instrument, level, fix, selected
    window.close()
    form.destroy()

def launch():
    global level_var
    global form
    
    C3toolbox.startup()
    form = Tkinter.Tk()
    form.wm_title('Reduce double pedal kicks to single pedal kicks')
    
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    OPTIONS = ["Expert", "Hard", "Medium", "Easy"]

    level_var = Tkinter.StringVar(helpLf)
    level_var.set(OPTIONS[0]) # default value

    levelOpt = apply(Tkinter.OptionMenu, (helpLf, level_var) + tuple(OPTIONS))
    levelOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)

    allBtn = Tkinter.Button(helpLf, text="Reduce all", command= lambda: execute(0)) 
    allBtn.grid(row=0, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    selBtn = Tkinter.Button(helpLf, text="Reduce selected", command= lambda: execute(1)) 
    selBtn.grid(row=0, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    logo = Tkinter.Frame(form, bg="#000")
    logo.grid(row=1, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = Tkinter.PhotoImage(file=path)
    imageLbl = Tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    form.mainloop()

if __name__ == '__main__':
    #launch()
    C3toolbox.startup()
    C3toolbox.reduce_chords('PART GUITAR', 'x', 0)
