from reaper_python import *
import C3toolbox
import create_beattrack
import create_animation_markers
import filter_notes
import remove_notes
import create_triplets
import fix_sustains
import simplify_roll
import remove_kick
import flip_discobeat
import unflip_discobeat
import single_pedal
import drums_animations
import reduce_5lane
import auto_animations
import polish_notes
import reduce_chords
import reduce_singlenotes
import add_slides
import tubes_space
import remove_invalid_chars
import capitalize_first
import check_capitalization
import unpitch
import pitch
import hide_lyrics
import create_phrase_markers
import trim_phrase_markers
import compact_harmonies
import add_vocalsoverdrive
import fix_textevents
import cleanup_phrases
import compound_phrases
import copy_od_solo
import single_snare
import auto_cleanup
import vocals_cleanup
import create_keys_animations
import edit_by_mbt
import cleanup_notes
import export_lyrics
import remove_notes_prokeys
import pgrootnotes
import fhp
import pg_copy_od_solo

import os
import sys
sys.argv=["Main"]
import Tkinter

global root

def execute_this(function):
    global root
    if function == 'reduce_drums':
        root.destroy()
        reduce_5lane.launch('PART DRUMS')
    elif function == 'reduce_5lane':
        root.destroy()
        reduce_5lane.launch('5LANE')
    else:
        subwindow = eval(function)
        root.destroy()
        subwindow.launch()
    
def RunCARV():
    global root
    root.destroy()
    import RBNCheck

if __name__ == '__main__':
    root = Tkinter.Tk()
    root.wm_title('C3 Reaper Automation Project')
    
    secVarious = Tkinter.LabelFrame(root, text=" Animation and System: ")
    secVarious.grid(row=0, columnspan=5, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    beattrackBtn = Tkinter.Button(secVarious, text="Create BEAT track", command= lambda: execute_this('create_beattrack')) 
    beattrackBtn.grid(row=0, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    animationsBtn = Tkinter.Button(secVarious, text="Create animations events", command= lambda: execute_this('create_animation_markers')) 
    animationsBtn.grid(row=0, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    drumsanimationsBtn = Tkinter.Button(secVarious, text="Create drums animations", command= lambda: execute_this('drums_animations')) 
    drumsanimationsBtn.grid(row=0, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    prokeysanimationsBtn = Tkinter.Button(secVarious, text="Create pro keys animations", command= lambda: execute_this('create_keys_animations')) 
    prokeysanimationsBtn.grid(row=0, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    invalidmarkersBtn = Tkinter.Button(secVarious, text="Remove invalid markers", command= lambda: execute_this('filter_notes')) 
    invalidmarkersBtn.grid(row=0, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    sec5lane = Tkinter.LabelFrame(root, text=" 5-lane: ")
    sec5lane.grid(row=1, columnspan=5, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    removenotesBtn = Tkinter.Button(sec5lane, text="Remove notes", command= lambda: execute_this('remove_notes')) 
    removenotesBtn.grid(row=1, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    tripleBtn = Tkinter.Button(sec5lane, text="Reduce to triple hits", command= lambda: execute_this('create_triplets')) 
    tripleBtn.grid(row=1, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    sustainsBtn = Tkinter.Button(sec5lane, text="Fix sustains", command= lambda: execute_this('fix_sustains')) 
    sustainsBtn.grid(row=1, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    rollsBtn = Tkinter.Button(sec5lane, text="Fix trills/rolls", command= lambda: execute_this('simplify_roll')) 
    rollsBtn.grid(row=1, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    editbymbtBtn = Tkinter.Button(sec5lane, text="Edit by MBT", command= lambda: execute_this('edit_by_mbt')) 
    editbymbtBtn.grid(row=1, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    polishBtn = Tkinter.Button(sec5lane, text="Polish notes", command= lambda: execute_this('polish_notes')) 
    polishBtn.grid(row=2, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    chordsBtn = Tkinter.Button(sec5lane, text="Reduce chords", command= lambda: execute_this('reduce_chords')) 
    chordsBtn.grid(row=2, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    singlenotesBtn = Tkinter.Button(sec5lane, text="Lower frets complexity", command= lambda: execute_this('reduce_singlenotes')) 
    singlenotesBtn.grid(row=2, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    prosoloodBtn = Tkinter.Button(sec5lane, text="Add missing solo/OD to pro", command= lambda: execute_this('copy_od_solo')) 
    prosoloodBtn.grid(row=2, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    cleanupnotesBtn = Tkinter.Button(sec5lane, text="Clean up notes' length", command= lambda: execute_this('cleanup_notes')) 
    cleanupnotesBtn.grid(row=2, column=5, rowspan=1, sticky="WE", padx=5, pady=2)
    
    prokeysreduceBtn = Tkinter.Button(sec5lane, text="Reduce pro keys note density based on 5-lane", command= lambda: execute_this('remove_notes_prokeys')) 
    prokeysreduceBtn.grid(row=3, column=1, columnspan=3, sticky="WE", padx=5, pady=2)
    

    secDrums = Tkinter.LabelFrame(root, text=" Drums: ")
    secDrums.grid(row=2, columnspan=5, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    removekicksBtn = Tkinter.Button(secDrums, text="Remove kicks", command= lambda: execute_this('remove_kick')) 
    removekicksBtn.grid(row=2, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    singlesnareBtn = Tkinter.Button(secDrums, text="Leave single snare hits", command= lambda: execute_this('single_snare')) 
    singlesnareBtn.grid(row=2, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    flipBtn = Tkinter.Button(secDrums, text="Flip disco beats", command= lambda: execute_this('flip_discobeat')) 
    flipBtn.grid(row=2, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    unflipBtn = Tkinter.Button(secDrums, text="Unflip disco beats", command= lambda: execute_this('unflip_discobeat')) 
    unflipBtn.grid(row=2, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    doublepedalBtn = Tkinter.Button(secDrums, text="Reduce 2x bass pedal", command= lambda: execute_this('single_pedal')) 
    doublepedalBtn.grid(row=2, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    secVocals = Tkinter.LabelFrame(root, text=" Vocals: ")
    secVocals.grid(row=3, columnspan=5, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    addslidesBtn = Tkinter.Button(secVocals, text="Add slides", command= lambda: execute_this('add_slides')) 
    addslidesBtn.grid(row=1, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    spacetubesBtn = Tkinter.Button(secVocals, text="Add space between tubes", command= lambda: execute_this('tubes_space')) 
    spacetubesBtn.grid(row=1, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    punctuationBtn = Tkinter.Button(secVocals, text="Remove illegal punctuation", command= lambda: execute_this('remove_invalid_chars')) 
    punctuationBtn.grid(row=1, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    capitalizeBtn = Tkinter.Button(secVocals, text="Capitalize first lyric in phrases", command= lambda: execute_this('capitalize_first')) 
    capitalizeBtn.grid(row=1, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    checkcapsBtn = Tkinter.Button(secVocals, text="Check/fix capitalization", command= lambda: execute_this('check_capitalization')) 
    checkcapsBtn.grid(row=1, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    unpitchBtn = Tkinter.Button(secVocals, text="Change notes to non-pitched", command= lambda: execute_this('unpitch')) 
    unpitchBtn.grid(row=2, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    hidelyricsBtn = Tkinter.Button(secVocals, text="Hide lyrics", command= lambda: execute_this('hide_lyrics')) 
    hidelyricsBtn.grid(row=2, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    createphraseBtn = Tkinter.Button(secVocals, text="Create phrase markers", command= lambda: execute_this('create_phrase_markers')) 
    createphraseBtn.grid(row=2, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    trimphraseBtn = Tkinter.Button(secVocals, text="Trim phrase markers", command= lambda: execute_this('trim_phrase_markers')) 
    trimphraseBtn.grid(row=2, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    harmoniesBtn = Tkinter.Button(secVocals, text="Compact harmonies", command= lambda: execute_this('compact_harmonies')) 
    harmoniesBtn.grid(row=2, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    overdriveBtn = Tkinter.Button(secVocals, text="Add overdrive phrases", command= lambda: execute_this('add_vocalsoverdrive')) 
    overdriveBtn.grid(row=3, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    fixtexteventsBtn = Tkinter.Button(secVocals, text="Fix text events", command= lambda: execute_this('fix_textevents')) 
    fixtexteventsBtn.grid(row=3, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    cleanupphrasesBtn = Tkinter.Button(secVocals, text="Delete empty phrases", command= lambda: execute_this('cleanup_phrases')) 
    cleanupphrasesBtn.grid(row=3, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    compactphrasesBtn = Tkinter.Button(secVocals, text="Compact phrases", command= lambda: execute_this('compound_phrases')) 
    compactphrasesBtn.grid(row=3, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    unpitchBtn = Tkinter.Button(secVocals, text="Change notes to pitched", command= lambda: execute_this('pitch')) 
    unpitchBtn.grid(row=3, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    exportlyricsBtn = Tkinter.Button(secVocals, text="Export lyrics", command= lambda: execute_this('export_lyrics')) 
    exportlyricsBtn.grid(row=4, column=1, rowspan=1, sticky="WE", padx=5, pady=2)
    
    secSupersets = Tkinter.LabelFrame(root, text=" Supersets: ")
    secSupersets.grid(row=4, columnspan=5, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    reductionsBtn = Tkinter.Button(secSupersets, text="Automatic reductions (5-lane)", command= lambda: execute_this('reduce_5lane')) 
    reductionsBtn.grid(row=4, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    reductionsBtn = Tkinter.Button(secSupersets, text="Automatic reductions (drums)", command= lambda: execute_this('reduce_drums')) 
    reductionsBtn.grid(row=4, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    animationsBtn = Tkinter.Button(secSupersets, text="Automatic animations", command= lambda: execute_this('auto_animations')) 
    animationsBtn.grid(row=4, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    vocalsBtn = Tkinter.Button(secSupersets, text="Vocals clean up", command= lambda: execute_this('vocals_cleanup')) 
    vocalsBtn.grid(row=4, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    generalBtn = Tkinter.Button(secSupersets, text="General clean up", command= lambda: execute_this('auto_cleanup')) 
    generalBtn.grid(row=4, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    secPGB = Tkinter.LabelFrame(root, text=" Pro Guitar/Bass: ")
    secPGB.grid(row=5, columnspan=5, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    GenerateRootNotesBtn = Tkinter.Button(secPGB, text="Generate Root Notes", command= lambda: execute_this('pgrootnotes'))
    GenerateRootNotesBtn.grid(row=1, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    GenerateFretHandPositionsBtn = Tkinter.Button(secPGB, text="Generate Fret Hand Positions", command= lambda: execute_this('fhp'))
    GenerateFretHandPositionsBtn.grid(row=1, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    CopyODSoloFromBasicGtrBtn = Tkinter.Button(secPGB, text="Copy OD/Solo Markers from 5-lane", command= lambda: execute_this('pg_copy_od_solo'))
    CopyODSoloFromBasicGtrBtn.grid(row=1, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    secValidation = Tkinter.LabelFrame(root, text=" Validation: ")
    secValidation.grid(row=6, columnspan=5, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    CARVBtn = Tkinter.Button(secValidation, text="Run C3 Automatic Rules Validator (CARV)", command=RunCARV )
    CARVBtn.grid(row=1, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    logo = Tkinter.Frame(root, bg="#000")
    logo.grid(row=9, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = Tkinter.PhotoImage(file=path)
    imageLbl = Tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)    
    
    root.mainloop()
