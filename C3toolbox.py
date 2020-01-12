# -*- coding: cp1252 -*-
# -*- additions by: Alternity, kueller -*-
from reaper_python import *
import operator
import decimal
import base64
import math
import binascii
import os
import sys
from C3notes import *

global end_event
global tracks_array
global maxlen
global end_of_track
global instrument_ticks
global measures_array
global notesname_array
global divisions_array
global sustains_array
global default_pause
global sustainspace_array
global sustains_array
global debug
global array_instruments
global array_levels
global array_levels_id
global config
global drumsanimations_array
global da_lh
global promarkers
global double_pedal_bpm
global twohit_drums
global chord_threshold
global phrase_char

###########################################################
#
# GLOBALS
#
###########################################################
correct_tqn = 480 #We take the TQN from the Reaper project but Magma wants 480 TQN.
#This array keeps track of the each track's ID. It HAS to be run every time a function is run because the user can change track's position, thus changing ID
tracks_array = { "PART DRUMS" : 999,
                 "PART GUITAR" : 999,
                 "PART BASS" : 999,
                 "PART VOCALS" : 999,
                 "PART KEYS" : 999,
                 "PART REAL_KEYS_X": 999,
                 "PART REAL_KEYS_H": 999,
                 "PART REAL_KEYS_M": 999,
                 "PART REAL_KEYS_E": 999,
                 "PART KEYS_ANIM_LH": 999,
                 "PART KEYS_ANIM_RH": 999,
                 "HARM1": 999,
                 "HARM2": 999,
                 "HARM3": 999,
                 "EVENTS": 999,
                 "BEAT": 999,
                 "PART DRUMS 2X": 999,
                 "VENUE": 999,
                 "PART RHYTHM": 999,
                 "PART REAL_GUITAR": 999,
                 "PART REAL_GUITAR_22": 999,
                 "PART REAL_BASS": 999,
                 "PART REAL_BASS_22": 999
                 }
array_instruments = {
        "Drums" : "PART DRUMS",
        "2x Drums" : "PART DRUMS 2X",
        "Rhythm" : "PART RHYTHM",
        "Guitar" : "PART GUITAR",
        "Bass" : "PART BASS",
        "Keys" : "PART KEYS",
        "Pro Keys" : "PART REAL_KEYS",
        "Vocals" : "PART VOCALS",
        "Harmony 1" : "HARM1",
        "Harmony 2" : "HARM2",
        "Harmony 3" : "HARM3",
        "Pro Guitar" : "PART REAL_GUITAR",
        "Pro Guitar 22" : "PART REAL_GUITAR_22",
        "Pro Bass" : "PART REAL_BASS",
        "Pro Bass 22" : "PART REAL_BASS_22"
        }

array_dropdownid = { "PART DRUMS" : 0,
                     "PART GUITAR" : 1,
                     "PART BASS" : 2,
                     "PART KEYS" : 3,
                     "PART REAL_KEYS_X": 4,
                     "PART REAL_KEYS_H": 4,
                     "PART REAL _KEYS_H": 4,
                     "PART REAL_KEYS_M": 4,
                     "PART REAL_KEYS_E": 4,
                     "PART DRUMS 2X": 5,
                     "PART RHYTHM": 6,
                     "PART VOCALS": 7,
                     "PART REAL_GUITAR": 8,
                     "PART REAL_GUITAR_22": 8,
                     "PART REAL_BASS": 9,
                     "PART REAL_BASS_22": 9
                 }

array_dropdownvocals = { "PART VOCALS" : 0,
                     "HARM1" : 1,
                     "HARM2" : 2,
                     "HARM3" : 3
                 }

array_partlyrics = { "PART VOCALS" : "vocals",
                     "HARM1" : "harm1",
                     "HARM2" : "harm2",
                     "HARM3" : "harm3"
                 }

array_dropdownid_chords = { "PART GUITAR" : 0,
                     "PART BASS" : 1,
                     "PART KEYS" : 2,
                     "PART RHYTHM": 3
                 }
array_levels = { "Expert" : ["x", "_X"], "Hard" : ["h", "_H"], "Medium" : ["m", "_M"], "Easy" : ["e", "_E"] }
array_levels_id = { 'x' : 0, 'h' : 1, 'm' : 2, 'e' : 3 }
array_drumkit = { 'x' : '3', 'h' : '2', 'm' : '1', 'e' : '0' }
sustains_array = { 70 : correct_tqn*0.5, \
                   160 : correct_tqn*0.75, \
                   999 : correct_tqn*1.25 } #Sustains length array based on BPM
sustainspace_array = { 70 : { 'x' : correct_tqn*0.125, 'h': correct_tqn*0.25, 'm' : correct_tqn*0.5, 'e' : correct_tqn }, \
                       160 : { 'x' : correct_tqn*0.25, 'h': correct_tqn*0.25, 'm' : correct_tqn, 'e' : correct_tqn } , \
                       999 : { 'x' : correct_tqn*0.5, 'h': correct_tqn*0.5, 'm' : correct_tqn*0.75, 'e' : correct_tqn } }
                    #Sustains length array based on BPM
phrases_space = correct_tqn*0.0625 #1/64th space
leveldvisions_array = { 'x' : 's', 'h' : 'e', 'm' : 'q', 'e' : 'h' }
divisions_array = { "w" : 1, "h" : 0.5, "q" : 0.25, "e" : 0.125, "s" : 0.0625, "t" : 0.03125, "f" : 0.015625 } #Grid division
nextdivisions_array = { "w" : "h", "h" : "q", "q" : "e", "e" : "s", "s" : "t", "t" : "f" } #Next grid division
promarkers = {98 : 110, 99 : 111, 100 : 112}
drumsanimations_array = { 96: [24, 24], 97 : [26, 28], 98 : [31, 31], 99 : [42, 42], 100 : [38, 39], 104 : [36, 37], 110 : [47, 47], 111 : [49, 49], 112 : [51, 51] }
#Animation notes. The arrays are for Hard and Soft, when available (if not, the same value is repeated)
#104 is not a real note, it's for the CRASH1 option instead of CRASH2
da_lh = { 24: 24, 26 : 27, 28 : 29, 31 : 30, 42 : 43, 36 : 34, 37 : 35, 38 : 44, 39 : 45, 47 : 46, 49 : 48, 51 : 50 }
#Left hand notes, except for the two snares, and the kick that remains the same

two_chords = [ '', 'GR', 'GY', 'RY', 'RB', 'YB', 'YO', 'BO' ]
one_chords = [ '', 'G', 'R', 'Y', 'B', 'O' ]
medium_chords_o = [ 'GR', 'GY', 'RY', 'RB', 'YB', 'BO' ]
medium_chords = [ 'GR', 'GY', 'RY', 'RB', 'YB' ]
medium_notes = [ 'G', 'R', 'Y', 'B' ]

easy_chords_o = [ 'G', 'R', 'Y', 'B', 'O']
easy_chords = [ 'G', 'R', 'Y']
easy_chords_order = { 'G' : 1, 'R' : 2, 'Y' : 3, 'B' : 4, 'O' : 5 }
easy_chords_translation = { 'GR' : ['G', 'G'], 'GY' : ['R', 'R'], 'RY' : ['Y', 'Y'], 'RB' : ['Y', 'B'], 'YB' : ['Y', 'B'], 'YO' : ['Y', 'O'], 'BO' : ['Y', 'O'] }
easy_notes = [ 'G', 'R', 'Y' ]
easy_singlenotes_array = { 'G' : 'G', 'R' : 'R', 'Y' : 'R', 'B' : 'Y', 'O' : 'Y' }

hard_chords_o = {'84, 86, 88' : [84, 88], '86, 87, 88' : [87, 88], '85, 87, 88' : [86, 88], '85, 86, 88' : [85, 88], '84, 85, 88' : [84, 87], '84, 87, 88' : [85, 88], '84, 86, 88' : [85, 88], '84, 87, 88' : [85, 88], '85, 86, 87' : [85, 87], '84, 86, 87' : [84, 87], '84, 85, 88' : [84, 87], '84, 85, 87' : [84, 86], '84, 85, 86' : [84, 85] }
hard_chords = {'84, 86, 88' : [84, 88], '86, 87, 88' : [87, 88], '85, 87, 88' : [86, 88], '85, 86, 88' : [86, 87], '84, 85, 88' : [84, 87], '84, 87, 88' : [85, 88], '84, 86, 88' : [85, 88], '84, 87, 88' : [85, 88], '85, 86, 87' : [85, 87], '84, 86, 87' : [85, 86], '84, 85, 88' : [84, 87], '84, 85, 87' : [84, 86], '84, 85, 86' : [84, 85] }

medium_chords_order = { 'GR' : 1, 'GY' : 2, 'RY' : 3, 'RB' : 4, 'YB' : 5, 'YO' : 6, 'BO' : 7, 'G' : 1, 'R' : 2, 'Y' : 3, 'B' : 4, 'O' : 5 }

octave_chords = { 'GO' : [ 'YO', 'RB', 'GY'], 'GB' : [ 'RB', 'GY', 'RY'], 'RO' : [ 'YO', 'RB', 'YB'] }

#This arrays fixes simultaneous hits. When two crashes are involved, hi ht and ride are mapped to crash1.
#If crash1 was selected as an option, it's mapped to crash2
twohit_drums = { '3142' : [da_lh[31], 42], '3136' : [da_lh[36], 38], '3137' : [da_lh[37], 39], '3138' : [da_lh[36], 38], '3139' : [da_lh[37], 39], '3149' : [da_lh[31], 49], '3151' : [da_lh[31], 51], \
                 '4749' : [da_lh[47], 49], '4751' : [da_lh[47], 51], \
                 '3642' : [da_lh[36], 38], '3647' : [36, da_lh[47]], '3649' : [36, da_lh[49]], \
                 '3742' : [da_lh[37], 39], '3747' : [37, da_lh[47]], '3749' : [37, da_lh[49]], \
                 '3842' : [da_lh[36], 38], '3847' : [38, da_lh[47]], '36849' : [38, da_lh[49]], \
                 '3942' : [da_lh[37], 39], '3947' : [39, da_lh[47]], '3949' : [39, da_lh[49]], \
                 '4247' : [da_lh[47], 42], '4251' : [da_lh[42], 51], \
                 '4951' : [da_lh[49], 51] }
double_pedal_bpm = 120 #The threshold under which we allow 1/16th kick notes on single pedal
maxlen = 1048576 #Used for the MIDI chunk editing and other functions
end_event = 0 #If no end_event is set or it's not set at the right position, looping through notes after the end_event will bring up an error
default_pause = correct_tqn*4*3 #The default space between notes that triggers an idle event
chord_threshold = 0.07 #7% is the defauly threshold for chords reduction
invalid_chars = ',:;"'
phrase_char = '@' #The character we use to tell the phrase markers script to start a new phrase
debug = 1

#DICTIONARY OF FREQUENTLY USED ARRAYS
# measures_array
# An array containing all measures with number, ticks of x.1, time signature, number of ticks per beat and BPM (a single value taken from the BPM marker nearest to x.1)
# 0. Measure number, 1. ticks of Mx.1, 2. denominator, 3. numerator, 4. ticks per beat, 5. BPM

# array_notes
# An array containing notes object, meaning a single element per note. 
# 0. 'E' or 'e' (unselected or selected), 1. location, 2. pitch, 3. velocity, 4. duration, 5. noteonoffchannel (9n or 8n)
# 0. 'X' or 'x' (unselected or selected), 1. location, 2. pre-text, 3. text, 4. post-text, 5. event type code)
# Event type code: ff01: TEXT MARKER, ff03 : TRACKNAME, ff05 : LYRICS

###########################################################

###########################################################
#
# UTILITIES
#
###########################################################

def PM(message):
    global config
    
    if config['debug'] == '1':
        RPR_ShowConsoleMsg(str(message))

def log(function, var):
    
    #This function logs all functions and variables passed
    #if config['log'] == '1':
        #with open ("log.txt", "a") as myfile:
            #myfile.write("appended text")
    a=5
            
def get_curr_project_filename():
    proj = RPR_EnumProjects(-1, "", 512)
    if proj[2] == "":
        return "Unsaved project"
    else:
        return proj[2]
        
def count_notes(array, start, end, notes, what, instrument):
    #array of notes, start, end, which notes to count, note pitch (0) or note type (1), instrument is id
    #start and end are optional
    #Returns an array with notes as key and note count as value, sorted by value, descending
    
    instrument_name = ''
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    array_count = {}
    for x in range(0, len(array)):
        #PM("\n")
        #PM(notes_dict[array[x][2]][1])
        if array[x][2] not in notes_dict:
            invalid_note_mb(array[x], instrumentname)
            return {}

        if (((start or end) and array[x][1] >= start and array[x][1] <= end) or (start == 0 and end == 0)) and ((what == 0 and array[x][2] in notes) or (what == 1 and notes_dict[array[x][2]][1] in notes)):
            if str(array[x][2]) in array_count:
                array_count[str(array[x][2])]+=1
            else:
                array_count[str(array[x][2])]= 1
    
    array_count = sorted(array_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return array_count


def mbt(position): #Returns an array with 0. measure, 1. beat, 2. ticks, 3. ticks relative to start of measure
    for x in range(0, len(measures_array)):
        if measures_array[x][1] <= position:
            m = x+1
            relative_position = position-measures_array[x][1]
            b = int(math.floor(relative_position/measures_array[x][4]))+1
            t = int(relative_position-((b-1)*measures_array[x][4]))
    return [m, b, t, relative_position]

def invalid_note_mb(note, instrumentname):
    m,b = mbt(int(note[1]))[:2]
    RPR_MB("Invalid note %d found in %s at position %d.%d" % (note[2], instrumentname, m, b), "Invalid note", 0)

def selected_range(array): #Returns an array with the first selected note at 0 and last selected note at 1
    #array must either be the notes or the events array, with absolute location at 1
    first_note = "unset"
    last_note = 0
    #Loop through array elements and find the first selected note: set first_note variable
    #Continue loop and set the first next selected note as last_note
    #Continue loop and if a new selected note has a starting point higher than last_note, set last_note to it
    for x in range(0,len(array)):
        if array[x][0] == 'e' or array[x][0] == 'x':
            #PM("\nlast_note: " + str(last_note) + " - " str()
            
            if first_note == "unset":
                first_note = array[x][1]
            elif array[x][1] > last_note:
                last_note = array[x][1]
    return [first_note, last_note]

def selected_notes(array): #Returns an array with only selected notes and with non selected notes
    array_valid = []
    array_notes = []
    for x in range(0, len(array)):
        note = array[x]
        if note[0] == 'e':
            array_valid.append(note)
        else:
            array_notes.append(note)
    return [array_valid, array_notes]

def note_objects(array): #Returns an array of note objects, meaning chords are one array element
    #PM("\n\nnoteobjectsbefore: \n")
    #PM(array)
    #PM("\n\n")
    noteobjects_array = []
    # 0. 'E' or 'e' (selected or unselected) (array)
    # 1. location
    # 2. pitch (array)
    # 3. velocity(array)
    # 4. duration (array)
    # 5. noteonoffchannel (9n or 8n) (array)
    # 6. chord
    location = array[0][1]
    note_object = [[], [], [], [], [], [], []]
    for x in range(0, len(array)):
        note = array[x]
        old_location = location
        location = note[1]
        #If the position changes, we need to first append to the main array the note_object array because there are no more notes on that location
        if location != old_location:
            note_object[6].sort()
            noteobjects_array.append(note_object)
            note_object = [[], [], [], [], [], [], []]
        for j in range(0, 6):
            note_object[j].append(note[j])
        note_object[6].append(note[2])
    note_object[6].sort()
    noteobjects_array.append(note_object)
    return noteobjects_array

def valid_notes(array, level, first_measure, last_measure, instrumentname, pro, selected):
    #This function returns an array of notes not to be touched (OD, markers, etc.) and an array of notes of the level to be edited
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    array_validnotes = []
    array_notes = []
    for x in range(0,len(array)):
        note = array[x]
        this_measure = mbt(int(note[1]))[0]
        if ((level != '' and notes_dict[note[2]][1] == level) or (level == '' and "notes" in notes_dict[note[2]][1])) and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_validnotes.append(note)
        else:
            array_notes.append(note)
    return [array_notes, array_validnotes]

def add_objects(array_notes, array_objects): #Adds objects as notes to the array_notes array
    for x in range(0,len(array_objects)):
        note = array_objects[x]
        for j in range(0, len(note[6])):
            if(len(note[4]) == 1):
                length = note[4][0]
            else:
                length = note[4][j]
            array_notes.append([note[0][j], note[1][0], note[2][j], note[3][j], length, note[5][j]])
    return array_notes

def sections(array_notesevents, what):
    #Returns an array with subsections in ticks
    for x in range(0, len(array_notesevents)):
        note = array_notesevents[x]

def level(array, instrument):
    #Returns the selected level, instrument is id
    instrument_name = ''
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    #If it's pro keys, let's catch level right away and return it
    if "KEYS_X" in instrumentname:
        return 'x'
    elif "KEYS_H" in instrumentname:
        return 'h'
    elif "KEYS_M" in instrumentname:
        return 'm'
    elif "KEYS_E" in instrumentname:
        return 'e'

    #If not, we need to loop through selected notes
    for x in range(0, len(array)):
        note = array[x]
        if note[0] == 'e':
            if note[2] not in notes_dict:
                invalid_note_mb(note, instrumentname)
                return None

            if notes_dict[note[2]][1] == "notes_x":
                return 'x'
            elif notes_dict[note[2]][1] == "notes_h":
                return 'h'
            elif notes_dict[note[2]][1] == "notes_m":
                return 'm'
            elif notes_dict[note[2]][1] == "notes_e":
                return 'e'

    #If still no joy, return x
    return 'x'

def remap_notes(array_chords, array_translation): #Remap all chords in a song to allowed chords
    array_chords_sorted = sorted(array_chords.iteritems(), key=operator.itemgetter(1), reverse=True)
    array_valid_chords = []
    #We get the most used chords and build an array
    for j in range(0, len(array_translation)):
        
        chord = array_chords_sorted[j][0]
        array_valid_chords.append(chord)
    if len(chord) > 1:
        onetwo_chords = two_chords
    else:
        onetwo_chords = one_chords
    array_chords_sorted = []
    array_valid_chords_letters = list(array_valid_chords)
    #Now we need to sort it, so we convert chords in numbers
    for j in range(0, len(array_valid_chords)):
        chord = array_valid_chords[j]
        chord_number = medium_chords_order[chord]
        array_chords_sorted.append(chord_number)
    array_chords_sorted.sort()
    #We now have a sorted array of chords represented in numbers. Let's convert it back...
    array_valid_chords = []
    for j in range(0, len(array_chords_sorted)):
        chord_number = array_chords_sorted[j]
        chord = onetwo_chords[chord_number]
        array_valid_chords.append(chord)
    array_conversions = []
    for j in range(0, len(array_translation)):
        array_conversions.append([array_valid_chords[j], array_translation[j]])
    return [array_conversions, array_valid_chords_letters]
            
###########################################################


###########################################################
#
# PREPPING AND COMMON FUNCTIONS
#
###########################################################


def get_trackid(): #Returns the id for the currently selected track
    global tracks_array
    sel = RPR_CountSelectedTracks(0)
    if sel > 1 or sel == 0:
        #More than one or no track selected, can't proceed
        item = ""
    else:
        item = RPR_GetSelectedTrack(0,0)
        source = RPR_GetSetMediaTrackInfo_String(item, "P_NAME", "", 0)[3]  

        if "DRUMS" in source and source != "PART DRUMS":
            source = "PART DRUMS 2X"
        elif "RHYTHM" in source:
            source = "PART RHYTHM"
        elif source == "PART REAL _KEYS_H":
            source = "PART REAL_KEYS_H"

        if source in tracks_array:
            return tracks_array[source]
        else:
            #The selected track is unrecognised
            return 999

def get_trackname(): #Returns the name for the currently selected track
    instrument = get_trackid()
    instrumentname = ''
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    if instrumentname:
        return instrumentname

def get_time_signatures(instrument_ticks):
    #This function creates measures array, an array containing all measures with their TS, BPM, starting point, etc.
    tsden_array = {'1048' : 16, '983' : 15, '917' : 14, '851' : 13, '786' : 12, '720' : 11, '655' : 10, '589' : 9, '524' : 8, '458' : 7, '393' : 6, '327' : 5, '262' : 4, '196' : 3, '131' : 2, '65': 1}
    tsnum_array = {16 : 577, 15 : 41, 14 : 505, 13 : 969, 12 : 433, 11 : 897, 10 : 361, 9: 825, 8 : 289, 7 : 753, 6 : 217, 5 : 681, 4 : 145, 3: 609, 2 : 73, 1: 537}
    #Examples:
    #4/4: 262 and 148 (145 is 1, 145+3 is 4)
    #7/8: 524 and 295 (289 is 1, 289+6 is 7)
    maxlen = 1048576
    trkptr = RPR_CSurf_TrackFromID(0,0)

    # Get Envelope Pointer:
    envptr = RPR_GetTrackEnvelopeByName( trkptr, 'Tempo map' )
    envstr = ''
    # Get Envelope Data:
    envstate = RPR_GetSetEnvelopeState(envptr, envstr, maxlen)
    nodes_array = []
    timesigchanges_array = []
    timesignature = '262148' #By default it's 4/4
    chunk = ""+envstate[2]
    vars_array = chunk.split("\n")
    
    #Create an array of 0. seconds of the point, 1. BPM, 2. time signature denominator, 3. time signature numerator , 4. ticks since 0
    for j in range(0, len(vars_array)):
        if vars_array[j].startswith('PT '):
            node = vars_array[j].split(" ")
            #if node[1] == '0.000000000000':
            #    node[1] = 0
            
            node_array = [float(node[1]), float(node[2])]
            if len(node) > 4:
                if node[4] != '0':
                    timesignature = str(node[4])
                
            if len(timesignature) > 6:
                numerator = timesignature[4:]
                denominator = timesignature[:4]
            else:
                numerator = timesignature[3:]
                denominator = timesignature[:3]
            timesignature_denominator = tsden_array[denominator]
            timesignature_numerator = (int(numerator)-tsnum_array[timesignature_denominator])+1
            node_array.append(timesignature_numerator)
            node_array.append(timesignature_denominator)
            nodes_array.append(node_array)

    #Create an array of TS changes: 0. BPM, 1. time signature denominator, 2. time signature numerator, 3. ticks passed since 0 
    ticks_passed = 0
    if len(nodes_array) > 0:
        old_ts = str(nodes_array[0][2])+str(nodes_array[0][3])
        timesigchanges_array.append([nodes_array[0][0], nodes_array[0][2], nodes_array[0][3], 0])
        nodes_array[0].append(0)
        for j in range(1, len(nodes_array)):
            ticks_per_second = (instrument_ticks*nodes_array[j-1][1])/60
            time_passed = nodes_array[j][0]-nodes_array[j-1][0]
            ticks_passed = (time_passed*ticks_per_second)+ticks_passed
            ticks_passed = decimal.Decimal(ticks_passed)
            ticks_passed = round(ticks_passed,10)
            nodes_array[j].append(ticks_passed)
            cur_ts = str(nodes_array[j][2])+str(nodes_array[j][3])
            if(old_ts <> cur_ts):
                timesigchanges_array.append([nodes_array[j][0], nodes_array[j][2], nodes_array[j][3], ticks_passed])
            old_ts = str(nodes_array[j][2])+str(nodes_array[j][3])         
            
        #PM(nodes_array)
        #Loop through the TS array and for each time signature span find out duration and then divide by numerator and denominator. The result is the number of measures in that ts
        m = 0
        x = 0 #This is needed in case we only have one time signature event
        measures_array = [] #0. Measure number, 1. ticks of Mx.1, 2. denominator, 3. numerator, 4. ticks per beat, 5. BPM

        for x in range(1, len(timesigchanges_array)):
            
            duration = float(timesigchanges_array[x][3]-timesigchanges_array[x-1][3])
            duration = round(duration, 0)
            duration = int(duration)

            divider = instrument_ticks/(timesigchanges_array[x-1][2]*0.25)
            number_of_measures = round(round(duration/divider)/timesigchanges_array[x-1][1], 0)
            number_of_measures = int(number_of_measures)

            ticks_per_measure = duration/number_of_measures
            ticks_per_beat = ticks_per_measure/timesigchanges_array[x][2]
            for j in range(0, number_of_measures):
                m+=1
                ticks_start = float((timesigchanges_array[x-1][3])+(j*ticks_per_measure))
                ticks_start = round(ticks_start, 0)
                ticks_start = int(ticks_start)
                measures_array.append([m, ticks_start, timesigchanges_array[x-1][1], timesigchanges_array[x-1][2], divider])
        #Now we need to add all measures from the last (or in some cases only) BPM marker to the end of the song, marked by the end event
        ticks_start = float(timesigchanges_array[len(timesigchanges_array)-1][3])
        ticks_start = round(ticks_start, 0)
        ticks_start = int(ticks_start)
        ticks_per_measure = instrument_ticks/(timesigchanges_array[x][2]*0.25)
        ticks = ticks_per_measure*timesigchanges_array[x][1]
        ticks_per_beat = ticks/timesigchanges_array[x][2]
        ticks_startmeasure = ticks_start
        loop_measure = 0
        while (ticks_startmeasure < end_event+ticks): #The whole loop runs for one measure longer than the end event
            m+=1
            ticks_startmeasure = ticks_start+(ticks*loop_measure)
            loop_measure+=1
            measures_array.append([m, ticks_startmeasure, timesigchanges_array[x][1], timesigchanges_array[x][2], ticks_per_measure])
        #Now we add the BPM for each measure taking the BPM value of the measure from nodes_array
        ok = 0

        for x in range(0, len(measures_array)):
            ticks_start = measures_array[x][1]
            ok = 0
            for j in reversed(range(0, len(nodes_array))):
                #PM("\n")
                #PM(str(int(round(float(ticks_start), 0)))+" <= "+str(int(float(nodes_array[j][4])))+" : "+str(nodes_array[j][1]))
                if int(round(float(ticks_start), 0)) >= int(float(nodes_array[j][4])):
                    measures_array[x].append(nodes_array[j][1])
                    ok = 1
                    #PM("\n")
                    break
            if ok == 0:
                measures_array[x].append(nodes_array[j][1])
                ok = 0
        #PM("\n")
        #PM(measures_array)
        return measures_array
    

def process_instrument(instrument): #Creates an array of all notes/events
    PM(instrument)
    global end_event
    global end_of_track
    mi = RPR_GetMediaItem(0,instrument)
    chunk = ""
    maxlen = 1048576
    (boolvar, mi, chunk, maxlen) = RPR_GetSetItemState(mi, chunk, maxlen)
    vars_array = ""
    notes_array = []
    conto_vars_array = 0
    vars_array = chunk.split("\n")
    conto_vars_array = len(vars_array)
    alertstring="real_keys_lh"+" - "+str(conto_vars_array)+"\n"
    noteloc = 0
    decval = ""
    encText = ""
    #CYCLING THROUGH CHUNK TO CREATE AN ARRAY OF NOTES
    notestring = "a\n"
    vars_array_string = ""
    ticks = 0
    end_firstpart = 0
    start_secondpart = 0
    
    for j in range(0, conto_vars_array):
        note = ""
        if vars_array[j].startswith('E ') or vars_array[j].startswith('e '):
            note = vars_array[j].split(" ")
            if len(note) >= 5:
                decval = int(note[3], 16)
                noteloc = noteloc + int(note[1])
                notes_array.append(note[0]+" "+str(noteloc)+" "+note[2]+" "+str(decval)+" "+str(note[4]))
        elif vars_array[j].startswith('<X') or vars_array[j].startswith('<x'):
            note = vars_array[j].split(" ")
            if len(note) >= 2:
                noteloc = noteloc + int(note[1])
                encText = vars_array[j+1]
                encClose = vars_array[j+2]
                notes_array.append(note[0]+" "+str(noteloc)+" "+note[2]+" "+str(encText)+" "+encClose)
                if base64.b64decode(str(encText))[2:] == '[end]':
                    end_event = noteloc
        elif "HASDATA" in vars_array[j]:
            note = vars_array[j].split(" ")
            ticks = int(note[2])
            if ticks != 480:
                result = RPR_MB( "One of the MIDI tracks isn't set to 480 ticks per beat. This will break Magma. CAT will now exit", "Invalid ticks per quarter", 0)
                return
        elif "<SOURCE MIDI" in vars_array[j]:
            end_firstpart = j+2 #it's the last element before the MIDI notes/events chunk
        elif "IGNTEMPO" in vars_array[j]:
            start_secondpart = j-1 #it's the first element after the MIDI notes/events chunk
    array_instrument = [ticks, notes_array, end_firstpart, start_secondpart]
    end_of_track = notes_array[-1]

    return array_instrument

def create_notes_array(notes): #instrument is the instrument shortname, NOT the instrument track number
    array_rawnotes = [] #An array containing only notes in raw format, notes on and off
    array_rawevents = [] #An array containing all text markers/events
    array_notes = []    #An array containing only notes, with:
                        #0. 'E' or 'e' (unselected or selected), 1. location, 2. pitch, 3. velocity, 4. duration, 5. noteonoffchannel
    array_events = [] #An array containing only text markers/events
    #First off we sort the notes from the markers, so it's easier to loop through notes

    for x in range(0, len(notes)):
        if notes[x].startswith('E') or notes[x].startswith('e'):
            array_rawnotes.append(notes[x])
        else:
            array_rawevents.append(notes[x])
    #Now we loop through the notes to remove all note off events and set a length for the notes

    for x in range(0, len(array_rawnotes)):
        note_bit = array_rawnotes[x].split(" ")
        if note_bit[2].startswith('9') and note_bit[4] != '00':
            for y in range(x, len(array_rawnotes)):
                cur_note = array_rawnotes[y].split(" ")

                if x != y and cur_note[3] == note_bit[3] and int(cur_note[1]) > int(note_bit[1]) and (cur_note[2].startswith('8') or cur_note[4] == '00'):
                    #We have the note off for the current note on event
                    #PM(str(note_bit[0])+ str(note_bit[1])+str(note_bit[3])+str(note_bit[4])+ str(int(cur_note[1])-int(note_bit[1]))+ str(note_bit[2]))
                    #PM("\n")
                    array_notes.append([note_bit[0], int(note_bit[1]), int(note_bit[3]), note_bit[4], (int(cur_note[1])-int(note_bit[1])), note_bit[2]])
                    break
             
    for x in range(0, len(array_rawevents)):
        note_bit = array_rawevents[x].split(" ")
        encText = note_bit[3]
        event_header = str(binascii.a2b_base64(encText).encode("hex"))[:4]
        lyric = base64.b64decode(str(encText))[2:]
        array_events.append([note_bit[0], int(note_bit[1]), note_bit[2], str(lyric), note_bit[4], event_header])
    
    return [array_notes, array_events] 

def rebuild_array(array_notesevents):
    global end_of_track
    global correct_tqn
    #Create a new temp array
    array_temp = [] #This array will contain all events/notes and it will be used for sorting. Its content will then go in a raw text array
    array_raw = []  
    #Loop through each note and convert the note on event in raw format to add it to the raw array
    for x in range(0, len(array_notesevents[0])):
        
        array_temp.append([array_notesevents[0][x][0], int(array_notesevents[0][x][1]), array_notesevents[0][x][5], (hex(int(array_notesevents[0][x][2])))[2:], array_notesevents[0][x][3]])
        #and create a note off event with absolute location
        array_temp.append([array_notesevents[0][x][0], int(array_notesevents[0][x][1])+int(array_notesevents[0][x][4]), str("8"+str(array_notesevents[0][x][5])[1:]),(hex(int(array_notesevents[0][x][2])))[2:], "00"])
    
    for x in range(0, len(array_notesevents[1])):
        hex_lyric = array_notesevents[1][x][5] + array_notesevents[1][x][3].encode("hex")
        encoded_text = str(base64.encodestring(hex_lyric.decode('hex')))
        #PM("encoded_text: "+encoded_text+"\n")
        array_temp.append([array_notesevents[1][x][0], int(array_notesevents[1][x][1]), array_notesevents[1][x][2], encoded_text, array_notesevents[1][x][4]])
    #Incorporate the events from array_rawevents and sort by absolute location
    array_temp.sort(key=operator.itemgetter(1,0))
    
    #We add the end of track event so the MIDI track doesn't cut off
    end_of_track_array = end_of_track.split(" ")
    end_of_track_time = int(end_of_track_array[1])
    if array_temp[-1][1] > int(end_of_track_array[1]):
        end_of_track_time = array_temp[-1][1]+correct_tqn
    #array_temp.append([end_of_track_array[0], end_of_track_time, end_of_track_array[2], end_of_track_array[3], end_of_track_array[4]])
    array_temp.append([end_of_track_array[0], end_of_track_time, end_of_track_array[2], (hex(int(end_of_track_array[3])))[2:], end_of_track_array[4]])
    #Loop through the rawarray. Set location of all notes based on difference between location of note x and of note x-1 of the rawarray

    if array_temp[0][0].startswith('E') or array_temp[0][0].startswith('e'):      
        array_raw.append(array_temp[0][0]+" "+str(array_temp[0][1])+" "+str(array_temp[0][2])+" "+str(array_temp[0][3])+" "+str(array_temp[0][4])) 
    else:
        array_raw.append(array_temp[0][0]+" "+str(array_temp[0][1])+" "+str(array_temp[0][2])+"\n  "+str(array_temp[0][3])+"\n"+str(array_temp[0][4]))
        
    for x in range(1, len(array_temp)):
        new_location = array_temp[x][1]-array_temp[x-1][1]
        if array_temp[x][0].startswith('E') or array_temp[x][0].startswith('e'): 
            array_raw.append(array_temp[x][0]+" "+str(new_location)+" "+str(array_temp[x][2])+" "+str(array_temp[x][3])+" "+str(array_temp[x][4]))
        else:
            array_raw.append(array_temp[x][0]+" "+str(new_location)+" "+str(array_temp[x][2])+"\n  "+array_temp[x][3]+"\n"+str(array_temp[x][4]))
    #PM(array_raw)       
    return array_raw
    

def rebuild_chunk(notes_array, instrument, end, start):
    #Let's start by putting the notes/events portion of the chunk back together. The array is already prepped here.
    noteschunk = ""
    for x in range(0, len(notes_array)):
        if notes_array[x].startswith('E') or notes_array[x].startswith('e'):
            noteschunk+=notes_array[x]+"\n"
        else:
            #event = notes_array[x].split("|")
            #PM(notes_array[x]) 
            #noteschunk+=event[0]+"\n"+event[1]+"\n"+event[2]+"\n"
            noteschunk+=notes_array[x]+"\n"
    #The notes/events portion of the chunk is done, now we loop through the whole chunk to find the spot where we need to snip    
    bi = RPR_GetMediaItem(0,instrument)
    first_chunk = ""
    second_chunk = ""
    maxlen = 1048576
    instrument = ""
    subchunk = ""
    (boolvar, bi, subchunk, maxlen) = RPR_GetSetItemState(bi, subchunk, maxlen)
    vars_array = subchunk.split("\n")

    for j in range(0, end+1):
        first_chunk+=vars_array[j]+"\n"
        
    for k in range(start, len(vars_array)):
        second_chunk+=vars_array[k]
        if k < vars_array :
            second_chunk+="\n"
            
    chunk = first_chunk+noteschunk+second_chunk
    return chunk

def prep_tracks():
    global maxlen
    global tracks_array
    num_mi = RPR_CountMediaItems(0)

    for i in range(0, num_mi):
        mi = RPR_GetMediaItem(0,i)
        trackID = RPR_GetMediaItem_Track(mi)
        trackname = RPR_GetSetMediaTrackInfo_String(trackID, "P_NAME", "", 0)[3]
        chunk = ""
        instrument = ""
        (boolvar, mi, chunk, maxlen) = RPR_GetSetItemState(mi, chunk, maxlen)
        #CYCLING THROUGH ALL TRACKS TO FIND THOSE RELEVANT
        #This check needs to go off everytime a command is issued because if the user changes position of the tracks the IDs change
        if "PART BASS" == trackname:
            tracks_array["PART BASS"] = i
        elif "PART DRUMS 2X" == trackname or "PART DRUMS 2x" == trackname or "PART DRUMS_2x" == trackname or "PART DRUMS_2X" == trackname:
            tracks_array["PART DRUMS 2X"] = i
        elif "PART DRUMS" == trackname:
            tracks_array["PART DRUMS"] = i
        elif "PART GUITAR" == trackname:
            tracks_array["PART GUITAR"] = i
        elif "PART VOCALS" == trackname:
            tracks_array["PART VOCALS"] = i
        elif "PART KEYS" == trackname:
            tracks_array["PART KEYS"] = i
        elif "KEYS_X" in trackname:
            tracks_array["PART REAL_KEYS_X"] = i
        elif "KEYS_H" in trackname:
            tracks_array["PART REAL_KEYS_H"] = i
        elif "KEYS_M" in trackname:
            tracks_array["PART REAL_KEYS_M"] = i
        elif "KEYS_E" in trackname:
            tracks_array["PART REAL_KEYS_E"] = i
        elif "PART KEYS_ANIM_RH" == trackname:
            tracks_array["PART KEYS_ANIM_RH"] = i
        elif "PART KEYS_ANIM_LH" == trackname:
            tracks_array["PART KEYS_ANIM_LH"] = i   
        elif "HARM1" == trackname:
            tracks_array["HARM1"] = i
        elif "HARM2" == trackname:
            tracks_array["HARM2"] = i
        elif "HARM3" == trackname:
            tracks_array["HARM3"] = i
        elif "EVENTS" == trackname:
            tracks_array["EVENTS"] = i
        elif "BEAT" == trackname:
            tracks_array["BEAT"] = i
        elif "VENUE" == trackname:
            tracks_array["VENUE"] = i  
        elif "PART REAL_GUITAR" == trackname:
            tracks_array["PART REAL_GUITAR"] = i
        elif "PART REAL_GUITAR_22" == trackname:
            tracks_array["PART REAL_GUITAR_22"] = i
        elif "PART REAL_BASS" == trackname:
            tracks_array["PART REAL_BASS"] = i  
        elif "PART REAL_BASS_22" == trackname:
            tracks_array["PART REAL_BASS_22"] = i          
        else:
            instrument = "???"
    #PM("\ntracks_array:\n")
    #PM(tracks_array)

def write_midi(instrument, array, end_part, start_part):
    global maxlen
    rebuilt_array = rebuild_array(array)
    chunk = rebuild_chunk(rebuilt_array, instrument, end_part, start_part)
    mi = RPR_GetMediaItem(0,instrument)
    (boolvar, mi, chunk, maxlen) = RPR_GetSetItemState(mi, chunk, maxlen)

###########################################################

###########################################################
#
# COMMANDS
#
###########################################################

def filter_notes(instrument): #Anything that's not a proper note or a text event is filtered out
    global maxlen
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]

    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    write_midi(instrument, array_notesevents, end_part, start_part)

def polish_notes(instrument, grid, tolerance, selected):
    #All notes off by tolerance on a grid are snapped
    global maxlen
    
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]

    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = array_notesevents[0]
    array_events = array_notesevents[1]

    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    if "REAL_KEYS" in instrumentname or "KEYS_ANIM" in instrumentname or "VOCALS" in instrumentname:
        level = "notes"
    else:
        level = "notes_x"
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    division = int(math.floor((correct_tqn*4)*divisions_array[grid]))
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notes)[0]))[0]
        last_measure = mbt(int(selected_range(array_notes)[1]))[0]
        if first_measure == last_measure:
            result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
            return

    for x in range(0, len(array_notes)):
        note = array_notes[x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrumentname)
            return
        position = mbt(note[1])[3]
        if (selected and mbt(int(note[1]))[0] >= first_measure and mbt(int(note[1]))[0] <= last_measure) or selected == 0:
            if "notes" in notes_dict[note[2]][1]:
                grid_check = int(math.floor(position/division))

                diff_after = position-(grid_check*division)

                diff_before = division - (position-(grid_check*division))

                if diff_after > 0 and diff_after < tolerance:
                    note[1] -= diff_after
                elif diff_before > 0 and diff_before < tolerance : #Slightly off, snap
                    note[1] += diff_before
                    
    write_midi(instrument, [array_notes, array_events], end_part, start_part)

def cleanup_notes(instrument, grid, level, selected):
    #All notes shorter than grid will be made 1/16th or the longest possible taking the following note into consideration
    global maxlen
    
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]

    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = array_notesevents[0]
    array_events = array_notesevents[1]

    leveltext = level
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    if "REAL_KEYS" in instrumentname or "KEYS_ANIM" in instrumentname:
        leveltext = "notes"
    else:
        leveltext = "notes_"+leveltext
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    division = int(math.floor((correct_tqn*4)*divisions_array[grid]))
    first_measure = 0
    last_measure = 0
    array_validnotes = []
    array_notes = []

    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
    if selected and first_measure == last_measure:
        result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
        return
    
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        #PM(note)
        this_measure = mbt(int(note[1]))[0]

        if note[2] in notes_dict and notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_validnotes.append(note)
        else:
            array_notes.append(note)

    array_validobjects = note_objects(array_validnotes)
    for x in range(0,len(array_validobjects)):
        note = array_validobjects[x]
        duration = note[4][0]
        new_length = 8
        if (selected and mbt(int(note[1]))[0] >= first_measure and mbt(int(note[1]))[0] <= last_measure) or selected == 0:
            if duration < division:
                if x+1 == len(array_validobjects):
                    new_length = correct_tqn/4
                elif note[1][0]+(correct_tqn/4) <= array_validobjects[x+1][1][0]:
                    new_length = correct_tqn/4
                elif note[1][0]+(correct_tqn/8) <= array_validobjects[x+1][1][0]:
                    new_length = correct_tqn/8
                elif note[1][0]+(correct_tqn/16) <= array_validobjects[x+1][1][0]:
                    new_length = correct_tqn/16
                elif note[1][0]+(correct_tqn/32) <= array_validobjects[x+1][1][0]:
                    new_length = correct_tqn/32
                else:
                    new_length = 8
                for j in range(0, len(note[4])):
                    note[4][j] = new_length
    array_notes = add_objects(array_notes, array_validobjects)
    write_midi(instrument, [array_notes, array_events], end_part, start_part)
        
        
def create_beattrack(halve, sel): #Call with halve to create an halved beat track
    global maxlen
    if halve:
        moltiplicatore = 2
    else:
        moltiplicatore = 1
    #Get notes array
    array_instrument_data = process_instrument(tracks_array["BEAT"])
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notes = create_notes_array(array_instrument_notes)
    array_beats = [] #0. 'e', 1. location, 2. pitch, 3. velocity, 4. duration, 5. noteonoffchannel
    last_measure = len(measures_array)
    first_measure = 1
    if(sel):
        array_beats_full = array_notes[0]
        first_measure = mbt(int(selected_range(array_beats_full)[0]))[0]
        last_measure = mbt(int(selected_range(array_beats_full)[1]))[0]
        if first_measure == last_measure:
            result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
            return
        #Once finished, delete all selected notes from the array plus those in the same measures
        for x in range(0,len(array_beats_full)):
            if array_beats_full[x][0] == 'E':
                this_measure = mbt(int(array_beats_full[x][1]))[0]
                if this_measure < first_measure or this_measure > last_measure:
                    array_beats.append(array_beats_full[x])
    #Loop through measures_array and put a downbeat note (12) at the 1 and an upbeat note (13) on the other beats
    evenodd = 0
    for x in range(first_measure-1, last_measure):
        ticks_per_beat = measures_array[x][4]
        ticks_start = measures_array[x][1]
        if(ticks_start < end_event):
            if(moltiplicatore == 2 and evenodd%2==0) or moltiplicatore == 1:
                array_beats.append(['e', ticks_start, 12, 64, correct_tqn/4, 96]) #Downbeat
            else:
                array_beats.append(['e', ticks_start, 13, 64, correct_tqn/4, 96]) #Upbeat because of halving
            ticks_start+=correct_tqn*moltiplicatore
            if x+1 == len(measures_array):
                start_check = end_event
            else:
                start_check = measures_array[x+1][1]
            while ticks_start <= (start_check-correct_tqn):
                if(ticks_start < end_event):
                    array_beats.append(['e', ticks_start, 13, 64, correct_tqn/4, 96]) #Upbeat
                ticks_start+=correct_tqn*moltiplicatore
        evenodd+=1
    write_midi(tracks_array["BEAT"], [array_beats, array_notes[1]], end_part, start_part)

def create_triplets(instrument):
    #instrument = full track name (PART DRUMS, in example)
    global maxlen
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]

    #Get notes
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    
    #Get array of valid notes
    array_notes = selected_notes(array_notesevents[0])[1] #The final array going in the array of notes and events  
    array_validnotes = selected_notes(array_notesevents[0])[0]
    #PM(array_validnotes)
    array_tempnotes = [] #The temp array containing the objects

    #Get array of objects
    array_validobjects = note_objects(array_validnotes)
    j = 0
    for x in range(0, len(array_validobjects)):
        #We remove every 4th note
        j+=1
        if j < 4:
            array_tempnotes.append(array_validobjects[x])
        else:
            j = 0
    array_notes = add_objects(array_notes, array_tempnotes)
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)

def remove_notes_prokeys(what,level,instrument,how,selected):
    #PM("\n\n"+what+" - "+level+" - "+instrument+" - "+str(how)+" - "+str(same)+" - "+str(sparse)+" - "+str(bend)+" - "+str(selected)+"\n\n")
    #w/h/q/e, whole, half, quarter, eighth grid
    #x/h/m/e, expert, hard, medium, easy
    #"PART DRUMS"/etc. (leave "" to apply to currently selected track
    #0-30, ticks tolerance
    #0/1, not keep or keep same consecutive notes even if they are 1 grid level faster than 'what'
    #0/1, detect pitch bends
    global maxlen
    global divisions_array
    global sustains_array
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]
    base_instrument = tracks_array['PART KEYS']
    #PM("\n\ninstrument: "+str(instrument))
    array_instrument_data = process_instrument(instrument)
    base_array_instrument_data = process_instrument(base_instrument)
    array_instrument_notes = array_instrument_data[1]
    array_base_instrument_notes = base_array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    base_array_notesevents = create_notes_array(array_base_instrument_notes)
    division = int(math.floor((correct_tqn*4)*divisions_array[what]))
    array_notes = [] #The final array going in the array of notes and events
    array_tempnotes = [] #The temp array containing the objects
    instrumentname = ''
    position = 0
    sparse_position = 0
    old_note = []
    base_level = "notes_"+level
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    if "REAL_KEYS" in instrumentname or "KEYS_ANIM" in instrumentname:
        level = "notes"
    else:
        level = "notes_"+level

    
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    base_notes_dict = notesname_array[notesname_instruments_array['PART KEYS']]
    array_validnotes = []
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
        if first_measure == last_measure:
            result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
            return
    #PM("lunghezza: ")
    #PM(len(array_notesevents[0]))
    #PM("first_measure: "+str(first_measure)+" - last_measure: "+str(last_measure)+"\n")
    #We filter out all OD, BRE, markers, etc.
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrumentname)
            return
        this_measure = mbt(int(note[1]))[0]
        if notes_dict[note[2]][1] == level and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_validnotes.append(note)
        else:
            array_notes.append(note)
    array_validpositions = []

    # If the array is not empty prompt to overwrite
    result = 6 # yes
    if len(array_validnotes) > 0:
        result = RPR_MB("Existing notes found in difficulty %s. Overwrite?" % instrumentname, "Reduce Pro Keys", 3)

    # Copy the next highest pro keys difficulty into the current one as a base.
    if result == 6:
        array_validnotes = []
        level_array_tmp = ['x', 'h', 'm', 'e']
        curr_level = instrumentname[-1].lower()
        curr_level_i = level_array_tmp.index(curr_level)
        upper_level = level_array_tmp[curr_level_i-1]

        upper_instrument_name = "PART REAL_KEYS_"+upper_level.upper()
        upper_instrument_data = process_instrument(tracks_array[upper_instrument_name])
        upper_instrument_notes = upper_instrument_data[1]
        upper_notesevents = create_notes_array(upper_instrument_notes)
        
        for x in range(0,len(upper_notesevents[0])):
            note = upper_notesevents[0][x]
            if note[2] not in notes_dict:
                invalid_note_mb(note, upper_instrument_name)
                return
            this_measure = mbt(int(note[1]))[0]
            if notes_dict[note[2]][1] == "notes" and (selected == 0 or (this_measure >= first_measure and this_measure <= last_measure)):
                array_validnotes.append(note)
            else:
                array_notes.append(note)

    for x in range(0,len(base_array_notesevents[0])):
        note = base_array_notesevents[0][x]
        this_measure = mbt(int(note[1]))[0]
        if base_notes_dict[note[2]][1] == base_level and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            valid_position = str(mbt(int(note[1]))[0])+"."+str(mbt(int(note[1]))[1])+"."+str(mbt(int(note[1]))[2])
            array_validpositions.append(valid_position) 
    #PM("array_validpositions: ")
    #PM(array_validpositions)
    
    array_rolls = []
    #Loop through all notes to find all markers, 126 or 127
    #For each marker found, add to markers_array location and location-length
    for x in range(0,len(array_notes)):
        note = array_notes[x]
        #PM(note)
        this_measure = mbt(int(note[1]))[0]

        if note[2] == 126 and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_rolls.append([note[1], note[1]+note[4]])
        elif note[2] == 127 and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_rolls.append([note[1], note[1]+note[4]])
            
    array_rollnotes = []
    for x in range(0,len(array_validnotes)):
        note = array_validnotes[x]
        for j in range(0, len(array_rolls)):
            start = array_rolls[j][0]
            end = array_rolls[j][1]
            if note[1] >= start and note[1] <= end:
                if note[1] not in array_rollnotes:
                    array_rollnotes.append(note[1])
            
    #We pass the valid notes array through a function that returns an object array with one element per note/chord
    array_validobjects = note_objects(array_validnotes)
    
    #We go through the notes to remove the unneeded notes
    for x in range(0,len(array_validobjects)):
        note = array_validobjects[x]
        old_position = position
        position = str(mbt(note[1][0])[0])+"."+str(mbt(note[1][0])[1])+"."+str(mbt(note[1][0])[2])
        #PM("position:")
        #PM(position)
        #PM("\n")
        if position in array_validpositions:
            array_tempnotes.append(note)

    #Now let's create array_notes using array_tempnotes
    array_notes = add_objects(array_notes, array_tempnotes)
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)

    
def remove_notes(what,level,instrument,how,same,sparse,bend,selected):
    #PM("\n\n"+what+" - "+level+" - "+instrument+" - "+str(how)+" - "+str(same)+" - "+str(sparse)+" - "+str(bend)+" - "+str(selected)+"\n\n")
    #w/h/q/e, whole, half, quarter, eighth grid
    #x/h/m/e, expert, hard, medium, easy
    #"PART DRUMS"/etc. (leave "" to apply to currently selected track
    #0-30, ticks tolerance
    #0/1, not keep or keep same consecutive notes even if they are 1 grid level faster than 'what'
    #0/1, detect pitch bends
    global maxlen
    global divisions_array
    global sustains_array
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]
    #PM("\n\ninstrument: "+str(instrument))
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    division = int(math.floor((correct_tqn*4)*divisions_array[what]))
    array_notes = [] #The final array going in the array of notes and events
    array_tempnotes = [] #The temp array containing the objects
    instrumentname = ''
    position = 0
    sparse_position = 0
    old_note = []
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    if "REAL_KEYS" in instrumentname or "KEYS_ANIM" in instrumentname:
        level = "notes"
    else:
        level = "notes_"+level
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    array_validnotes = []
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
        if first_measure == last_measure:
            result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
            return
    #PM("lunghezza: ")
    #PM(len(array_notesevents[0]))
    #PM("first_measure: "+str(first_measure)+" - last_measure: "+str(last_measure)+"\n")
    #We filter out all OD, BRE, markers, etc.
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        this_measure = mbt(int(note[1]))[0]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrumentname)
            return
        if notes_dict[note[2]][1] == level and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_validnotes.append(note)
        else:
            array_notes.append(note)
            
    array_rolls = []
    #Loop through all notes to find all markers, 126 or 127
    #For each marker found, add to markers_array location and location-length
    for x in range(0,len(array_notes)):
        note = array_notes[x]
        #PM(note)
        this_measure = mbt(int(note[1]))[0]

        if note[2] == 126 and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_rolls.append([note[1], note[1]+note[4]])
        elif note[2] == 127 and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_rolls.append([note[1], note[1]+note[4]])
            
    array_rollnotes = []
    for x in range(0,len(array_validnotes)):
        note = array_validnotes[x]
        for j in range(0, len(array_rolls)):
            start = array_rolls[j][0]
            end = array_rolls[j][1]
            if note[1] >= start and note[1] <= end:
                if note[1] not in array_rollnotes:
                    array_rollnotes.append(note[1])
            
    #We pass the valid notes array through a function that returns an object array with one element per note/chord
    array_validobjects = note_objects(array_validnotes)
    #First off, if the pitch bend option is on, we fix those
    skip_bend = 0
    if bend == 1 and "DRUMS" not in instrumentname: #WARNING: keys uneven chords are not yet worked in
        array_validobjects2 = list(array_validobjects)
        array_validobjects = []
        distance = (correct_tqn/4)+how #Pitch bend interval is 1/16th+tolerance
        for x in range(0,len(array_validobjects2)):
            if skip_bend == 0:
                #We need to exclude uneven keys chords
                uneven = 0
                if x < len(array_validobjects2)-1:
                    chord = array_validobjects2[x+1][6]
                    chord_length = chord[0]
                
                    for k in range(0,len(chord)):
                        old_chord_length = chord_length
                        chord_length = chord[k]
                        if chord_length != old_chord_length:
                            uneven = 1
                            break
                if x < len(array_validobjects2)-1 and uneven == 0: #If it's the last note, it can't be a bend; no uneven chords on keys can have bends
                    #A pitch bend happens when:
                    #Two objects are separated by less than distance
                    #Two objects are different
                    #The first object has no preceding object closer than (correct_tqn/2)-how
                    # AND
                    #The second object is equal or longer than sustains length
                    # OR
                    #The second object is (correct_tqn/2)-how from the next object                
                    position = array_validobjects2[x+1][1][0]
                    measure = mbt(position)[0]
                    bpm = measures_array[measure-1][5]
                   
                    for key in sorted(sustains_array.iterkeys()):
                        if key > bpm:
                            sustain_length = sustains_array[key]
                            break
                    difference = array_validobjects2[x+1][1][0]-array_validobjects2[x][1][0]
                    different_note = 0
                    if array_validobjects2[x+1][6] != array_validobjects2[x][6]:
                        different_note = 1
                    else:
                        different_note = 0
                    preceding_distance = (correct_tqn/2)-how
                    #preceding_difference = array_validobjects2[x][1][0]-array_validobjects2[x-1][1][0]
                    sustain = array_validobjects2[x+1][4][0]
                    if difference <= distance \
                        and different_note == 1 \
                        and (x == 0 or (x > 0 and array_validobjects2[x][1][0]-array_validobjects2[x-1][1][0] >= preceding_distance)) \
                        and (sustain >= sustain_length or x == (len(array_validobjects2)-2) or (array_validobjects2[x+2][1][0]-array_validobjects2[x+1][1][0])>=((correct_tqn/2)-how)):
                        #Pitch bend
                        new_length = (array_validobjects2[x+1][1][0]-array_validobjects2[x][1][0])+array_validobjects2[x+1][4][0]
                        new_position = array_validobjects2[x][1][0]
                        array_validobjects.append([array_validobjects2[x+1][0], [new_position], array_validobjects2[x+1][2], array_validobjects2[x+1][3], [new_length], array_validobjects2[x+1][5], array_validobjects2[x+1][6]])
                        skip_bend = 1
                    else:
                        array_validobjects.append(array_validobjects2[x])
                else:
                    array_validobjects.append(array_validobjects2[x])
            else:
                skip_bend = 0

    #Then we go through the notes to remove the unneeded notes
    for x in range(0,len(array_validobjects)):
        note = array_validobjects[x]
        old_position = position
        position = mbt(note[1][0])[3]

        #PM(str(position)+",")
        grid_check = int(math.floor(position/division))
        #PM(str(position)+" - "+str(grid_check)+" - "+str(division)+" - "+str(how)+"\n")
        if note[1][0] in array_rollnotes:
            array_tempnotes.append(note)
            old_note = note[6]
            sparse_position = note[1][0]
        elif position-(grid_check*division) <= how or (division - (position-(grid_check*division))) <= how : #Note(s) to keep
            #for j in range(0,len(note[6])):
            array_tempnotes.append(note)
            old_note = note[6]
            sparse_position = note[1][0]
        elif sparse and ((note[1][0]-sparse_position) >= division): #Distant note
            #for j in range(0,len(note[6])):
            array_tempnotes.append(note)
            old_note = []
            sparse_position = note[1][0]                
        elif same:
            newdivision = int(math.floor((correct_tqn*4)*divisions_array[nextdivisions_array[what]]))
            grid_check = int(math.floor(position/newdivision))
            if position-(grid_check*newdivision) <= how or (division - (position-(grid_check*newdivision))) <= how:
                if x > 0 and note[6] == array_validobjects[x-1][6]: #Same note, leave it
                    array_tempnotes.append(note)  
                    sparse_position = note[1][0]
    #Now if same or sparse is selected, we go through the array to fix redundant notes
    position = 0
    if same == 1 or sparse == 1:
        array_tempnotes2 = list(array_tempnotes)
        array_tempnotes = []
        for x in range(0,len(array_tempnotes2)):
            note = array_tempnotes2[x]
            old_position = position
            position = note[1][0]
            grid_check = int(math.floor(position/division))
            if (position-(grid_check*division) > how and x < (len(array_tempnotes2)-1)) and position not in array_rollnotes: #This object is not on grid, let's see if it can stay...
                next_position = array_tempnotes2[x+1][1][0]
                if next_position-position >= division or (next_position-position >= division*0.5 and same and array_tempnotes2[x+1][6] == note[6]):
                    array_tempnotes.append(note)
            else:
                array_tempnotes.append(note)
    #Now let's create array_notes using array_tempnotes
    array_notes = add_objects(array_notes, array_tempnotes)
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)

def create_animation_markers(instrument, expression, pause, mute):
    global maxlen
    global default_pause
    
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]
        
    if expression != '': 
        if "[" in expression: #Let's catch shenanigans
            play_event = expression
        else:
            play_event = "["+expression+"]"
    else:
        play_event = '[play]'
    if pause == 0:
        pause = default_pause

    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    if "REAL_KEYS" in instrumentname or "KEYS_ANIM" in instrumentname or "VOCALS" in instrumentname:
        level = "notes"
    else:
        level = "notes_x"
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
        
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = []
    array_events = array_notesevents[1]

    for x in range(0, len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] in notes_dict and notes_dict[note[2]][1] == level:
            array_notes.append(note)

    if len(array_notes) > 0:
        #First we check to see if there's a play and an idle_realtime marker.
        play_check = 0
        idle_check = 0
        for x in range(0, len(array_events)):
            if array_events[x][3] == '[play]' or array_events[x][3] == '[mellow]' or array_events[x][3] == '[intense]':
                play_check = 1
            elif array_events[x][3] == "[idle_realtime]":
                idle_check = 1
        result = 1
        #If we find both, we ask the user whether to abort or proceed
        if play_check == 1 and idle_check == 1 and mute == 0:
            result = RPR_MB( "At least one play/mellow/intense and one [idle_realtime] markers are already on the track. Are you sure you want to remove those and create them from scratch?", "Markers found", 1 )
        array_temp = []
        if result == 1:
            #We loop through text events and remove all play, idle and idle_realtime event, according to expression
            for x in range(0, len(array_events)):
                event = array_events[x]
                if event[3] != "[play]" and event[3] != "[intense]" and event[3] != "[mellow]" and event[3] != "[idle]" and event[3] != "[idle_realtime]":
                    array_temp.append(event)
            #Let's check the first valid expert note
            first_note = mbt(array_notes[0][1])
            array_temp.append(['<X', measures_array[first_note[0]-1][1], '0', play_event, '>', 'ff01'])
            if first_note[0] > 3: #If it happens inside M3, we put a [play] event at M3.1. If not, we put an [idle] event
                array_temp.append(['<X', measures_array[2][1], '0', '[idle]', '>', 'ff01'])
            location =int(array_notes[0][1])+int(array_notes[0][4])
            lastmarker = 'p' #We set a variable to keep track of the last inserted event: p = play, i = idle. NOT USED ANYMORE

            for x in range(0, len(array_notes)): #We loop through the valid expert notes.
                note = array_notes[x]
                if note[0] == 'E' or note[0] == 'e':
                    #PM(note)
                    #PM("\n")
                    if note[2] in notes_dict and notes_dict[note[2]][1] == level:
                        distance = note[1]-location
                        #Every time there's a space equal or longer than pause between end of previous note and new note, we drop a new marker
                        if distance >= pause:
                            array_temp.append(['<X', location+correct_tqn, '0', '[idle]', '>', 'ff01'])
                            array_temp.append(['<X', note[1]-correct_tqn, '0', play_event, '>', 'ff01'])
                        location = note[1]+note[4] #Let's reset location right away
            #correct_tqn after the last valid expert note we drop the [idle_realtime] marker
            array_temp.append(['<X', location+correct_tqn, '0', '[idle_realtime]', '>', 'ff01'])
        else:
            PM("no go")
        #PM(array_temp)
        write_midi(instrument, [array_notesevents[0], array_temp], end_part, start_part)

def fix_sustains(instrument, level, fix, selected):
    #This function removes too short sustains. With fix = 1 it also shortens sustains based on instrument, difficulty and BPM.
    global maxlen
    global sustainspace_array
    global sustains_array
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]
    #PM("\n\ninstrument: "+instrument)
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = [] #The final array going in the array of notes and events
    array_tempnotes = [] #The temp array containing the objects
    instrumentname = ''
    old_note = []
    leveltext = level
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    if "REAL_KEYS" in instrumentname or "KEYS_ANIM" in instrumentname:
        leveltext = "notes"
    else:
        leveltext = "notes_"+leveltext
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    array_validnotes = []
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
    if selected and first_measure == last_measure:
        result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
        return
    #We filter out all OD, BRE, markers, etc.
        
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        #PM(note)
        this_measure = mbt(int(note[1]))[0]

        if note[2] in notes_dict and notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_validnotes.append(note)
        else:
            array_notes.append(note)

    #We pass the valid notes array through a function that returns an object array with one element per note/chord
    array_validobjects = note_objects(array_validnotes)
    for x in range(0,len(array_validobjects)):
        note = array_validobjects[x]
        measure = mbt(note[1][0])[0]
        bpm = int(measures_array[measure-1][5])
        if fix == 1 and x < len(array_validobjects)-1: #We fix too long sustains
            #If it's longer than 1/16th, do the check
            if note[4][0] > correct_tqn/4:
            
            #Get current position+length
                #We loop through all notes in the object to find the longest note
                #We use that as the end_position
                #We use a while statement to take an object which starting position is >= end_pos
                end_position = note[1][0]+note[4][0]
                distance = array_validobjects[x+1][1][0]-end_position
                #Let's get the sustain space based on BPM and difficulty

                for key in sorted(sustainspace_array.iterkeys()):
                    if bpm <= key:
                        sustain_space = sustainspace_array[key][level]
                        break
                if "REAL_KEYS" in instrumentname and sustain_space < correct_tqn*0.5 and (len(note[2]) > 1 or len(array_validobjects[x+1][2]) > 1 ):
                    sustain_space = correct_tqn*0.5
                #Check if next object's position is at least space. If not, shorten sustain so that there's space left
                
                
                if distance < sustain_space:
                    new_distance = (array_validobjects[x+1][1][0]-note[1][0])-sustain_space
                    if new_distance < correct_tqn*0.25:
                        new_distance = correct_tqn*0.25
                    for j in range(0, len(note[4])):
                        note[4][j] = new_distance
            
        #Once done, check if sustain is too long. In case, fix it
        for key in sorted(sustains_array.iterkeys()):
            if bpm <= key:
                sustain_length = sustains_array[key]
                break
        #PM(str(note[4][0])+" - "+str(sustain_length)+" - "+str(bpm)+"\n")
        if note[4][0] > (correct_tqn*0.25)+20 and note[4][0]+20 < sustain_length: #20 ticks tolerance for good measure, it's roughly 2 1/128th
            for j in range(0, len(note[4])):
                note[4][j] = correct_tqn*0.25
    array_notes = add_objects(array_notes, array_validobjects)
    
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)

def single_snare(instrument,level, what, selected):
    #This functions removes kick notes when coupled with another notes
    #instrument: PART DRUMS or PART DRUMS 2x
    #what: 'a' remove any note coupled with snare; 't' remove any tom; 'k' remove any kick; 'c' remove any cymbal
    PM(str(instrument)+" - "+str(level)+" - "+str(what)+" - "+str(selected))
    global maxlen
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)

    array_notes = [] #The final array going in the array of notes and events
    array_tempnotes = [] #The temp array containing the objects
    instrumentname = ''
    old_note = []
    leveltext = level
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes_"+leveltext
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    for key in notes_dict:
        if notes_dict[key][1] == leveltext:
            if "Kick" in notes_dict[key][0]:
                kick = key
            elif "Red" in notes_dict[key][0]:
                snare = key
            elif "Yellow" in notes_dict[key][0]:
                notey = key
            elif "Blue" in notes_dict[key][0]:
                noteb = key
            elif "Green" in notes_dict[key][0]:
                noteg = key
            
    array_validnotes = []
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
        if first_measure == last_measure:
            result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
            return
    #We filter out all OD, BRE, markers, etc.
    array_temp = []
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        #PM(note)
        this_measure = mbt(int(note[1]))[0]

        if note[2] in notes_dict and (notes_dict[note[2]][1] == leveltext or (note[2] >= 110 and note[2] <= 112)) and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_validnotes.append(note)
        else:
            array_notes.append(note)
            
    array_validobjects = note_objects(array_validnotes)
    for x in range(0, len(array_validobjects)):
        note = array_validobjects[x]
        if snare in note[6] and len(note[6]) > 1: #There's a kick with other notes, let's check if it needs removing
            if what == 'a' or \
               (what == 'k' and kick in note[6]) or \
               (what == 't' and (110 in note[6] or 111 in note[6] or 112 in note[6])) or \
               (what == 'c' and (notey in note[6] or noteb in note[6] or noteg in note[6])):
                sub_array = [[], [], [], [], [], [], []]
                for j in range (0, len(note[6])):
                    if note[2][j] == snare or (note[2][j] >= 110 and note[2][j] <= 112):
                        for h in range(0, 7):
                            sub_array[h].append(note[h][j])
                array_temp.append(sub_array)
            else:
                array_temp.append(note)
        else: #Add the note
            array_temp.append(note)
    array_notes = add_objects(array_notes, array_temp)
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)

def remove_kick(instrument,level, what, selected):
    #This functions removes kick notes when coupled with another notes
    #instrument: PART DRUMS or PART DRUMS 2x
    #what: 'a' remove kick when coupled with any other note; 't' when coupled with any tom; 's' when coupled with snare; 'p' when coupled with snare or tom
    global maxlen
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)

    array_notes = [] #The final array going in the array of notes and events
    array_tempnotes = [] #The temp array containing the objects
    instrumentname = ''
    old_note = []
    leveltext = level
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes_"+leveltext
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    for key in notes_dict:
        if notes_dict[key][1] == leveltext:
            if "Kick" in notes_dict[key][0]:
                kick = key
            elif "Red" in notes_dict[key][0]:
                snare = key
            elif "Yellow" in notes_dict[key][0]:
                notey = key
            elif "Blue" in notes_dict[key][0]:
                noteb = key
            elif "Green" in notes_dict[key][0]:
                noteg = key
            
    array_validnotes = []
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
        if first_measure == last_measure:
            result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
            return
    #We filter out all OD, BRE, markers, etc.
    array_temp = []
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        #PM(note)
        this_measure = mbt(int(note[1]))[0]

        if note[2] in notes_dict and (notes_dict[note[2]][1] == leveltext or (note[2] >= 110 and note[2] <= 112)) and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_validnotes.append(note)
        else:
            array_notes.append(note)
            
    array_validobjects = note_objects(array_validnotes)
    for x in range(0, len(array_validobjects)):
        note = array_validobjects[x]
        if kick in note[6] and len(note[6]) > 1: #There's a kick with other notes, let's check if it needs removing
            if what == 'a' or \
               (what == 's' and snare in note[6]) or \
               (what == 't' and (110 in note[6] or 111 in note[6] or 112 in note[6])) or \
               (what == 'p' and (snare in note[6] or 110 in note[6] or 111 in note[6] or 112 in note[6])):
                sub_array = [[], [], [], [], [], [], []]
                for j in range (0, len(note[6])):
                    if note[2][j] != kick:
                        for h in range(0, 7):
                            sub_array[h].append(note[h][j])
                array_temp.append(sub_array)
            else:
                array_temp.append(note)
        else: #Add the note
            array_temp.append(note)
    array_notes = add_objects(array_notes, array_temp)
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)

def single_pedal(level, how, selected):
    global maxlen
    global double_pedal_bpm
    instrument = tracks_array['PART DRUMS']
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)

    array_notes = [] #The final array going in the array of notes and events
    instrumentname = ''
    leveltext = level
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes_"+leveltext
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    for key in notes_dict:
        if notes_dict[key][1] == leveltext:
            if "Kick" in notes_dict[key][0]:
                kick = key
            
    
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
        if first_measure == last_measure:
            result = RPR_MB( "This command works from measure to measure, please select notes from at least 2 different measures", "Invalid selection", 0)
            return
    #We filter out all OD, BRE, markers, etc.
    array_validnotes = []
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        #PM(note)
        this_measure = mbt(int(note[1]))[0]

        if note[2] == kick and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_validnotes.append(note)
        else:
            array_notes.append(note)
    
    #Loop through kick notes and everytime you find one set start to its location
    old_note = 0
    start = 0
    end = 0
    count = 0
    doublekick_array = []
    triplet = 0
    for x in range(0, len(array_validnotes)):
        note = array_validnotes[x]
        measure = mbt(note[1])[0]
        bpm = int(measures_array[measure-1][5])
        grid = 0.5
        if bpm < double_pedal_bpm:
            grid = 0.25
        if x < len(array_validnotes)-1:
            nextnote = array_validnotes[x+1]
            
            if nextnote[1]-note[1] <= ((correct_tqn/3)*grid) and (triplet == 0 or triplet == 4) or \
               nextnote[1]-note[1] <= ((correct_tqn*0.5)*grid) and (triplet == 0 or triplet == 3) or \
               nextnote[1]-note[1] <= ((correct_tqn/1.5)*grid) and (triplet == 0 or triplet == 2) or \
               nextnote[1]-note[1] <= ((correct_tqn)*grid) and (triplet == 0 or triplet == 1):
                if nextnote[1]-note[1] <= ((correct_tqn/3)*grid):
                    triplet = 4
                elif nextnote[1]-note[1] <= ((correct_tqn*0.5)*grid):
                    triplet = 3
                elif nextnote[1]-note[1] <= ((correct_tqn/1.5)*grid):
                    triplet = 2
                else:
                    triplet = 1

                #If the next note is less than 1/8th (give or take 20 ticks) from the previous note, \
                #   advance a count var by 1 and don't change start (but keep track of note location)
                if start == 0:
                    start = note[1]
                else:
                    count +=1
                #If the count var reaches 4, for every new note set an end var with its location

                if count > 1:
                    end = nextnote[1]
            else:
                #Every time a note is 1/8th or more, reset the start var, unless the end var is filled
                if end:
                    #When the next note is 1/8th or more, add start and end as an array to a doublekick_array and reset start and end
                    doublekick_array.append([start, end, triplet]) 
                start = 0
                end = 0
                count = 0
                triplet = 0
    if start and end:
        doublekick_array.append([start, end, triplet])

    if len(doublekick_array)==0:
        result = RPR_MB( "No double kicks found, skipping process", "Warning", 0)
        return
    
    #Once finished, go through the doublekick_array and process every double kick section
    array_notestoremove = []

    for x in range(0, len(doublekick_array)):
        start = doublekick_array[x][0]
        end = doublekick_array[x][1]
        triplet = doublekick_array[x][2]
        note_count_array = count_notes(array_validnotes, start, end, [96], 0, instrument)
        note_count = list(note_count_array[0])
        number_of_notes = int(note_count[1])
        count = 0
        for j in range(0, len(array_validnotes)):
            note = array_validnotes[j]
            if note[1] >= start and note[1] <= end:
                if triplet == 2 or triplet == 4:
                    count+=1
                    if count % 2 == 0:
                        array_notestoremove.append(note[1])
                elif number_of_notes == 4:
                    count+=1
                    if count == 4:
                       array_notestoremove.append(note[1])     
                else:
                    position = mbt(note[1])[3]
                    measure = mbt(note[1])[0]
                    #PM("\n")
                    #PM(str(position) + " : " + str(measure))
                    #PM("\n")
                    bpm = int(measures_array[measure-1][5])
                    grid = 'e'
                    if bpm < double_pedal_bpm:
                        grid = 's'
                    division = int(math.floor((correct_tqn*4)*divisions_array[grid]))
                    grid_check = int(math.floor(position/division))
                    #PM(str(bpm)+ " | " )
                    #PM(str(position-(grid_check*division)))
                    #PM(" - ")
                    if position-(grid_check*division) > how:
                        array_notestoremove.append(note[1])
    for x in range(0, len(array_validnotes)):
        note = array_validnotes[x]
        if note[1] not in array_notestoremove:
            array_notes.append(note)
    #Use the remove_notes criteria and keep only notes on a 1/8th grid for those sections
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)
    
def flip_discobeat(instrument, level, selected, mute):
    global maxlen
    flipmarker = ''
    #This section originally set different mix for different levels.
    #However, since the function works on Expert level notes anyway all levels now point to the same marker
    if level == 'x':
        flipmarker = 'mix 3 drums'
    elif level == 'h':
        flipmarker = 'mix 3 drums'
    elif level == 'm':
        flipmarker = 'mix 3 drums'
    elif level == 'e':
        flipmarker = 'mix 3 drums'
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)

    array_notes = [] #The final array going in the array of notes and events
    instrumentname = ''
    leveltext = level
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes_"+leveltext
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    for key in notes_dict:
        if notes_dict[key][1] == leveltext:
            if "Red" in notes_dict[key][0]:
                snare = key
            elif "Yellow" in notes_dict[key][0]:
                notey = key
                
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
        if first_measure == last_measure:
            result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)

    array_validnotes = []
    for x in range(0,len(array_notesevents[1])):
        note = array_notesevents[1][x]
        #PM(note)
        this_measure = mbt(int(note[1]))[0]
        if selected == 0 or (selected and (this_measure >= first_measure-1 and this_measure <= last_measure)):
            array_validnotes.append(note)
            
    #Look through markers and create an array of ticks for all disco sections using 0d and 0.
    discoflip_array = []
    start = 0
    end = 0
    for x in range(0, len(array_validnotes)):
        event = array_validnotes[x]
        if event[3] == "["+flipmarker+"0d]" or \
           event[3] == "["+flipmarker+"1d]" or \
           event[3] == "["+flipmarker+"2d]" or \
           event[3] == "["+flipmarker+"3d]" or \
           event[3] == "["+flipmarker+"4d]":
            if start:
                result = RPR_MB( "Two consecutive disc flip markers found, please fix your chart", "Invalid markers", 0)
                return
            else:
                start = event[1]
        elif event[3] == "["+flipmarker+"0]" or \
           event[3] == "["+flipmarker+"1]" or \
           event[3] == "["+flipmarker+"2]" or \
           event[3] == "["+flipmarker+"3]" or \
           event[3] == "["+flipmarker+"4]":
            if start:
                end = event[1]
                discoflip_array.append([start, end])
                start = 0
                end = 0
    if start:
        end = array_notesevents[0][-1][1]
        discoflip_array.append([start, end])

    for x in range(0, len(discoflip_array)):
        start = discoflip_array[x][0]
        end = discoflip_array[x][1]
        noteycount = 0
        snarecount = 0
        #Count hi hat and snare notes: if snare notes > hi hat notes means the section is already flipped: prompt user
        for j in range(0, len(array_notesevents[0])):
            note = array_notesevents[0][j]
            if note[1] >= start and note[1] <= end:
                if note[2] == notey:
                    noteycount+=1
                elif note[2] == snare:
                    snarecount+=1
        if snarecount > noteycount:
            start_m = str(mbt(start)[0])
            end_m = str(mbt(end)[0])
            if mute == 0:
                result = RPR_MB( "The disco flip section from M"+start_m+" to M"+end_m+" looks already flipped: proceed anyway?", "Disco flip detected", 1 )
        if snarecount <= noteycount or result == 1:
            #Go through the disco array and every snare note in there is transformed in hi hat and viceversa.
            for j in range(0, len(array_notesevents[0])):
                note = array_notesevents[0][j]
                if note[1] >= start and note[1] <= end and note[2] == notey:
                    note[2] = snare
                elif note[1] >= start and note[1] <= end and note[2] == snare:
                    note[2] = notey
    write_midi(instrument, [array_notesevents[0], array_notesevents[1]], end_part, start_part)

def unflip_discobeat(instrument, level, how, selected):
    global maxlen
    division = int(math.floor((correct_tqn*4)*divisions_array['e']))
    #This section originally set different mix for different levels.
    #However, since the function works on Expert level notes anyway all levels now point to the same marker
    flipmarker = 'mix 3 drums'
    new_flipmarker = ''
    if level == 'x':
        new_flipmarker = 'mix 3 drums'
    elif level == 'h':
        new_flipmarker = 'mix 2 drums'
    elif level == 'm':
        new_flipmarker = 'mix 1 drums'
    elif level == 'e':
        new_flipmarker = 'mix 0 drums'
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)

    array_notes = [] #The final array going in the array of notes and events
    instrumentname = ''
    leveltext = level
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes_"+leveltext
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    for key in notes_dict:
        if notes_dict[key][1] == leveltext:
            if "Red" in notes_dict[key][0]:
                snare = key
            elif "Yellow" in notes_dict[key][0]:
                notey = key
                
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
        if first_measure == last_measure:
            result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)

    array_validnotes = []
    for x in range(0,len(array_notesevents[1])):
        note = array_notesevents[1][x]
        #PM(note)
        this_measure = mbt(int(note[1]))[0]
    
        if selected == 0 or (selected and (this_measure >= first_measure-1 and this_measure <= last_measure)):
            array_validnotes.append(note)
            
    #Look through markers and create an array of ticks for all disco sections using 0d and 0.
    discoflip_array = []
    start = 0
    end = 0
    for x in range(0, len(array_validnotes)):
        event = array_validnotes[x]
        if event[3] == "["+flipmarker+"0d]" or \
           event[3] == "["+flipmarker+"1d]" or \
           event[3] == "["+flipmarker+"2d]" or \
           event[3] == "["+flipmarker+"3d]" or \
           event[3] == "["+flipmarker+"4d]":
            #event[3] = event[3].replace("d]", "]")
            if start:
                result = RPR_MB( "Two consecutive disc flip markers found, please fix your chart", "Invalid markers", 0)
                return
            else:
                start = event[1]
        elif event[3] == "["+flipmarker+"0]" or \
           event[3] == "["+flipmarker+"1]" or \
           event[3] == "["+flipmarker+"2]" or \
           event[3] == "["+flipmarker+"3]" or \
           event[3] == "["+flipmarker+"4]":
            if start:
                end = event[1]
                discoflip_array.append([start, end])
                start = 0
                end = 0
    if start:
        end = array_notesevents[0][-1][1]
        discoflip_array.append([start, end])
    array_notestoremove = []
    array_add = []

    for x in range(0, len(discoflip_array)):
        start = discoflip_array[x][0]
        end = discoflip_array[x][1]
        noteycount = 0
        snarecount = 0
        #Count hi hat and snare notes: if snare notes > hi hat notes means the section is already flipped: prompt user
        for j in range(0, len(array_notesevents[0])):
            note = array_notesevents[0][j]
            if note[1] >= start and note[1] <= end:
                if note[2] == notey:
                    noteycount+=1
                elif note[2] == snare:
                    snarecount+=1
        if noteycount > snarecount:
            start_m = str(mbt(start)[0])
            end_m = str(mbt(end)[0])
            if mute == 0:
                result = RPR_MB( "The disco flip section from M"+start_m+" to M"+end_m+" looks already unflipped: proceed anyway?", "Section unflipped", 1 )
        
        if noteycount <= snarecount or result == 1:
            #Go through the disco array and every snare note in there is transformed in hi hat and viceversa.
            for j in range(0, len(array_notesevents[0])):
                note = array_notesevents[0][j]
                #Go through the disco array and convert every hi hat to snare
                if note[1] >= start and note[1] <= end and note[2] == notey:
                    #For every snare on a 1/8th grid, check if there's a hi hat note 1/16th before or after: if so, drop a hi hat note on the same tick as the snare
                    note[2] = snare
                    position = mbt(note[1])[3]
                    grid_check = int(math.floor(position/division))
                    if position-(grid_check*division) <= how:
                        if j < len(array_notesevents[0])-1 and j > 0:
                            if array_notesevents[0][j-1][2] == snare or array_notesevents[0][j+1][2]:
                                new_note = list(note)
                                new_note[2] = notey
                                array_add.append(new_note)
                elif note[1] >= start and note[1] <= end and note[2] == snare:
                    #Use the remove_notes criteria and keep only hi hat notes on a 1/8th grid for those sections, converting them from snare first
                    note[2] = notey
                    position = mbt(note[1])[3]
                    grid_check = int(math.floor(position/division))
                    if position-(grid_check*division) > how:
                        array_notestoremove.append(note[1])
    if len(array_add) > 0:
        array_notesevents[0].extend(array_add)
        
    array_temp = []
    for x in range(0, len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if (note[2] == notey and note[1] not in array_notestoremove) or note[2] != notey:
            array_temp.append(note)
    #Remove disco flip markers
    for x in range(0, len(array_notesevents[1])):
        event = array_notesevents[1][x]
        if event[3] == '[mix '+array_drumkit[level]+' drums0d]':
            event[3] = '[mix '+array_drumkit[level]+' drums0]'
            
        elif event[3] == '[mix '+array_drumkit[level]+' drums1d]':
            event[3] = '[mix '+array_drumkit[level]+' drums1]'
        elif event[3] == '[mix '+array_drumkit[level]+' drums2d]':
            event[3] = '[mix '+array_drumkit[level]+' drums2]'
        elif event[3] == '[mix '+array_drumkit[level]+' drums3d]':
            event[3] = '[mix '+array_drumkit[level]+' drums3]'
        elif event[3] == '[mix '+array_drumkit[level]+' drums4d]':
            event[3] = '[mix '+array_drumkit[level]+' drums4]'
    
    write_midi(instrument, [array_temp, array_notesevents[1]], end_part, start_part)
    
    
def simplify_roll(instrument, level, selected):
    global maxlen
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)

    
    instrumentname = ''
    leveltext = level

    array_notes = [] #The final array going in the array of notes and events
    array_validnotes = []

    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    if "REAL_KEYS" in instrumentname or "KEYS_ANIM" in instrumentname:
        leveltext = "notes"
    else:
        leveltext = "notes_"+leveltext
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
    #if selected and first_measure == last_measure:
        #result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
        #return

    array_onenote = []
    array_twonotes = []
    #Loop through all notes to find all markers, 126 or 127
    #For each marker found, add to markers_array location and location-length
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        #PM(note)
        this_measure = mbt(int(note[1]))[0]

        if note[2] == 126 and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_onenote.append([note[1], note[1]+note[4]])
        elif note[2] == 127 and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_twonotes.append([note[1], note[1]+note[4]])

    array_notestoremove = []
    array_notestoadd = []
    #Now loop through markers_array
    sequence = (correct_tqn*4)*divisions_array[leveldvisions_array[level]]
    note_marker = 0
    note_marker1 = 0
    note_marker2 = 0
    for x in range(0, len(array_onenote)):

        note_template = []
        start = array_onenote[x][0]
        end = array_onenote[x][1]
        note_count_array = count_notes(array_notesevents[0], start, end, [leveltext], 1, instrument)
        if len(note_count_array) > 0:
            note_count = list(note_count_array[0])
            note_marker = int(note_count[0])
            for j in range(0, len(array_notesevents[0])):
                note = array_notesevents[0][j]
                if note[1] >= start and note[1] <= end and note[2] == note_marker:
                    if note_template == []:
                        note_template = list(note) #We are creating a template for the new notes we're gonna add later
                    array_notestoremove.append([note[2], note[1]])
            k = 0
            location = start
            #From start to end drop a 1/16th note every eigth, quarter, etc. depending on level to array_notestoadd
            while (location < end+20):
                note = list(note_template)
                note[1] = location
                note[4] = correct_tqn*0.125
                array_notestoadd.append(note)
                k=1
                location+=(k*sequence)

    #For 127, look for the 2 notes  and add all notes to array_notestoremove
    note_template = []
    for x in range(0, len(array_twonotes)):
        start = array_twonotes[x][0]
        end = array_twonotes[x][1]
        note_count_array = count_notes(array_notesevents[0], start, end, [leveltext], 1, instrument)
        if len(note_count_array) > 1:
            note_count = list(note_count_array[0])
            note_marker1 = int(note_count[0])
            note_count = list(note_count_array[1])
            note_marker2 = int(note_count[0])
            #PM(str(note_marker1) + " - " +str(note_marker2))
            for j in range(0, len(array_notesevents[0])):
                note = array_notesevents[0][j]
                #For 126, look for one of the 5 notes and once found add all notes to array_notestoremove
                if note[1] >= start and note[1] <= end and (note[2] == note_marker1 or note[2] == note_marker2):
                    if note_template == []:
                        note_template = list(note) #We are creating a template for the new notes we're gonna add later
                    array_notestoremove.append([note[2], note[1]])
                    
            #For h, add notes every eighth, alternated. For m and e, add every quarter to array_notestoadd
            k = 0
            location = start
            if level == 'h':
                sequence = (correct_tqn*4)*divisions_array['q']
            else:
                sequence = (correct_tqn*4)*divisions_array['h']
            #From start to end drop a 1/16th note every eigth, quarter, etc. depending on level to array_notestoadd
            while (location < end+20):
                note = list(note_template)
                note[1] = location
                note[2] = note_marker1
                note[4] = correct_tqn*0.25
                array_notestoadd.append(note)
                k=1
                location+=(k*sequence)
                
            k = 0
            location = start+(sequence*0.5)
            while (location < end+20):
                note = list(note_template)
                note[1] = location
                note[2] = note_marker2
                note[4] = correct_tqn*0.25
                array_notestoadd.append(note)
                k=1
                location+=(k*sequence)
                
    #Remove array_notestoremove from array_notes
    array_temp = []
    for x in range(0, len(array_notesevents[0])):
        note = array_notesevents[0][x]
        remove = 0
        for j in range(0, len(array_notestoremove)):
            toremove = array_notestoremove[j]
            if note[2] == toremove[0] and note[1] == toremove[1]:
                remove = 1
        if remove == 0:
            array_temp.append(note)
        #if (note[2] != note_marker and note[2] != note_marker1 and note[2] != note_marker2) or \
            #((note[2] == note_marker or note[2] == note_marker1 or note[2] == note_marker2) and note[1] not in array_notestoremove):
            
    
    #Add array_notestoadd to array_notes
    array_temp.extend(array_notestoadd)

    write_midi(instrument, [array_temp, array_notesevents[1]], end_part, start_part)

def drums_animations(instrument, crash, soft, flam, grid, cymbals, how, mute):

    #instrument (PART DRUMS)
    #crash: 0 for CRASH2 default crash, 1 for CRASH1 default crash
    #soft: 0 for HARD default snare/crash, 1 for SOFT default snare/crash
    #flam: 0 is default, set to 1 if you want snare + Yt to be transformed to snare LH + RH
    #grid: e for eight is default, set to s for sixteenth to indicate you the lowest subdivision grid is 1/32 instwed of 1/16
    #cymbals: the number of consecutive cymbals hits that trigger a two handed action

    
    global maxlen
    
    instrument_track = tracks_array[instrument]
    notes_dict = notesname_array[notesname_instruments_array[instrument]]
    
    division = int(math.floor((correct_tqn*4)*divisions_array[grid]))
    
    array_instrument_data = process_instrument(instrument_track)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = array_notesevents[0]
    array_events = array_notesevents[1]
    array_promarkers = {}
    notes_found = 0
    result = 0

    if mute == 0:
        for x in range(0, len(array_notes)):
            note = array_notes[x]
            if note[2] not in notes_dict:
                invalid_note_mb(note, "PART DRUMS")
                return

            if notes_dict[note[2]][1] == "animations":
                notes_found = 1
                result = RPR_MB( "Drums animations notes found. Do you want to delete them and proceed?", "Animations notes found", 1 )
                break

    if result == 1 or notes_found == 0 or mute == 1:
        array_temp = list(array_notes)
        array_notes = []
        for x in range(0, len(array_temp)):
            note = array_temp[x]
            if notes_dict[note[2]][1] != "animations":
                array_notes.append(note)
    else:
        return

    #Copy all notes from expert to the respective animation notes
    for x in range(0, len(array_notes)):
        note = array_notes[x]
        if note[2] >= 110 and note[2] <= 112:
            if note[1] in array_promarkers:
                array_promarkers[note[1]].append(note[2])
            else:
                array_promarkers[note[1]] = [note[2]]

    for x in range(0, len(array_notes)):
        note = array_notes[x]
        if notes_dict[note[2]][1] == "notes_x":
            #It's an expert note, let's add it as animation
            if note[1] in array_promarkers and (note[2]+12) in array_promarkers[note[1]]:
                pitch = promarkers[note[2]]
            else:
                pitch = note[2]
            new_note = list(note)
            if(pitch == 100 and crash): #CRASH1 option
                pitch = 104
            new_note[2] = drumsanimations_array[pitch][soft]
            array_notes.append(new_note)
            
    #Flip disco sections putting snare on the right hand
            
    #Look through markers and create an array of ticks for all disco sections using 0d and 0.
    flipmarker = 'mix 3 drums'
    discoflip_array = []
    start = 0
    end = 0
    for x in range(0, len(array_events)):
        event = array_events[x]
        if event[3] == "["+flipmarker+"0d]" or \
           event[3] == "["+flipmarker+"1d]" or \
           event[3] == "["+flipmarker+"2d]" or \
           event[3] == "["+flipmarker+"3d]" or \
           event[3] == "["+flipmarker+"4d]":
            if start:
                result = RPR_MB( "Two consecutive disc flip markers found, please fix your chart", "Invalid markers", 0)
                return
            else:
                start = event[1]
        elif event[3] == "["+flipmarker+"0]" or \
           event[3] == "["+flipmarker+"1]" or \
           event[3] == "["+flipmarker+"2]" or \
           event[3] == "["+flipmarker+"3]" or \
           event[3] == "["+flipmarker+"4]":
            if start:
                end = event[1]
                discoflip_array.append([start, end])
                start = 0
                end = 0
    if start:
        end = array_notesevents[0][-1][1]
        discoflip_array.append([start, end])
    
    for x in range(0, len(discoflip_array)):
        start = discoflip_array[x][0]
        end = discoflip_array[x][1]
        noteycount = 0
        snarecount = 0
        #Count hi hat and snare notes: if snare notes > hi hat notes means the section is already flipped: prompt user
        for j in range(0, len(array_notes)):
            note = array_notes[j]
            if note[1] >= start and note[1] <= end:
                if note[2] == 98:
                    noteycount+=1
                elif note[2] == 97:
                    snarecount+=1
        if snarecount < noteycount:
            start_m = str(mbt(start)[0])
            end_m = str(mbt(end)[0])
            if mute == 0:
                result = RPR_MB( "The disco flip section from M"+start_m+" to M"+end_m+" does not look flipped", "Warning: no disco flip", 0 )

        #Go through the disco array and every snare note in there is transformed in hi hat and viceversa.
        for j in range(0, len(array_notes)):
            note = array_notes[j]
            if note[1] >= start and note[1] <= end and note[2] == 31:
                note[2] = drumsanimations_array[97][soft]
            elif note[1] >= start and note[1] <= end and (note[2] == 26 or note[2] == 28):
                note[2] = 31
           
    #Look for consecutive 16th notes with no other non-kick notes associated. Alternate.
    array_validnotes = []
    array_animationnotes = []

    #First we isolate the animation notes
    for x in range(0, len(array_notes)):
        note = array_notes[x]
        if notes_dict[note[2]][1] == "animations":
            array_animationnotes.append(note)
        else:
            array_validnotes.append(note)
    
    array_validobjects = note_objects(array_animationnotes)
    fill = 0
    pitch = 0
    item = 0
    cym_bonus = 0
    for x in range(0, len(array_validobjects)):
        note = array_validobjects[x]
        curpos = note[1][0]
        if x < len(array_validobjects)-1:
            nextpos = array_validobjects[x+1][1][0]
            distance = nextpos-curpos
        else:
            nextpos = 1000
            distance = 1000

        if distance <= (correct_tqn*0.5)-10 and \
           ((len(note[6]) == 1 and note[6][0] != 24) or \
           (len(note[6]) == 2 and 24 in note[6])): #Proper fill
            #We need to check how many hi hat ride, or crash consecutive notes there are.
            proceed = 1
            if cym_bonus == 0 and (31 in note[6] or 36 in note[6] or 37 in note[6] or 38 in note[6] or 39 in note[6] or 42 in note[6]):
                proceed = 0
                j = 0
                cym_count = 0
                while j <= cymbals:
                    j +=1
                    if x+j < len(array_validobjects)-1:
                        cym_note = array_validobjects[x+j-1]
                        cym_curpos = cym_note[1][0]
                        cym_nextpos = array_validobjects[x+j][1][0]
                        cym_distance = cym_nextpos-cym_curpos
                        if cym_distance <= (correct_tqn*0.5)-10 and \
                           ((len(cym_note[6]) == 1 and cym_note[6][0] != 24) or \
                           (len(cym_note[6]) == 2 and 24 in cym_note[6])):
                            if 31 in note[6] or 36 in note[6] or 37 in note[6] or 38 in note[6] or 39 in note[6] or 42 in note[6]:
                                cym_count+=1
                if cym_count >= cymbals:
                    cym_bonus = cym_count
                else:
                    cym_bonus = 0
            if proceed == 1 or cym_bonus >0 or fill >= cymbals:
                if cym_bonus > 0:
                    cym_bonus -=1
                    
                #PM("fill! " + str(fill) +" \n")
                if note[2][0] == 24:
                    item = 1
                else:
                    item = 0
                pitch = note[2][item]
                if fill > 0: #The fill has already begun
                    if fill % 2 != 0 and pitch != 26 and pitch != 28:
                        newpitch = da_lh[pitch]
                        note[2][item] = newpitch
                    elif fill % 2 == 0 and (pitch == 26 or pitch == 28):
                        newpitch = da_lh[pitch]
                        note[2][item] = newpitch
   
                    #PM("newpitch " + str(newpitch) +" \n")
                    fill+=1
                else:
                    #We need to check whether the first note is on grid or not
                    position = mbt(note[1][0])[3]
                    grid_check = int(math.floor(position/division))
                    if position-(grid_check*division) <= how or (division - (position-(grid_check*division))) <= how : #Note(s) on grid
                        if pitch == 26 or pitch == 28:
                            newpitch = da_lh[pitch]
                            note[2][item] = newpitch
                        fill = 1
                    else:
                        if pitch != 26 and pitch != 28:
                            newpitch = da_lh[pitch]
                            note[2][item] = newpitch
                        fill = 2
            else:
                fill = 0
        elif fill > 0 and ((len(note[6]) == 1 and note[6][0] != 24) or (len(note[6]) == 2 and 24 in note[6])):
            if note[2][0] == 24:
                item = 1
            else:
                item = 0
            pitch = note[2][item]
            if fill % 2 != 0 and pitch != 26 and pitch != 28:
                newpitch = da_lh[pitch]
                note[2][item] = newpitch
            elif fill % 2 == 0 and (pitch == 26 or pitch == 28):
                newpitch = da_lh[pitch]
                note[2][item] = newpitch
            fill = 0
        elif (len(note[6]) == 2 and 24 not in note[6] and 26 not in note[6] and 28 not in note[6]) or (len(note[6]) > 2 and 26 not in note[6] and 28 not in note[6]):
            #Remap two handed hits, no snare involved
            chord_string = ''
            for j in range(0, len(note[6])):
                if note[6][j] != 24:
                    chord_string+=str(note[6][j])
            PM(str(mbt(note[1][0])[0])+":"+str(mbt(note[1][0])[1])+":"+str(mbt(note[1][0])[2])+"\n")
            twohits = twohit_drums[chord_string]
            firstpitch = int(chord_string[2:])
            secondpitch = int(chord_string[:2])
            for j in range(0, len(note[2])):
                curpitch = note[2][j]
                if firstpitch == curpitch:
                    note[2][j] = twohits[0]
                elif secondpitch == curpitch:
                    note[2][j] = twohits[1]
                    
        #Look for Yt and snare chords and make them flam (optional)
        elif flam and (47 in note[6] and (26 in note[6] or 28 in note[6])):
            for j in range(0, len(note[2])):
                curpitch = note[2][j]
                if curpitch == 47 and soft:
                    note[2][j] = da_lh[28]
                elif curpitch == 47:
                    note[2][j] = da_lh[26]
        else:
            fill = 0
            
    #Look for Bc that has Yc before that and Yc the next note or the next note after that                    
    array_notes = add_objects(array_validnotes, array_validobjects)
    write_midi(instrument_track, [array_notes, array_events], end_part, start_part)

def reduce_singlenotes(instrument, level, selected):
    #option is dependant on level:
    #Medium - 1 allows the use of BO chords
    #Hard
    global maxlen
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_events = array_notesevents[1]
    
    instrumentname = ''
    leveltext = level

    array_validnotes = [] #The final array going in the array of notes and events
    array_notes = []
    
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    if "REAL_KEYS" in instrumentname or "KEYS_ANIM" in instrumentname:
        leveltext = "notes"
    else:
        leveltext = "notes_"+leveltext
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
    #if selected and first_measure == last_measure:
        #result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
        #return
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrumentname)
            return
        this_measure = mbt(int(note[1]))[0]
        if notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_validnotes.append(note)
        else:
            array_notes.append(note)
            
    #We pass the valid notes array through a function that returns an object array with one element per note/chord
    array_validobjects = note_objects(array_validnotes)

    array_conversions = []
    array_chords = {}
    array_big_chords = {}

    if level == 'm':
        array_translation = medium_notes
    else:
        array_translation = easy_notes

    chord_count = 0
    for x in range(0, len(array_validobjects)):
        note = array_validobjects[x]
        chord = ""
        if len(note[6])==1:
            chord_count+=1
            chord = notes_dict[note[2][0]][2]
            if chord in array_chords:
                array_chords[chord]+=1
            else:
                array_chords[chord]=1
    unused = 0
    for chord_type, chordcount in array_chords.iteritems():
        if (chordcount*100)/chord_count <= chord_threshold*100 and chord_type != 'O':
            unused = 1

    if (level == 'm' and 'O' in array_chords and (array_chords['O']*100)/chord_count <= chord_threshold*100) or \
       (level == 'e' and 'O' in array_chords and 'B' in array_chords and (array_chords['O']*100)/chord_count <= chord_threshold*100 and (array_chords['B']*100)/chord_count <= chord_threshold*100):
        #Do nothing
        c3 = 0
    elif level == 'm' and 'O' in array_chords and (array_chords['O']*100)/chord_count > chord_threshold*100 and unused == 0 and len(array_chords) >= len(array_translation):
        array_conversions.append(['O', 'B'])
    elif len(array_chords) >= len(array_translation):
        #Remap
        array_conversions = remap_notes(array_chords, array_translation)
        array_valid_chords = array_conversions[1]
        array_conversions = array_conversions[0]
    elif level == 'e' and len(array_chords) == 1:
        for note_from, note_to in array_chords.iteritems():
            array_conversions.append([note_from, easy_singlenotes_array[note_from]])
    elif (level == 'm' and 'O' not in array_chords) or (level == 'e' and 'O' not in array_chords and 'B' not in array_chords):
        #Do nothing
        c3 = 0
    elif (level == 'm' and 'O' in array_chords) or (level == 'e' and ('O'  in array_chords or 'B'  in array_chords)):
        chord_pattern = []
        for note_from, note_to in array_chords.iteritems():
            chord_pattern.append(easy_chords_order[note_from])
        chord_pattern.sort()
        chord_text = ''
        for k in range(0, len(chord_pattern)):
            chord_text+=one_chords[chord_pattern[k]]
        conversion_array = { 'm' : { 'GRO' : ['G', 'R', 'B'], 'GYO' : ['G', 'Y', 'B'], 'GBO' : ['G', 'Y', 'B'], 'RYO' : ['R', 'Y', 'B'], \
                                     'RBO' : ['R', 'Y', 'B'], 'YBO' : ['R', 'Y', 'B'], 'YO' : ['Y', 'B'], 'BO' : ['Y', 'B'], 'O' : ['B'] } , \
                             'e' : { 'RB' : ['G', 'R'], 'YB' : ['G', 'Y'], 'YO' : ['R', 'Y'], 'BO' : ['R', 'Y'], 'B': ['R'], 'O' : ['Y'] } }
        array_conversions = remap_notes(array_chords, conversion_array[level][chord_text])
        array_valid_chords = array_conversions[1]
        array_conversions = array_conversions[0]
    else: #This situation should never happen but we remap as a catch-all
        #Remap
        array_conversions = remap_notes(array_chords, array_translation)
        array_valid_chords = array_conversions[1]
        array_conversions = array_conversions[0]
    #We need to convert the chord from letters to numbers
    array_conversions_final = {}

    for x in range(0, len(array_conversions)):
        
        chordfrom = array_conversions[x][0]
        chordto = array_conversions[x][1]
        for notenumber, notedata in notes_dict.iteritems():
            if notedata[1] == leveltext and notedata[2] == chordfrom:
                chordfrom = str(notenumber)
        array_conversions_final[chordfrom] = chordto

    for x in range(0, len(array_validobjects)):
        note = array_validobjects[x]
        chord = str(note[6][0])
        #PM(chord)
        #PM("\n")
        #If a chord is in array_conversions_final it means it needs translating 
        if len(note[6]) == 1 and chord in array_conversions_final:
            #We go through each chord note and see what it translates to
            #We take the letter from the translation
            note_letter = array_conversions_final[chord][0]
            #We get the number of the note
            for notenumber, notedata in notes_dict.iteritems():
                if notedata[1] == leveltext and notedata[2] == note_letter:
                    note_number = notenumber
            #We go through the notes in the chord and look for the position for the note
            note[2][0] = note_number

    array_notes = add_objects(array_notes, array_validobjects)
    write_midi(instrument, [array_notes, array_events], end_part, start_part)
        
def reduce_chords(instrument, level, option, selected):
    #option is dependant on level:
    #Medium - 1 allows the use of BO chords
    #Hard
    global maxlen
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_events = array_notesevents[1]
    
    instrumentname = ''
    leveltext = level

    array_validnotes = [] #The final array going in the array of notes and events
    array_notes = []
    
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    if "REAL_KEYS" in instrumentname or "KEYS_ANIM" in instrumentname:
        leveltext = "notes"
    else:
        leveltext = "notes_"+leveltext
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
    #if selected and first_measure == last_measure:
        #result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
        #return
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrumentname)
            return
        this_measure = mbt(int(note[1]))[0]
        if notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_validnotes.append(note)
        else:
            array_notes.append(note)
            
    #We pass the valid notes array through a function that returns an object array with one element per note/chord
    array_validobjects = note_objects(array_validnotes)

    array_conversions = []
    
    
    if level == 'h':
        array_objects = list(array_validobjects)
        array_validobjects = []
        array_chords = []
        array_translation = hard_chords
        if option: #The user has elected to keep orange notes
            array_translation = hard_chords_o
        for x in range(0, len(array_objects)):
            note = array_objects[x]
            if len(note[6])==3:
                chord = ', '.join(str(v) for v in note[6])
                newchord_array = array_translation[chord]
                new_chord = [[], [], [], [], [], [], []]
                for j in range(0, len(note)):
                    for k in range(0, len(newchord_array)):
                        new_chord[j].append(note[j][0])
                for j in range(0, len(newchord_array)):
                    new_chord[2][j] = newchord_array[j]
                    new_chord[6][j] = newchord_array[j]
                array_validobjects.append(new_chord)
            elif note[6] == [84, 88]:
                if note[2][0] == 88:
                    note[2][0] = 87
                else:
                    note[2][1] = 87
                array_validobjects.append(note)
            else:
                array_validobjects.append(note)


    elif level == 'm' or level == 'e':

        if level == 'm':
            array_translation = medium_chords
            if option: #The user has elected to keep orange notes
                array_translation = medium_chords_o
        else:
            array_translation = easy_chords
            if option: #The user has elected to keep orange notes
                array_translation = easy_chords_o
        
        
        array_chords = {}
        array_big_chords = {}
        chord_count = 0
        for x in range(0, len(array_validobjects)):
            note = array_validobjects[x]
            chord = ""
            if len(note[6])==2:
                for j in range(0, len(note[6])):
                    notebit = note[6][j]
                    chord+=notes_dict[notebit][2]
                chord_count+=1
                if chord == 'GB' or chord == 'RO':
                    if chord in array_big_chords:
                        array_big_chords[chord]+=1
                    else:
                        array_big_chords[chord]=1
                else:
                    if chord in array_chords:
                        array_chords[chord]+=1
                    else:
                        array_chords[chord]=1
                    
        
        #Now we count the notes. We need to see the number of occurrances of each chord
        #First we leave out any chord occurring less than n% of all chords
        #array_allchords = list(array_chords)
        #array_chords = []

        
        array_valid_chords = []
        if level == 'e':
            if len(array_chords) >= len(array_translation):
                
                array_conversions = remap_notes(array_chords, array_translation)
                array_valid_chords = array_conversions[1]
                array_conversions = array_conversions[0]

            for chord_from, note_to in easy_chords_translation.iteritems():
                if chord_from not in array_valid_chords and chord_from in array_chords:
                    pos = 0
                    if (array_chords[chord_from]*100)/chord_count <= chord_threshold*100:
                        pos = 1

                    array_conversions.append([chord_from, note_to[pos]])

        else:
            if len(array_chords) < len(array_translation):
                a=5
            elif len(array_chords) == len(array_translation):
                #Reshuffle
                array_conversions = remap_notes(array_chords, array_translation)
                array_valid_chords = array_conversions[1]
                array_conversions = array_conversions[0]
            else:

                array_conversions = remap_notes(array_chords, array_translation)
                array_valid_chords = array_conversions[1]
                array_conversions = array_conversions[0]

            if 'YO' not in array_valid_chords:
                array_conversions.append(['YO', 'YB'])
            if 'BO' not in array_valid_chords and option == 0:
                array_conversions.append(['BO', 'YB'])
            
            #We now convert octave chords
            for x in range(0, len(array_big_chords)):
                chord = list(array_big_chords.keys())[x]
                translated_chords = octave_chords[chord]
                
                if translated_chords[0] not in array_chords or array_chords[translated_chords[0]] <= (chord_count*chord_threshold):
                    array_conversions.append([chord, translated_chords[0]])
                elif translated_chords[1] not in array_chords or array_chords[translated_chords[1]] <= (chord_count*chord_threshold):
                    array_conversions.append([chord, translated_chords[1]])
                else:
                    array_conversions.append([chord, translated_chords[2]])

        #We need to convert the chord from letters to numbers
        array_conversions_final = {}

        for x in range(0, len(array_conversions)):
            
            chordfrom = array_conversions[x][0]
            chordto = array_conversions[x][1]
            chordfrom = list(chordfrom)
            chordto = list(str(chordto))
            for j in range(0, len(chordfrom)):
                note = chordfrom[j]
                for notenumber, notedata in notes_dict.iteritems():
                    if notedata[1] == leveltext and notedata[2] == note:
                        chordfrom[j] = str(notenumber)
            chordfrom = ', '.join(chordfrom)
            array_conversions_final[chordfrom] = chordto

        #Now we need to translate
        #We loop through all chords
        if level == 'm':
            for x in range(0, len(array_validobjects)):
                note = array_validobjects[x]
                chord = ', '.join(str(v) for v in note[6])
                #PM(chord)
                #PM("\n")
                #If a chord is in array_conversions_final it means it needs translating 
                if chord in array_conversions_final:
                    #We go through each chord note and see what it translates to
                    for j in range(0, len(note[6])):
                        #We take the letter from the translation
                        note_letter = array_conversions_final[chord][j]
                        #We get the number of the note
                        for notenumber, notedata in notes_dict.iteritems():
                            if notedata[1] == leveltext and notedata[2] == note_letter:
                                note_number = notenumber
                        #We go through the notes in the chord and look for the position for the note
                        for k in range(0, len(note[2])):
                            sub_note = note[2][k]
                            if sub_note == note[6][j]:
                                note[2][k] = note_number
        else:
            array_objects = list(array_validobjects)
            array_validobjects = []
            array_chords = []

            for x in range(0, len(array_objects)):
                note = array_objects[x]
                if len(note[6])==2:
                    chord = ', '.join(str(v) for v in note[6])
                    if chord in array_conversions_final:
                        newchord_array = array_conversions_final[chord]
                        new_chord = [[], [], [], [], [], [], []]
                        for j in range(0, len(note)):
                            new_chord[j].append(note[j][0])
                        for j in range(0, len(newchord_array)):
                            new_note = newchord_array[j]
                            for notenumber, notedata in notes_dict.iteritems():
                                if notedata[1] == leveltext and notedata[2] == new_note:
                                    chordto = notenumber
                            new_chord[2][j] = chordto
                            new_chord[6][j] = chordto
                        array_validobjects.append(new_chord)
                else:
                    array_validobjects.append(note)  
                        
    array_notes = add_objects(array_notes, array_validobjects)
    write_midi(instrument, [array_notes, array_events], end_part, start_part)

def edit_by_mbt(instrument, level, measure, beat, tick, notes, selected):
    #Measure, beat and tick: 0 for any, a number for specific measure or specific beat
    #0.1.50 removes note from any measure, beat 1, first eighth note
    #0.0.50 removes note from any measure, any beat, first eighth note
    #notes: array of G, R, Y, B, O containing only notes to be processed
    global maxlen
    PM(instrument + " - " + level + " - " + str(measure) + " - " + str(beat) + " - " + str(tick) + " - ")
    PM("\n")
    PM(notes)
    PM("\n")
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    
    instrumentname = ''
    leveltext = level

    array_validnotes = [] #The final array going in the array of notes and events
    array_notes = []
    
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    if "REAL_KEYS" in instrumentname or "KEYS_ANIM" in instrumentname:
        leveltext = "notes"
    else:
        leveltext = "notes_"+leveltext
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    
    first_measure = 0
    last_measure = 0
    if(selected):
        first_measure = mbt(int(selected_range(array_notesevents[0])[0]))[0]
        last_measure = mbt(int(selected_range(array_notesevents[0])[1]))[0]
    if selected and first_measure == last_measure:
        result = RPR_MB( "This command works from measure to measure, please selected notes from at least 2 different measures", "Invalid selection", 0)
        return
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        this_measure = mbt(int(note[1]))[0]
        if (notes_dict[note[2]][1] == leveltext or note[2] == 110 or note[2] == 111 or note[2] == 112) and \
           (selected == 0 or (selected and (this_measure >= first_measure and this_measure <= last_measure))):
            array_validnotes.append(note)
        else:
            array_notes.append(note)

    array_validobjects = note_objects(array_validnotes)
    array_tokeep = []
    for x in range(0,len(array_validobjects)):
        note = array_validobjects[x]
        measurebeat = mbt(note[1][0])
        this_measure = measurebeat[0]
        this_beat = measurebeat[1]
        this_tick = measurebeat[2]
        if this_measure == measure or measure == 100:
            if this_beat == beat or beat == 100:
                if this_tick == tick or tick == 100:
                    note_object = [[], [], [], [], [], [], []]
                    for j in range(0, len(note[6])):
                        pitch = note[2][j]
                        letter = notes_dict[pitch][2]
                        if letter not in notes:
                            for k in range(0, 7):
                                note_object[k].append(note[k][j])
                    if len(note_object[0]) > 0:
                        array_tokeep.append(note_object)
                else:
                    array_tokeep.append(note)
            else:
                array_tokeep.append(note)
        else:
            array_tokeep.append(note)
            
    array_notes = add_objects(array_notes, array_tokeep)
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)

        
def copy_od_solo():
    #Loop through pro keys x. 
    global maxlen
    instrument = tracks_array["PART REAL_KEYS_X"]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    
    instrumentname = ''
    
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes"
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    
    array_validnotes = [] #The final array going in the array of notes and events
    array_notes = []
    solo = 0
    od = 0
    
    for x in range(0, len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrumentname)
            return
        if notes_dict[note[2]][1] == "od":
            od = 1
        elif notes_dict[note[2]][1] == "solo":
            solo = 1
        if od == 1 and solo == 1:
            break

    #If OD and solo markers are present, do nothing
    if od != 1 or solo != 1:
        instrument_b = tracks_array["PART KEYS"]
        array_instrument_data = process_instrument(instrument_b)
        array_instrument_notes = array_instrument_data[1]
        array_notesevents_b = create_notes_array(array_instrument_notes)
        
        instrumentname = ''
        
        for instrument_name, instrument_id in tracks_array.iteritems():
            if instrument_id == instrument_b:
                instrumentname = instrument_name
                
        notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
        #PM(array_notesevents_b[0])
        for x in range(0, len(array_notesevents_b[0])):
            note = array_notesevents_b[0][x]
            if notes_dict[note[2]][1] == "od" and od == 0:
                array_notesevents[0].append(note)
            elif notes_dict[note[2]][1] == "solo" and solo == 0:
                note[2] = 115
                array_notesevents[0].append(note)
        
    #Otherwise, if OD is missing, loop through 5 lane and copy OD
    #If solo is missing, loop through 5 lane and copy solo
    write_midi(instrument, [array_notesevents[0], array_notesevents[1]], end_part, start_part)

def add_slides(instrument, selected):
    #Loop through all vocal notes
    #For every note, look through the events array for a lyric
    #If no lyrics is present, add a + lyric at the note's position
    global maxlen
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_events = array_notesevents[1]
    
    instrumentname = ''

    array_validnotes = [] #The final array going in the array of notes and events
    array_notes = []
    
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes"
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrumentname)
            return
        this_measure = mbt(int(note[1]))[0]
        if notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and note[0] == 'e')):
            array_validnotes.append(note)
        else:
            array_notes.append(note)

    for x in range(0, len(array_validnotes)):
        note = array_validnotes[x]
        position = note[1]
        found = 0
        for j in range(0, len(array_events)):
            event = array_events[j]
            if event[1] == position and event[5] == 'ff05':
                found = 1
                break
        if found == 0:
            array_events.append(['<X', position, '0', '+', '>', 'ff05'])
            
    write_midi(instrument, [array_notesevents[0], array_events], end_part, start_part)


def tubes_space(instrument, selected):

    global maxlen
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]
    #PM("\n\ninstrument: "+instrument)
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = [] #The final array going in the array of notes and events
    array_tempnotes = [] #The temp array containing the objects
    instrumentname = ''
    old_note = []
    leveltext = "phrase"
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name

    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    array_validnotes = []
    array_od = []
        
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] in notes_dict and notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and note[0] == 'e')):
            array_validnotes.append(note)
        elif note[2] in notes_dict and notes_dict[note[2]][1] == "od":
            array_od.append(note)
        else:
            array_notes.append(note)

    #We pass the valid notes array through a function that returns an object array with one element per note/chord
    for x in range(0,len(array_validnotes)):
        note = array_validnotes[x]
        if x < len(array_validnotes)-1: #We fix too long phrases
        #Get current position+length
            end_position = note[1]+note[4]
            distance = array_validnotes[x+1][1]-end_position
            #Let's get the sustain space based on BPM and difficulty

            if distance < phrases_space:
                new_distance = (array_validnotes[x+1][1]-note[1])-phrases_space
                note[4] = new_distance
                for j in range(0, len(array_od)):
                    overdrive = array_od[j]
                    if overdrive[1] == note[1]:
                        overdrive[4] = new_distance
                        break

    array_validnotes.extend(array_notes)
    array_validnotes.extend(array_od)
    
    write_midi(instrument, [array_validnotes, array_notesevents[1]], end_part, start_part)

def remove_invalid_chars(instrument, selected):
    global maxlen
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]
    #PM("\n\ninstrument: "+instrument)
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_events = [] #The final array going in the array of events

    array_validevents = []

    #This doesn't work, Reaper doesn't save selection status for markers. We leave it here in case we find a workaround
    for x in range(0,len(array_notesevents[1])):
        event = array_notesevents[1][x]
        if selected == 0 or (selected and event[0] == 'x'):
            array_validevents.append(event)
        else:
            array_events.append(event)

    for x in range(0, len(array_validevents)):
        event = array_validevents[x]
        if event[5] == 'ff05':
            event[3] = event[3].translate(None, invalid_chars)
    array_validevents.extend(array_events)
    
    write_midi(instrument, [array_notesevents[0], array_validevents], end_part, start_part)

def capitalize_first(instrument, selected):
    #Take the first lyric on or after the location and check for capitalization
    global maxlen
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]
    #PM("\n\ninstrument: "+instrument)
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = [] #The final array going in the array of notes and events
    array_tempnotes = [] #The temp array containing the objects
    instrumentname = ''
    old_note = []
    leveltext = "phrase"
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name

    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    array_phrases = []
    #Loop through all phrase notes and get location (selected or non selected, based on user's choice)
    #Build an array of phrases with location and duration
    #Loop through all lyrics that are <= location of each phrase marker
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] in notes_dict and notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and note[0] == 'e')):
            array_phrases.append([note[1], note[1]+note[4]])
    for x in range(0, len(array_phrases)):
        start = array_phrases[x][0]
        end = array_phrases[x][1]
        for j in range(0, len(array_notesevents[1])):
            event = array_notesevents[1][j]
            if event[1] >= start and event[5] == 'ff05':
                if event[3][:1] != "'":
                    event[3] = event[3].capitalize()
                else:
                    temp_event = event[3][1:]
                    temp_event = temp_event.capitalize()
                    event[3] = event[3][:1]+temp_event
                break
            elif event[1] > end: #Phrase marker is empty
                break
                                 
    write_midi(instrument, [array_notesevents[0], array_notesevents[1]], end_part, start_part)


def check_capitalization(instrument, selected):
    #Take the first lyric on or after the location and check for capitalization
    PM(instrument)
    PM("\n")
    global maxlen
  
    if instrument == '':
        instrument = get_trackid()
        phrase_instrument = get_trackid()
    else:
        if instrument == 'HARM3':
            phrase_instrument = tracks_array['HARM1']
        else:
            phrase_instrument = tracks_array[instrument]
        instrument = tracks_array[instrument]
        
    #PM("\n\ninstrument: "+instrument)
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = [] #The final array going in the array of notes and events
    array_tempnotes = [] #The temp array containing the objects
    instrumentname = ''
    old_note = []
    leveltext = "phrase"
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name

    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    array_phrases = []

    array_instrument_data_phrase = process_instrument(phrase_instrument)
    array_instrument_notes_phrase = array_instrument_data_phrase[1]
    array_notesevents_phrase = create_notes_array(array_instrument_notes_phrase)
    
    #Loop through all phrase notes and get location (selected or non selected, based on user's choice)
    #Build an array of phrases with location and duration
    #Loop through all lyrics that are <= location of each phrase marker
    for x in range(0,len(array_notesevents_phrase[0])):
        note = array_notesevents_phrase[0][x]
        if note[2] in notes_dict and notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and note[0] == 'e')):
            array_phrases.append([note[1], note[1]+note[4]])
    check = 0
    PM(array_phrases)
    for x in range(0, len(array_phrases)):
        start = array_phrases[x][0]
        end = array_phrases[x][1]
        first = 0
        for j in range(0, len(array_notesevents[1])):
            event = array_notesevents[1][j]
            if event[1] >= start and event[5] == 'ff05' and first == 0:
                first = 1
                first_letter = event[3][:1]
                quotes = 0
                if first_letter == "'":
                    quotes = 1
                    first_letter = event[3][1]
                if first_letter.islower():
                    result = 1
                    check = 1
                    #If we find both, we ask the user whether to abort or proceed
                    result = RPR_MB( "The first word in this phrase ("+event[3]+") is not capitalized. Capitalize it?", "Lower case found", 1 )
                    if result == 1:
                        if quotes == 0:
                            event[3] = event[3].capitalize()
                        else:
                            temp_event = event[3][1:]
                            temp_event = temp_event.capitalize()
                            event[3] = event[3][:1]+temp_event
            elif event[1] >= start and event[5] == 'ff05' and first == 1 and event[1] < end:
                first_letter = event[3][:1]
                quotes = 0
                if first_letter == "'":
                    quotes = 1
                    first_letter = event[3][1]
                if first_letter.isupper() and event[3] != 'I' and "I'" not in event[3]:
                    result = 1
                    check = 1
                    #If we find both, we ask the user whether to abort or proceed
                    result = RPR_MB( "A word in the middle of the phrase is capitalized ("+event[3]+"). Make it lower case?", "Upper case found", 1 )
                    if result == 1:
                        if quotes == 0:
                            event[3] = event[3].lower()
                        else:
                            temp_event = event[3][1:]
                            temp_event = temp_event.capitalize()
                            event[3] = event[3][:1]+temp_event 
            elif event[1] >= end:
                break
    if check == 0:
        result = RPR_MB( "No issues found", "Capitalization", 0 )
    write_midi(instrument, [array_notesevents[0], array_notesevents[1]], end_part, start_part)

def export_lyrics_all(phrasing):   

    export_lyrics("PART VOCALS", phrasing)
    export_lyrics("HARM1", phrasing)
    export_lyrics("HARM2", phrasing)
    export_lyrics("HARM3", phrasing)

def export_lyrics(instrument, phrasing):
    selected = 0
    #Take the first lyric on or after the location and check for capitalization
    PM(instrument)
    PM("\n")
    global maxlen
    lyrics_instrument = instrument
  
    if instrument == '':
        instrument = get_trackid()
        phrase_instrument = get_trackid()
    else:
        if instrument == 'HARM3':
            phrase_instrument = tracks_array['HARM1']
        else:
            phrase_instrument = tracks_array[instrument]
        instrument = tracks_array[instrument]
        
    #PM("\n\ninstrument: "+instrument)
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = [] #The final array going in the array of notes and events
    array_tempnotes = [] #The temp array containing the objects
    instrumentname = ''
    old_note = []
    leveltext = "phrase"
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name

    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    array_phrases = []

    array_instrument_data_phrase = process_instrument(phrase_instrument)
    array_instrument_notes_phrase = array_instrument_data_phrase[1]
    array_notesevents_phrase = create_notes_array(array_instrument_notes_phrase)
    
    #Loop through all phrase notes and get location (selected or non selected, based on user's choice)
    #Build an array of phrases with location and duration
    #Loop through all lyrics that are <= location of each phrase marker
    for x in range(0,len(array_notesevents_phrase[0])):
        note = array_notesevents_phrase[0][x]
        if note[2] in notes_dict and notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and note[0] == 'e')):
            array_phrases.append([note[1], note[1]+note[4]])
    check = 0
    PM(array_phrases)
    phrase_lyrics = ''
    for x in range(0, len(array_phrases)):
        start = array_phrases[x][0]
        end = array_phrases[x][1]
        first = 0
        array_phrase_lyrics = []
        if phrasing and lyrics_instrument != 'HARM3':
            phrase_lyrics += '@'
        for j in range(0, len(array_notesevents[1])):
            event = array_notesevents[1][j]
            if event[1] >= start and event[5] == 'ff05' and event[1] < end:
                lyrics = event[3]
                phrase_lyrics+=lyrics+" "
            elif event[1] >= end:
                phrase_lyrics+="\r\n"
                break      
    file_name = get_curr_project_filename()
    file_name = file_name[:-4]
    file_name+="_"+array_partlyrics[lyrics_instrument]+".txt"
    #PM(phrase_lyrics)
    with open (file_name, "w") as myfile:
        myfile.write(phrase_lyrics)
    

def unpitch(instrument, character, selected):
    global maxlen
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_events = array_notesevents[1]
    
    instrumentname = ''

    array_validnotes = [] #The final array going in the array of notes and events
    array_notes = []
    
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes"
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] in notes_dict and notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and note[0] == 'e')):
            position = note[1]
            found = 0
            for j in range(0, len(array_events)):
                event = array_events[j]
                if event[1] == position and event[5] == 'ff05' and '#' not in event[3] and '^' not in event[3]:
                    if "$" in event[3]:
                        event[3] = event[3].translate(None, "$")
                        event[3]+=character+"$"
                    else:
                        event[3]+=character
                    break
                
    write_midi(instrument, [array_notesevents[0], array_notesevents[1]], end_part, start_part)

def pitch(instrument, selected):
    global maxlen
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_events = array_notesevents[1]
    
    instrumentname = ''

    array_validnotes = [] #The final array going in the array of notes and events
    array_notes = []
    
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes"
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] in notes_dict and notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and note[0] == 'e')):
            position = note[1]
            found = 0
            for j in range(0, len(array_events)):
                event = array_events[j]
                if event[1] == position and event[5] == 'ff05' and ('#' in event[3] or '^' in event[3]):
                    event[3] = event[3].translate(None, "#")
                    event[3] = event[3].translate(None, "^")
                    break
                
    write_midi(instrument, [array_notesevents[0], array_notesevents[1]], end_part, start_part)

def hide_lyrics(instrument, selected):
    global maxlen
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_events = array_notesevents[1]
    
    instrumentname = ''

    array_validnotes = [] #The final array going in the array of notes and events
    array_notes = []
    
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes"
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] in notes_dict and notes_dict[note[2]][1] == leveltext and (selected == 0 or (selected and note[0] == 'e')):
            position = note[1]
            found = 0
            for j in range(0, len(array_events)):
                event = array_events[j]
                if event[1] == position and event[5] == 'ff05' and '$' not in event[3]:
                    event[3]+='$'
                    break
                
    write_midi(instrument, [array_notesevents[0], array_notesevents[1]], end_part, start_part)

def create_phrase_markers(instrument, grid, mute):
    global maxlen
    instrument_text = instrument
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_events = array_notesevents[1]
    
    instrumentname = ''

    array_validnotes = [] #The final array going in the array of notes and events
    array_validevents = []
    
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes"
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
    full = 0
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrumentname)
            return
        if notes_dict[note[2]][1] == "phrase" or notes_dict[note[2]][1] == "od":
            full = 1
            break
        
    result = 1
    if full == 1 and mute == 0:
        result = RPR_MB( "Phrase markers or overdrive phrases found. Do you want to delete them and proceed?", "Phrase markers found", 1 )
        if result == 2:
            return
    
    array_notes = list(array_notesevents[0])
    
    if result == 1 and full == 1:
        array_notes = []
        for x in range(0,len(array_notesevents[0])):
            note = array_notesevents[0][x]
            if notes_dict[note[2]][1] != "phrase" and notes_dict[note[2]][1] != "od":
                array_notes.append(note)
                

    #Let's create an array of notes
    for x in range(0,len(array_notes)):
        note = array_notes[x]
        if notes_dict[note[2]][1] == leveltext:
            array_validnotes.append(note)

    #Let's create an array of lyrics
    for x in range(0,len(array_notesevents[1])):
        event = array_notesevents[1][x]
        if event[5] == 'ff05': #It's a lyric
            array_validevents.append(event)
            
    #Loop through lyrics and every time we find a @ character in the lyrics we set that-1/64th as starting point for the phrase marker
    start = 0
    end = 0
    new_start = 0
    for x in range(0, len(array_validevents)):
        event = array_validevents[x]
        if phrase_char in event[3] and start == 0: #We need to start a phrase
            #When we have a start marker we proceed looping to find the next one
            start = event[1]
            event[3] = event[3].translate(None, phrase_char)
        elif phrase_char in event[3]:
            #Once we do we take that position, we set it as new_next and look for the last note before that marker
            new_start = event[1]
            event[3] = event[3].translate(None, phrase_char)
            for j in reversed(range(0, len(array_validnotes))):
                note = array_validnotes[j]
                if note[1] < event[1]:
                    #We take the note position, add its length and 1/64th and set that as end
                    end = note[1]+note[4]
                    break
            #We create a phrase marker with start and end
            length = end - start + (phrases_space*2)
            phrase_marker = ['E', (start-phrases_space), 105, '60', length, '90']
            array_notes.append(phrase_marker)
            start = new_start

    #Now we do the same for the last phrase marker
    if start > 0:
        note = array_validnotes[-1]
        #We take the note position, add its length and 1/64th and set that as end
        end = note[1]+note[4]
        #We create a phrase marker with start and end
        length = end - start + (phrases_space*2)
        phrase_marker = ['E', (start-phrases_space), 105, '60', length, '90']
        array_notes.append(phrase_marker)

    array_percussions = []
    array_percussions_set = []
    start = 0
    end = 0
    #loop through all notes and look for displayed percussions to create an array of starts and ends of tambourine sections
    for x in range(0, len(array_notes)):
        note = array_notes[x]
        if notes_dict[note[2]][1] == "percussion":
            array_percussions_set.append(note)
        elif notes_dict[note[2]][1] != "percussion" and len(array_percussions_set) > 0:
            array_percussions.append(array_percussions_set)
            array_percussions_set = []
    if len(array_percussions_set) > 0:
        array_percussions.append(array_percussions_set)

    #PM(array_percussions)
    #Loop through that array and at first position-1/64th set the phrase start
    reset = 0
    for x in range(0, len(array_percussions)):
        array_percussions_set = array_percussions[x]
        for j in range(0, len(array_percussions_set)):
            percussion = array_percussions_set[j]
            
            if j == 0 or reset == 1:
                reset = 0
                start = percussion[1]
            elif percussion[1]-start >= correct_tqn*4*2 and (array_percussions_set[-1][1]-percussion[1]) > correct_tqn*4 and \
                 (j == len(array_percussions_set)-1 or array_percussions_set[j+1][1]-percussion[1] > correct_tqn*0.25):
                end = percussion[1]+percussion[4]
                length = end - start + (phrases_space*2)
                phrase_marker = ['E', int(start-phrases_space), 105, '60', int(length), '90']

                array_notes.append(phrase_marker)
                reset = 1
        end = percussion[1]+percussion[4]
        length = end - start + (phrases_space*2)
        phrase_marker = ['E', (start-phrases_space), 105, '60', length, '90']
        array_notes.append(phrase_marker)
    
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)
    
    #Once finished, we fire the trim_phrase_markers function
    trim_phrase_markers(instrument_text, grid)
    
    
def trim_phrase_markers(instrument, grid):
    #grid is the grid line in tick: quarter is 480, eighth is 240
    global maxlen
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_events = array_notesevents[1]
    division = int(math.floor((correct_tqn*4)*divisions_array['q']))
    instrumentname = ''

    array_validnotes = [] #The final array going in the array of notes and events
    array_validphrases = []
    array_notes = []
    array_od = []
    
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "notes"
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    
    #Let's create an array of notes
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrumentname)
            return
        if notes_dict[note[2]][1] == "phrase":
            array_validphrases.append(note)
        elif notes_dict[note[2]][1] == "notes" or notes_dict[note[2]][1] == "percussion":
            array_validnotes.append(note)
        elif notes_dict[note[2]][1] == "od":
            array_od.append(note)
        else:
            array_notes.append(note)
    
    #Get start of phrase
    for x in range(0, len(array_validphrases)):
        phrase = array_validphrases[x]
        position = mbt(phrase[1])[3]
        grid_check = int(math.floor(position/division))
        #If it's on a quarter grid, do nothing
        #if position-(grid_check*division) > 0:
        #If it's not, get position of the first note of the phrase
        notes_found = 0
        for j in range(0, len(array_validnotes)):
            note = array_validnotes[j]
            if note[1] >= phrase[1] and note[1] < phrase[1]+phrase[4]:
                notes_found = 1
                note_position = mbt(note[1])[3]
                for k in reversed(range(0, 32)):
                    if k*grid < note_position-phrases_space:
                        #Get the first quarter grid before that position
                        new_position = note[1]-(note_position-(k*grid))
                        break
                    new_position = note[1]-note_position-grid #We catch any note that's on or 1/64th later than the first beat
                break
        #Check if the previous phrase marker ends on or after that quarter grid
        if notes_found == 1 and (x == 0 or (array_validphrases[x-1][1]+array_validphrases[x-1][4]+phrases_space) < new_position):                                                 
            #If it doesn't, set that as new start
            for j in range(0, len(array_od)):
                overdrive = array_od[j]
                if overdrive[1] == phrase[1]:
                    overdrive[4]+= overdrive[1]-new_position
                    overdrive[1] = new_position
                    break
            phrase[4]+= phrase[1]-new_position
            phrase[1] = new_position
                
                
    #Get end of phrase           
    for x in range(0, len(array_validphrases)):
        phrase = array_validphrases[x]
        end_of_phrase = phrase[1]+phrase[4]
        position = mbt(end_of_phrase)[3]
        grid_check = int(math.floor(position/division))
        #If it's on a quarter grid, do nothing
        if position-(grid_check*division) > 0:
            #If it's not, get position of the last note of the phrase
            notes_found = 0
            for j in reversed(range(0, len(array_validnotes))):
                note = array_validnotes[j]
                if note[1] < end_of_phrase and note[1] >= phrase[1]:
                    notes_found = 1
                    end_of_note = note[1]+note[4]
                    note_position = mbt(end_of_note)[3]
                    for k in range(0, 32):
                        if k*grid > note_position+phrases_space:
                            #Get the first quarter grid after that position
                            new_position = end_of_note+((k*grid)-note_position)
                            break
                        measure = mbt(end_of_note)[0]
                        first_beat = measures_array[measure-1][1]
                        new_position = first_beat+grid #We catch any note that's on or 1/64th earlier than the last beat
                    break
                
            #Check if the next phrase marker starts on or after that quarter grid
            if notes_found == 1 and (x == len(array_validphrases)-1 or (array_validphrases[x+1][1]-phrases_space) > new_position):
                for j in range(0, len(array_od)):
                    overdrive = array_od[j]
                    if overdrive[1] == phrase[1]:
                        overdrive[4] += new_position-end_of_phrase
                #If it doesn't, set that as new end
                phrase[4] += new_position-end_of_phrase

    array_notes.extend(array_validnotes)
    array_notes.extend(array_validphrases)
    array_notes.extend(array_od)
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)

def compact_harmonies(precedence, grid):
    #precedence tells us the order: main, secondary, tertiary
    #grid is in ticks
    #Main is the main harmony, meaning that that harmony is used to loop through and if a note needs to be fixed, main is the one from which we take start/end
    global maxlen
    #precedence = { 'main' : 'h1', 'second' : 'h2', 'third' : 'h3' }
    #grid = 30
    #Check if h1 and h2 are available, otherwise fail
    if tracks_array['HARM1'] == 999 or tracks_array['HARM2'] == 999:
        result = RPR_MB( "You don't have harmonies to compact", "No harmonies", 0)
        return

    #Check if h3 is available and build an h1, h2 and h3 array of notes
    instrument = tracks_array['HARM1']
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part_h1 = array_instrument_data[2]
    start_part_h1 = array_instrument_data[3]
    array_notesevents_h1 = create_notes_array(array_instrument_notes)
    instrument_h2 = tracks_array['HARM2']
    array_instrument_data = process_instrument(instrument_h2)
    array_instrument_notes = array_instrument_data[1]
    end_part_h2 = array_instrument_data[2]
    start_part_h2 = array_instrument_data[3]
    array_notesevents_h2 = create_notes_array(array_instrument_notes)
    if tracks_array['HARM3'] != 999:
        instrument_h3 = tracks_array['HARM3']
        array_instrument_data = process_instrument(instrument_h3)
        array_instrument_notes = array_instrument_data[1]
        end_part_h3 = array_instrument_data[2]
        start_part_h3 = array_instrument_data[3]
        array_notesevents_h3 = create_notes_array(array_instrument_notes)     

    array_validnotes_h1 = []
    array_validnotes_h2 = []
    array_validnotes_h3 = []
    array_notes_h1 = []
    array_notes_h2 = []
    array_notes_h3 = []
    array_lyrics_h1 = []
    array_lyrics_h2 = []
    array_lyrics_h3 = []

    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    array_lyrics_h1 = array_notesevents_h1[1]
    array_lyrics_h2 = array_notesevents_h2[1]
    
    #Let's create an array of notes
    for x in range(0,len(array_notesevents_h1[0])):
        note = array_notesevents_h1[0][x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, "HARM1")
            return
        if notes_dict[note[2]][1] == "phrase":
            array_validnotes_h1.append(note)
        else:
            array_notes_h1.append(note)

    #Let's create an array of notes
    for x in range(0,len(array_notesevents_h2[0])):
        note = array_notesevents_h2[0][x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, "HARM2")
            return
        if notes_dict[note[2]][1] == "phrase":
            array_validnotes_h2.append(note)
        else:
            array_notes_h2.append(note)
            
    if tracks_array['HARM3'] != 999:
        array_lyrics_h3 = array_notesevents_h3[1]
        for x in range(0,len(array_notesevents_h3[0])):
            note = array_notesevents_h3[0][x]
            if note[2] not in notes_dict:
                invalid_note_mb(note, "HARM3")
                return
            if notes_dict[note[2]][1] == "phrase":
                array_validnotes_h3.append(note)
            else:
                array_notes_h3.append(note)

    
    
    #Name the main array as main
    main = eval('array_notes_'+precedence['main'])
    mainlyrics = eval('array_lyrics_'+precedence['main'])
    second = eval('array_notes_'+precedence['second'])
    secondlyrics = eval('array_lyrics_'+precedence['second'])
    third = eval('array_notes_'+precedence['third'])
    thirdlyrics = eval('array_lyrics_'+precedence['third'])
    
    if len(second) == 0:
        result = RPR_MB( "Your secondary harmony track is empty", "Empty harmony track", 0)
        return

    #Loop through main and for each note check if on secondary there's a note early or late by grid
    for x in range(0, len(main)):
        note = main[x]
        position = note[1]
        for j in range(0, len(second)):
            s_note = second[j]
            s_position = s_note[1]
            #If so, check if the note is longer or shorter than main's by grid
            if abs(position-s_position) == 0 and abs(note[4]-s_note[4]) == 0:
                 pass
            elif abs(position-s_position) <= grid and abs(note[4]-s_note[4]) <= grid:
                #If so, make the secondary note the same as main
                s_note[1] = note[1]
                s_note[4] = note[4]
                for k in range(0, len(secondlyrics)):
                    lyric = secondlyrics[k]
                    if lyric[1] == s_position and lyric[5] == 'ff05':
                        lyric[1] = position
                        break
                break

    if len(third) > 0:
        #Repeat for tertiary if it exists
        for x in range(0, len(main)):
            note = main[x]
            position = note[1]
            for j in range(0, len(third)):
                s_note = third[j]
                s_position = s_note[1]
                #If so, check if the note is longer or shorter than main's by grid
                if abs(position-s_position) == 0 and abs(note[4]-s_note[4]) == 0:
                    pass
                elif abs(position-s_position) <= grid and abs(note[4]-s_note[4]) <= grid:
                    #If so, make the secondary note the same as main
                    s_note[1] = note[1]
                    s_note[4] = note[4]
                    for k in range(0, len(thirdlyrics)):
                        lyric = thirdlyrics[k]
                        if lyric[1] == s_position and lyric[5] == 'ff05':
                            lyric[1] = position
                            break
                    break
                
        #Repeat secondary against tertiary
        for x in range(0, len(second)):
            note = second[x]
            position = note[1]
            for j in range(0, len(third)):
                s_note = third[j]
                s_position = s_note[1]
                #If so, check if the note is longer or shorter than main's by grid
                if abs(position-s_position) == 0 and abs(note[4]-s_note[4]) == 0:
                    pass
                elif abs(position-s_position) <= grid and abs(note[4]-s_note[4]) <= grid:
                    #If so, make the secondary note the same as main
                    s_note[1] = note[1]
                    s_note[4] = note[4]
                    for k in range(0, len(thirdlyrics)):
                        lyric = thirdlyrics[k]
                        if lyric[1] == s_position and lyric[5] == 'ff05':
                            lyric[1] = position
                            break
                    break
         
    array_notes_h1.extend(array_validnotes_h1)
    write_midi(instrument, [array_notes_h1, array_lyrics_h1], end_part_h1, start_part_h1)
    
    array_notes_h2.extend(array_validnotes_h2)
    write_midi(instrument_h2, [array_notes_h2, array_lyrics_h2], end_part_h2, start_part_h2)
    
    if tracks_array['HARM3'] != 999:
        array_notes_h3.extend(array_validnotes_h3)
        write_midi(instrument_h3, [array_notes_h3, array_lyrics_h3], end_part_h3, start_part_h3)

def add_vocalsoverdrive(instrument, frequency, mute):
    global maxlen
    instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = array_notesevents[0]
    instrumentname = ''

    array_validnotes = []
    
    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    leveltext = "phrase"
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    full = 0
    for x in range(0,len(array_notes)):
        note = array_notes[x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrumentname)
            return
        if notes_dict[note[2]][1] == "od":
            full = 1
            break
        
    result = 1
    if full == 1 and mute == 0:
        result = RPR_MB( "Overdrive phrases found. Do you want to delete them and proceed?", "Overdrive found", 1 )
        if result == 2:
            return
        
    array_notes = list(array_notesevents[0])
    
    if result == 1 and full == 1:
        array_notes = []
        for x in range(0,len(array_notesevents[0])):
            note = array_notesevents[0][x]
            if notes_dict[note[2]][1] != "od":
                array_notes.append(note)

        
    for x in range(0,len(array_notes)):
        note = array_notes[x]
        if notes_dict[note[2]][1] == "phrase":
            for j in range(0, len(array_notes)):
                valid = 1
                s_note = array_notes[j]
                if notes_dict[s_note[2]][1] == "percussion" and s_note[1] >= note[1] and s_note[1] <= note[1]+note[4]:
                    valid = 0
                    break
            if valid == 1:
                array_validnotes.append(note)

    for x in range(0, len(array_validnotes)-4): #We leave the last 4 measures free for OD use

        if ((x+1) % frequency) == 0:
            note = array_validnotes[x]
            phrase = list(note)
            phrase[2] = 116
            array_notes.append(phrase)
            
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)
    

def fix_textevents(instrument, what):
    #What tells us whether to check for all issues, for text events or for lyrics only
    #0: check all
    #1: check only lyrics incorrectly set as anything else
    #2: check only events ([...]) set as anything else
    global maxlen
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_events = array_notesevents[1] #The final array going in the array of events

    #Loop through all text events
    for x in range(0,len(array_events)):
        event = array_events[x]
        if (what == 0 or what == 1) and "[" not in event[3] and event[5] == 'ff01':
            event[5] = 'ff05'
        elif (what == 0 or what == 2) and "[" in event[3] and event[5] != 'ff01':
            event[5] = 'ff01'
    
    write_midi(instrument, [array_notesevents[0], array_events], end_part, start_part)

def cleanup_phrases(instrument):
    global maxlen
    if instrument == '':
        instrument = get_trackid()
    else:
        instrument = tracks_array[instrument]
    #PM("\n\ninstrument: "+instrument)
    array_instrument_data = process_instrument(instrument)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)

    array_phrases = []
    array_od = []
    array_notes = []
    array_remove = []

    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument:
            instrumentname = instrument_name
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    #This doesn't work, Reaper doesn't save selection status for markers. We leave it here in case we find a workaround
    for x in range(0,len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrumentname)
            return
        if notes_dict[note[2]][1] == "phrase":
            array_phrases.append(note)
        elif notes_dict[note[2]][1] == "od":
            array_od.append(note)
        else:
            array_notes.append(note)
            
    #Loop for all phrases markers
    #If no note >= or <= is found, delete marker and delete overdrive
    for x in range(0, len(array_phrases)):
        note = array_phrases[x]
        found = 0
        for j in range(0, len(array_notes)):
            s_note = array_notes[j]
            if (s_note[1] >= note[1] and s_note[1] < note[1]+note[4]) or (s_note[1]+s_note[4] > note[1] and s_note[1]+s_note[4] < note[1]+note[4]):
                found = 1
                break
        if found == 0:
            array_remove.append(note[1])
            
    array_validphrases = []
    array_validod = []
    
    
    for x in range(0, len(array_phrases)):
        note = array_phrases[x]
        if note[1] not in array_remove:
            array_validphrases.append(note)
            
    for x in range(0, len(array_od)):
        note = array_od[x]
        if note[1] not in array_remove:
            array_validod.append(note)

    array_notes.extend(array_validphrases)
    array_notes.extend(array_validod)
    write_midi(instrument, [array_notes, array_notesevents[1]], end_part, start_part)
    
def compact_phrases():
    global maxlen
    
    if tracks_array['HARM1'] != 999 and tracks_array['HARM2'] != 999:
        instrument = tracks_array['HARM1']
        array_instrument_data = process_instrument(instrument)
        array_instrument_notes = array_instrument_data[1]
        end_part_h1 = array_instrument_data[2]
        start_part_h1 = array_instrument_data[3]
        array_notesevents_h1 = create_notes_array(array_instrument_notes)
        array_notes_h1 = array_notesevents_h1[1]
        instrument_h2 = tracks_array['HARM2']
        array_instrument_data = process_instrument(instrument_h2)
        array_instrument_notes = array_instrument_data[1]
        end_part_h2 = array_instrument_data[2]
        start_part_h2 = array_instrument_data[3]
        array_notesevents_h2 = create_notes_array(array_instrument_notes)
        array_notes_h2 = array_notesevents_h2[1]
        instrument_v = tracks_array['PART VOCALS']
        array_instrument_data = process_instrument(instrument_v)
        array_instrument_notes = array_instrument_data[1]
        end_part_v = array_instrument_data[2]
        start_part_v = array_instrument_data[3]
        array_notesevents_v = create_notes_array(array_instrument_notes)

        array_validnotes_h1 = []
        array_validnotes_h2 = []
        array_notes_h1 = []
        array_notes_h2 = []

        for instrument_name, instrument_id in tracks_array.iteritems():
            if instrument_id == instrument:
                instrumentname = instrument_name
        notes_dict = notesname_array[notesname_instruments_array[instrumentname]]
            
        
        #Let's create an array of notes
        for x in range(0,len(array_notesevents_h1[0])):
            note = array_notesevents_h1[0][x]
            if note[2] not in notes_dict:
                invalid_note_mb(note, "HARM1")
                return
            if notes_dict[note[2]][1] == "phrase":
                array_validnotes_h1.append(note)
            else:
                array_notes_h1.append(note)

        #Let's create an array of notes
        for x in range(0,len(array_notesevents_h2[0])):
            note = array_notesevents_h2[0][x]
            if note[2] not in notes_dict:
                invalid_note_mb(note, "HARM2")
                return
            if notes_dict[note[2]][1] == "phrase":
                array_validnotes_h2.append(note)
            else:
                array_notes_h2.append(note)

        #For each phrase marker on H1 we check if there's an H2 marker with position >= H1 position and position <= H1 end
        for x in range(0, len(array_validnotes_h1)):
            note = array_validnotes_h1[x]
            for j in range(0, len(array_validnotes_h2)):
                h2_note = array_validnotes_h2[j]
                if h2_note[1] >= note[1] and h2_note[1] <=  note[1]+note[4]:
                    #If h2 starts later, check if the earlier h2 phrase marker's end position is > h1 position. If not, set h2 phrase marker's start to h1's.
                    if h2_note[1] > note[1] and (j == 0 or array_validnotes_h2[j-1][1]+array_validnotes_h2[j-1][4] < note[1]):
                        h2_note[4]+=h2_note[1]-note[1]
                        h2_note[1] = note[1]
                    #If h2 ends earlier, check if the next h2 phrase marker's start position is < h1 end. If not, set h2 phrase marker's end to h1's
                    if h2_note[1]+h2_note[4] < note[1]+note[4] and (j == len(array_validnotes_h2)-1 or array_validnotes_h2[j+1][1] > note[1]+note[4]):
                        h2_note[4] += (note[1]+note[4])-(h2_note[1]+h2_note[4])
                    #If h2 ends later, check if the next h1 phrase marker's start position is < h2 end. If not, set h1 phrase marker's end to h2's
                    if h2_note[1]+h2_note[4] > note[1]+note[4] and (x == len(array_validnotes_h1)-1 or array_validnotes_h1[x+1][1] > h2_note[1]+h2_note[4]):
                        for k in range(0, len(array_notesevents_v[0])):
                            overdrive = array_notesevents_v[0][k]
                            if notes_dict[overdrive[2]][1] == "od" and overdrive[1] == note[1]:
                                for n in range(0, len(array_notesevents_v[0])):
                                    vocal_phrase = array_notesevents_v[0][n]
                                    if notes_dict[vocal_phrase[2]][1] == "phrase" and vocal_phrase[1] == note[1]:
                                        vocal_phrase[4] += (h2_note[1]+h2_note[4])-(note[1]+note[4])
                                        break
                                overdrive[4] += (h2_note[1]+h2_note[4])-(note[1]+note[4])
                                break
                            
                        note[4] += (h2_note[1]+h2_note[4])-(note[1]+note[4])
                        
                        
        for x in range(0, len(array_validnotes_h2)):
            note = array_validnotes_h2[x]
            for j in range(0, len(array_validnotes_h1)):
                h1_note = array_validnotes_h1[j]
                if h1_note[1] >= note[1] and h1_note[1] <=  note[1]+note[4]:
                    #If h2 starts later, check if the earlier h2 phrase marker's end position is > h1 position. If not, set h2 phrase marker's start to h1's.
                    if h1_note[1] > note[1] and (j == 0 or array_validnotes_h1[j-1][1]+array_validnotes_h1[j-1][4] < note[1]):
                        for j in range(0, len(array_notesevents_v[0])):
                            overdrive = array_notesevents_v[0][j]
                            if notes_dict[overdrive[2]][1] == "od" and overdrive[1] == h1_note[1]:
                                overdrive[4]+=overdrive[1]-note[1]
                                overdrive[1] = note[1]
                                break
                        h1_note[4]+=h1_note[1]-note[1]
                        h1_note[1] = note[1]
                    #If h2 ends earlier, check if the next h2 phrase marker's start position is < h1 end. If not, set h2 phrase marker's end to h1's
                    if h1_note[1]+h1_note[4] < note[1]+note[4] and (j == len(array_validnotes_h1)-1 or array_validnotes_h1[j+1][1] > note[1]+note[4]):
                        for j in range(0, len(array_notesevents_v[0])):
                            overdrive = array_notesevents_v[0][j]
                            if notes_dict[overdrive[2]][1] == "od" and overdrive[1] == h1_note[1]:
                                overdrive[4] += (note[1]+note[4])-(h1_note[1]+h1_note[4])
                                break
                        h1_note[4] += (note[1]+note[4])-(h1_note[1]+h1_note[4])
                    #If h2 ends later, check if the next h1 phrase marker's start position is < h2 end. If not, set h1 phrase marker's end to h2's
                    if h1_note[1]+h2_note[4] > note[1]+note[4] and (x == len(array_validnotes_h2)-1 or array_validnotes_h2[x+1][1] > h1_note[1]+h1_note[4]):
                        for k in range(0, len(array_notesevents_v[0])):
                            overdrive = array_notesevents_v[0][k]
                            if notes_dict[overdrive[2]][1] == "od" and overdrive[1] == h1_note[1]:
                                for n in range(0, len(array_notesevents_v[0])):
                                    vocal_phrase = array_notesevents_v[0][n]
                                    if notes_dict[vocal_phrase[2]][1] == "phrase" and vocal_phrase[1] == h1_note[1]:
                                        vocal_phrase[4] += (h1_note[1]+h1_note[4])-(note[1]+note[4])
                                        break
                                overdrive[4] += (h1_note[1]+h1_note[4])-(note[1]+note[4])
                                break
                        note[4] += (h1_note[1]+h1_note[4])-(note[1]+note[4])
                        
        array_notes_h1.extend(array_validnotes_h1)
        array_notes_h2.extend(array_validnotes_h2)
        write_midi(instrument, [array_notes_h1, array_notesevents_h1[1]], end_part_h1, start_part_h1)
        write_midi(instrument_h2, [array_notes_h2, array_notesevents_h2[1]], end_part_h2, start_part_h2)
        write_midi(instrument_v, [array_notesevents_v[0], array_notesevents_v[1]], end_part_v, start_part_v)
    else:
        return 'no h1 or h2'


def create_keys_animations():
    global maxlen
    instrument_keys = tracks_array['PART REAL_KEYS_X']
    array_instrument_data = process_instrument(instrument_keys)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_stdkeys = list(array_notesevents[0])

    instrument_keys = tracks_array['PART KEYS_ANIM_RH']
    array_instrument_data = process_instrument(instrument_keys)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)

    for instrument_name, instrument_id in tracks_array.iteritems():
        if instrument_id == instrument_keys:
            instrumentname = instrument_name
    notes_dict = notesname_array[notesname_instruments_array[instrumentname]]

    array_temp = []

    for x in range(0, len(array_notesevents[0])):
        note = array_notesevents[0][x]
        if notes_dict[note[2]][1] != "notes" and notes_dict[note[2]][1] != "shift":
            array_temp.append(note)


    for x in range(0, len(array_stdkeys)):
        note = array_stdkeys[x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, "PART REAL_KEYS_X")
            return

        if notes_dict[note[2]][1] == "notes" or notes_dict[note[2]][1] == "shift":
            array_temp.append(note)
            
    write_midi(instrument_keys, [array_temp, array_notesevents[1]], end_part, start_part)
            
###########################################################
#
# SUPERSETS
#
###########################################################

def reduce_5lane(instrument, levels, hard, medium, easy, chords, reduceChords, reduceNotes, singlesnare, mute, tolerance, unflip):
    #log("reduce_5lane", [instrument, levels, hard, medium, easy, mute, tolerance, unflip])
    #instrument is PART DRUMS, etc.
    #levels is an array with hard, medium and easy, 0 for no go, 1 for go
    #hard is an array with grid, medium and easy, 0 for no go, 1 for go
    global maxlen
    PM("\n\n")
    PM(instrument)
    PM("\n")
    PM(levels)
    PM("\n")
    PM(hard)
    PM("\n")
    PM(medium)
    PM("\n")
    PM(easy)
    PM("\n")
    PM(chords)
    PM("\n")
    PM(reduceChords)
    PM("\n")
    PM(reduceNotes)
    PM("\n")
    PM(singlesnare)
    PM("\n")
    PM(mute)
    PM("\n")
    PM(tolerance)
    PM("\n")
    PM(unflip)
    PM("\n")
    instrument_track = tracks_array[instrument]
    notes_dict = notesname_array[notesname_instruments_array[instrument]]

    array_instrument_data = process_instrument(instrument_track)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = array_notesevents[0]
    array_events = array_notesevents[1]

    #Check if Hard is full. If so, prompt to confirm deletion
    notes = count_notes(array_notes, 0, 0, ["notes_h"], 1, instrument_track)
    if notes == {}:
        return
    
    result = 0
    if notes != [] and levels[0] == 1 and mute == 0:
        result = RPR_MB( "Hard appears to already have notes in it: proceed deleting and re-creating reductions for hard?", "Notes found", 1 )

    if (notes == [] or result == 1 or mute == 1) and levels[0] == 1:

        #Clean Hard and copy from Expert
        array_full = list(array_notes)
        array_notes = []
        for x in range(0,len(array_full)):
            note = array_full[x]
            if note[2] not in notes_dict:
                invalid_note_mb(note, instrument)
                return
            if notes_dict[note[2]][1] != 'notes_h':
                array_notes.append(note)
        
        for x in range(0,len(array_notes)):
            note = array_notes[x]
            if notes_dict[note[2]][1] == 'notes_x':
                note_new = list(note)
                note_new[2] = note_new[2]-12
                array_notes.append(note_new)

        array_events_valid = []

        for x in range(0, len(array_events)):
            event = array_events[x]
            if "[mix 2" not in event[3]:
                array_events_valid.append(event)

        for x in range(0, len(array_events_valid)):
            event = array_events_valid[x]
            if "[mix 3" in event[3]:
                new_event = list(event)
                new_event[3] = new_event[3].replace("mix 3", "mix 2")
                array_events_valid.append(new_event)
                
        write_midi(instrument_track, [array_notes, array_events_valid], end_part, start_part)

        #Unflip, if needed
        if (instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X') and  unflip == 'h':
            unflip_discobeat(instrument, 'h', 20, 0)
        
        #remove_notes using 1/8th grid, sparse, pitch bend
        pitchbend = hard[3]
        if instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X':
            pitchbend = 0

        if (instrument == 'PART GUITAR' or instrument == 'PART BASS' or instrument == 'PART KEYS' or instrument == 'PART RHYTHM') and reduceChords:
            reduce_chords(instrument, 'h', chords[2], 0)
        
        remove_notes(hard[0],'h',instrument,tolerance,hard[1],hard[2],pitchbend,0)

        #Run simplify_roll
        simplify_roll(instrument, 'h', 0)

        if instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X':
            if singlesnare[0] != 'n':
                PM("snare hard")
                single_snare(instrument, 'h', singlesnare[0], 0)

        fix_sustains(instrument, 'h', 1, 0) #instrument, level, fix, selected
        
    #Check if Medium is full. If so, prompt to confirm deletion
    
    array_instrument_data = process_instrument(instrument_track)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = array_notesevents[0]

    notes = count_notes(array_notes, 0, 0, ["notes_m"], 1, instrument_track)

    result = 0
    if notes != [] and levels[1] == 1 and mute == 0:
        result = RPR_MB( "Medium appears to already have notes in it: proceed deleting and re-creating reductions for medium?", "Notes found", 1 )

    if (notes == [] or result == 1 or mute == 1) and levels[1] == 1:
        
        #Clean Medium and copy from Hard
        array_full = list(array_notes)
        array_notes = []
        for x in range(0,len(array_full)):
            note = array_full[x]
            if note[2] not in notes_dict:
                invalid_note_mb(note, instrument)
                return
            if notes_dict[note[2]][1] != 'notes_m':
                array_notes.append(note)

        for x in range(0,len(array_notes)):
            note = array_notes[x]
            if notes_dict[note[2]][1] == 'notes_h':
                note_new = list(note)
                note_new[2] = note_new[2]-12
                array_notes.append(note_new)
       
        array_events_valid = []

        for x in range(0, len(array_events)):
            event = array_events[x]
            if "[mix 1" not in event[3]:
                array_events_valid.append(event)

        for x in range(0, len(array_events_valid)):
            event = array_events_valid[x]
            if "[mix 2" in event[3]:
                new_event = list(event)
                new_event[3] = new_event[3].replace("mix 2", "mix 1")
                array_events_valid.append(new_event)
  
        write_midi(instrument_track, [array_notes, array_events_valid], end_part, start_part)

        #Unflip, if needed
        if (instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X') and  unflip == 'm':
            unflip_discobeat(instrument, 'm', 20, 0)

        if medium[3] == 1 and (instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X'):
            remove_kick(instrument, 'm', 'p', 0)

        #remove_notes using 1/4th grid, consecutive notes, sparse
        pitchbend = medium[3]
        if instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X':
            pitchbend = 0

        remove_notes(medium[0],'m',instrument,tolerance,medium[1],medium[2],pitchbend,0)

        if (instrument == 'PART GUITAR' or instrument == 'PART BASS' or instrument == 'PART KEYS' or instrument == 'PART RHYTHM') and reduceNotes:
            reduce_singlenotes(instrument, 'm', 0)

        if (instrument == 'PART GUITAR' or instrument == 'PART BASS' or instrument == 'PART KEYS' or instrument == 'PART RHYTHM') and reduceChords:
            reduce_chords(instrument, 'm', chords[1], 0)
   
        #Run simplify_roll
        simplify_roll(instrument, 'm', 0)

        if instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X':
            if singlesnare[1] != 'n':
                PM("snare medium")
                single_snare(instrument, 'm', singlesnare[1], 0)

        fix_sustains(instrument, 'm', 1, 0) #instrument, level, fix, selected
        
    #Check if Easy is full. If so, prompt to confirm deletion

    array_instrument_data = process_instrument(instrument_track)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = array_notesevents[0]

    notes = count_notes(array_notes, 0, 0, ["notes_e"], 1, instrument_track)

    result = 0
    if notes != [] and levels[2] == 1 and mute == 0:
        result = RPR_MB( "Easy appears to already have notes in it: proceed deleting and re-creating reductions for easy?", "Notes found", 1 )

    if (notes == [] or result == 1 or mute == 1) and levels[2] == 1:
        
        #Clean Easy and copy from Medium
        array_full = list(array_notes)
        array_notes = []
        for x in range(0,len(array_full)):
            note = array_full[x]
            if note[2] not in notes_dict:
                invalid_note_mb(note, instrument)
                return
            if notes_dict[note[2]][1] != 'notes_e':
                array_notes.append(note)
                
        for x in range(0,len(array_notes)):
            note = array_notes[x]
            if notes_dict[note[2]][1] == 'notes_m':
                note_new = list(note)
                note_new[2] = note_new[2]-12
                array_notes.append(note_new)

        array_events_valid = []

        for x in range(0, len(array_events)):
            event = array_events[x]
            if "[mix 0" not in event[3]:
                array_events_valid.append(event)

        for x in range(0, len(array_events_valid)):
            event = array_events_valid[x]
            if "[mix 1" in event[3]:
                new_event = list(event)
                new_event[3] = new_event[3].replace("mix 1", "mix 0")
                array_events_valid.append(new_event)
                
        write_midi(instrument_track, [array_notes, array_events_valid], end_part, start_part)

        #Unflip, if needed
        if (instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X') and  unflip == 'e':
            unflip_discobeat(instrument, 'e', 20, 0)

        if medium[3] == 1 and (instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X'):
            remove_kick(instrument, 'e', 'a', 0)

        #remove_notes using 1/2nd grid, consecutive notes, sparse
        pitchbend = easy[3]
        if instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X':
            pitchbend = 0

        if (instrument == 'PART GUITAR' or instrument == 'PART BASS' or instrument == 'PART KEYS' or instrument == 'PART RHYTHM') and reduceNotes:
            reduce_singlenotes(instrument, 'e', 0)

        if (instrument == 'PART GUITAR' or instrument == 'PART BASS' or instrument == 'PART KEYS' or instrument == 'PART RHYTHM') and reduceChords:
            reduce_chords(instrument, 'e', chords[0], 0)
           
        remove_notes(easy[0],'e',instrument,tolerance,easy[1],easy[2],pitchbend,0)

        #Run simplify_roll
        simplify_roll(instrument, 'e', 0)
        
        if instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X':
            if singlesnare[2] != 'n':
                PM("snare easy: " + str(singlesnare[2]))
                
                single_snare(instrument, 'e', str(singlesnare[2]), 0)

        fix_sustains(instrument, 'e', 1, 0) #instrument, level, fix, selected

def auto_animations(beattrack, expression, pause, grid, crash, soft, flam, tolerance, keys, mutevar):
    #Create the BEAT track
    create_beattrack(beattrack, 0)

    #Add animations markers
    array_anims = ["PART DRUMS", "PART GUITAR", "PART BASS", "PART VOCALS", "PART KEYS", "PART REAL_KEYS_X", "PART DRUMS 2X", "PART RHYTHM"]
    for x in range(0, len(array_anims)):
        if tracks_array[array_anims[x]] != 999:
            create_animation_markers(array_anims[x], expression, pause, mutevar)

    #Create drums animations
    array_drumsanims = ["PART DRUMS", "PART DRUMS 2X"]
    for x in range(0, len(array_drumsanims)):
        if tracks_array[array_drumsanims[x]] != 999:
            drums_animations(str(array_drumsanims[x]), int(crash), int(soft), int(flam), str(grid), int(tolerance), 10, int(mutevar))

    if keys == 1 and tracks_array['PART REAL_KEYS_X'] != 999:
        create_keys_animations()

def auto_generalcleanup(instruments, polish, grid, tolerance, invalidmarkers, sustains, whatsustains, odsolo, pedal, rolls):
    PM(instruments)
    PM("\n")
    PM(str(polish) + " - " + str(grid) + " - " + str(tolerance) + " - " + str(invalidmarkers) + " - " + str(sustains) + " - " + str(whatsustains) + " - " + str(odsolo) + " - " + str(pedal) + " - " + str(rolls))
    for x in range(0, len(instruments)):
        instrument = instruments[x]
        if polish == 1 and instrument != 'PART VOCALS':
            if instrument != 'PART REAL_KEYS':
                polish_notes(instrument, grid, int(tolerance), 0)
            else:
                polish_notes('PART REAL_KEYS_X', grid, int(tolerance), 0)
                polish_notes('PART REAL_KEYS_H', grid, int(tolerance), 0)
                polish_notes('PART REAL_KEYS_M', grid, int(tolerance), 0)
                polish_notes('PART REAL_KEYS_E', grid, int(tolerance), 0)
        if sustains == 1 and instrument != 'PART VOCALS':
            if instrument != 'PART REAL_KEYS':
                fix_sustains(instrument, 'x', whatsustains, 0)
                fix_sustains(instrument, 'h', whatsustains, 0)
                fix_sustains(instrument, 'm', whatsustains, 0)
                fix_sustains(instrument, 'e', whatsustains, 0)
            else:
                fix_sustains('PART REAL_KEYS_X', 'x', whatsustains, 0)
                fix_sustains('PART REAL_KEYS_H', 'h', whatsustains, 0)
                fix_sustains('PART REAL_KEYS_M', 'm', whatsustains, 0)
                fix_sustains('PART REAL_KEYS_E', 'e', whatsustains, 0)
        if invalidmarkers == 1:
            if instrument == 'PART VOCALS':
                if tracks_array['HARM1'] != 999:
                    filter_notes('HARM1')
                if tracks_array['HARM2'] != 999:
                    filter_notes('HARM2')
                if tracks_array['HARM3'] != 999:
                    filter_notes('HARM3')
                elif instrument == 'PART REAL_KEYS':
                    filter_notes('PART REAL_KEYS_X')
                    filter_notes('PART REAL_KEYS_H')
                    filter_notes('PART REAL_KEYS_M')
                    filter_notes('PART REAL_KEYS_E')
                else:
                    filter_notes(instrument)
                    
        if rolls == 1 and instrument != 'PART VOCALS':
            if instrument != 'PART REAL_KEYS':
                simplify_roll(instrument, 'h', 0)
                simplify_roll(instrument, 'm', 0)
                simplify_roll(instrument, 'e', 0)
            else:
                simplify_roll('PART REAL_KEYS_H', 'h', 0)
                simplify_roll('PART REAL_KEYS_M', 'm', 0)
                simplify_roll('PART REAL_KEYS_E', 'e', 0)
        if pedal == 1 and (instrument == 'PART DRUMS' or instrument == 'PART DRUMS 2X'):
            single_pedal('x', 20, 0)
    if odsolo == 1:
        copy_od_solo()
                

def auto_vocalscleanup(instruments, compactphrase, trim, grid, tubespace, cleanup, compactharmonies, prec, precgrid, removeinvalid, capitalize, fixtextevents, textv, checkcaps):
    PM(instruments)
    PM("\n")
    PM(prec)
    PM("\n")
    PM(str(compactphrase) + " - " + str(trim) + " - " + str(grid) + " - " + str(tubespace) +  " - " + str(cleanup) + " - " + str(compactharmonies) + " - " + str(precgrid) + " - " + str(removeinvalid) + " - " + str(capitalize) + " - " + str(fixtextevents)+ " - " + str(textv)+ " - " + str(checkcaps))
    for x in range(0, len(instruments)):
        instrument = instruments[x]
        if tracks_array[instrument] != 999:
            if tubespace == 1 and instrument != 'HARM3':
                tubes_space(instrument, 0)
            if trim == 1 and instrument != 'HARM3':
                trim_phrase_markers(instrument, grid)
            if cleanup == 1 and instrument != 'HARM3':
                cleanup_phrases(instrument)
            if cleanup == 1 and instrument != 'HARM3':
                cleanup_phrases(instrument)
            if removeinvalid == 1:
                remove_invalid_chars(instrument, 0)
            if capitalize == 1 and instrument != 'HARM3':
                capitalize_first(instrument, 0)
            if fixtextevents == 1:
                fix_textevents(instrument, textv)
            if checkcaps == 1:
                check_capitalization(instrument, 0)
            
                
    if compactphrase == 1 and tracks_array['HARM1'] != 999 and tracks_array['HARM2'] != 999:
        compact_phrases()
        
    if compactharmonies == 1 and tracks_array['HARM1'] != 999 and tracks_array['HARM2'] != 999:
        compact_harmonies(prec, precgrid)

def copy5laneodtopgb(instrument):

    #instrument (PART REAL_GUITAR, PART REAL_GUITAR_22, PART REAL_BASS, PART REAL_BASS_22)

    global maxlen
   
    instrument_track = tracks_array[instrument]
    notes_dict = notesname_array[notesname_instruments_array[instrument]]
   
    array_instrument_data = process_instrument(instrument_track)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = array_notesevents[0]
    array_events = array_notesevents[1]
    notes_found = 0
    result = 0
 
    for x in range(0, len(array_notes)):
        note = array_notes[x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrument)
            return
        if note[2] == 116 or note[2] == 115:
            notes_found = 1
            result = RPR_MB( "Overdrive and/or Solo markers found. Do you want to delete them and proceed?", "Overdrive and/or Solo markers found", 1 )
            break
 
    if result == 1 or notes_found == 0:
        array_temp = list(array_notes)
        array_notes = []
        for x in range(0, len(array_temp)):
            note = array_temp[x]
            if note[2] != 116 and note[2] != 115:
                array_notes.append(note)
    else:
        return

    pnotes = []
    fnotes = []

    for item in array_notes:
        pnotes.append(item)

    if "BASS" in instrument:
        finstrument = "PART BASS"
    else:
        finstrument = "PART GUITAR"

    finstrument_track = tracks_array[finstrument]
    fnotes_dict = notesname_array[notesname_instruments_array[finstrument]]
   
    farray_instrument_data = process_instrument(finstrument_track)
    farray_instrument_notes = farray_instrument_data[1]
    farray_notesevents = create_notes_array(farray_instrument_notes)
    farray_notes = farray_notesevents[0]

    for item in farray_notes:
        fnotes.append(item)

    for item in fnotes:
        if item[2] not in fnotes_dict:
            invalid_note_mb(item, finstrument)
            return
        if fnotes_dict[item[2]][1] == "od":
            pnotes.append(item)
        if fnotes_dict[item[2]][1] == "solo":
            item[2] = 115
            pnotes.append(item)

    write_midi(instrument_track, [pnotes, array_events], end_part, start_part)

def generate_fhp(instrument):
    #instrument (PART REAL_GUITAR, PART REAL_GUITAR_22, PART REAL_BASS, PART REAL_BASS_22)

    global maxlen
   
    instrument_track = tracks_array[instrument]
    notes_dict = notesname_array[notesname_instruments_array[instrument]]
   
    array_instrument_data = process_instrument(instrument_track)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = array_notesevents[0]
    array_events = array_notesevents[1]
    notes_found = 0
    result = 0
 
    for x in range(0, len(array_notes)):
        note = array_notes[x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrument)
            return
        if notes_dict[note[2]][1] == "fhp":
            notes_found = 1
            result = RPR_MB( "Fret Hand Position markers found. Do you want to delete them and proceed?", "Fret Hand Position markers found", 1 )
            break
 
    if result == 1 or notes_found == 0:
        array_temp = list(array_notes)
        array_notes = []
        for x in range(0, len(array_temp)):
            note = array_temp[x]
            if notes_dict[note[2]][1] != "fhp":
                array_notes.append(note)
    else:
        return

    

    lastlocation = 0
    lastfhp = 100

    for x in range(0, len(array_notes)):
        note = array_notes[x]
        pitch = note[2]
        location = note[1]
        if location == lastlocation:
            pass
        else:
            if pitch == 96 or pitch == 97 or pitch == 98 or pitch == 99 or pitch == 100 or pitch == 101:
                velocity = int(str(note[3]), 16)
                new_note = list(note)
                openstring = 0
                count = 0
                chord = []
                if "22" in instrument:
                    fhp = 119
                else:
                    fhp = 114
                for y in range(0, len(array_notes)):
                    note1 = array_notes[x]
                    note2 = array_notes[y]
                    pitch = note2[2]
                    if pitch == 96 or pitch == 97 or pitch == 98 or pitch == 99 or pitch == 100 or pitch == 101:
                        if note1[1] == note2[1]:
                            count = count + 1
                            chord.append(note2)
                            lastlocation = note2[1]
                count2 = 0
                numbers = []
                for item in chord:
                    numbers.append(int(str(item[3]), 16))
                lowest = numbers[0]
                highest = numbers[0]
                for item in numbers[1:]:
                    if item < lowest:
                        lowest = item
                    if item > highest:
                        highest = item
                if highest == 100:
                    if lastfhp == 100:
                        fhp = 101
                    else:
                        fhp = lastfhp
                elif highest >= lastfhp:
                    if highest <= lastfhp + 3:
                        fhp = lastfhp
                    else:
                        fhp = lowest
                elif highest < lastfhp:
                    fhp = lowest
                if fhp == 100 or fhp != lastfhp:
                    if fhp == 100:
                        fhp = 101
                    if "22" in instrument:
                        if fhp > 119:
                            fhp = 119
                    else:
                        if fhp > 114:
                            fhp = 114
                    new_note[3] = hex(fhp)
                    new_note[2] = 108
                    array_notes.append(new_note)

                    lastfhp = fhp
                    
                else:
                    continue
                    
    write_midi(instrument_track, [array_notes, array_events], end_part, start_part)

def pg_root_notes(instrument, estringlow, astring, dstring, gstring, bstring, estringhigh):
 
    #instrument (PART REAL_GUITAR, PART REAL_GUITAR_22, PART REAL_BASS, PART REAL_BASS_22)
    #all strings : tuning
 
    global maxlen
   
    instrument_track = tracks_array[instrument]
    notes_dict = notesname_array[notesname_instruments_array[instrument]]
   
    array_instrument_data = process_instrument(instrument_track)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = array_notesevents[0]
    array_events = array_notesevents[1]
    notes_found = 0
    result = 0
   
    string1 = 0 + estringlow
    string2 = 0 + astring
    string3 = 0 + dstring
    string4 = 0 + gstring
    string5 = 0 + bstring
    string6 = 0 + estringhigh
 
    for x in range(0, len(array_notes)):
        note = array_notes[x]
        if note[2] not in notes_dict:
            invalid_note_mb(note, instrument)
            return
        if notes_dict[note[2]][1] == "root_notes":
            notes_found = 1
            result = RPR_MB( "Root notes found. Do you want to delete them and proceed?", "Root notes found", 1 )
            break
 
    if result == 1 or notes_found == 0:
        array_temp = list(array_notes)
        array_notes = []
        for x in range(0, len(array_temp)):
            note = array_temp[x]
            if notes_dict[note[2]][1] != "root_notes":
                array_notes.append(note)
    else:
        return

    lastlocation = 0
 
    for x in range(0, len(array_notes)):
        note = array_notes[x]
        pitch = note[2]
        location = note[1]
        if location == lastlocation:
            pass
        else:
            if pitch == 96 or pitch == 97 or pitch == 98 or pitch == 99 or pitch == 100 or pitch == 101:
                #It's an expert note, let's add it as a root note
                velocity = int(str(note[3]), 16)
                new_note = list(note)
                openstring = 0
                count = 0
                chord = []
                for y in range(0, len(array_notes)):
                    note1 = array_notes[x]
                    note2 = array_notes[y]
                    pitch = note2[2]
                    if pitch == 96 or pitch == 97 or pitch == 98 or pitch == 99 or pitch == 100 or pitch == 101:
                        if note1[1] == note2[1]:
                            count = count + 1
                            chord.append(note2)
                            lastlocation = note2[1]
                if count > 1:
                    for item in chord:
                        if(pitch == 96):
                            note = item
                            break
                    for item in chord:
                        if(pitch == 97):
                            note = item
                            break
                    for item in chord:
                        if(pitch == 98):
                            note = item
                            break
                    for item in chord:
                        if(pitch == 99):
                            note = item
                            break
                    for item in chord:
                        if(pitch == 100):
                            note = item
                            break
                    for item in chord:
                        if(pitch == 101):
                            note = item

                if(note[2] == 96):                    #Which string? Which note?
                    openstring = 16 + string1
                elif(note[2] == 97):
                    openstring = 9 + string2
                elif(note[2] == 98):
                    openstring = 14 + string3
                elif(note[2] == 99):
                    openstring = 7 + string4
                elif(note[2] == 100):
                    openstring = 11 + string5
                elif(note[2] == 101):
                    openstring = 16 + string6

                root = openstring + velocity - 100
                roothigh = 15
                rootlow = 4
                while (root > roothigh):
                    root = root - 12
                    if(root < rootlow):
                        break
                while (root < rootlow):
                    root = root + 12
                    if(root > roothigh):
                        break
                new_note[2] = root
            
                array_notes.append(new_note)
           
    write_midi(instrument_track, [array_notes, array_events], end_part, start_part)

def gpimport_drums(instrument, notedata, GPnotes, offset):

    global maxlen
   
    instrument_track = tracks_array[instrument]
    notes_dict = notesname_array[notesname_instruments_array[instrument]]
   
    array_instrument_data = process_instrument(instrument_track)
    array_instrument_notes = array_instrument_data[1]
    end_part = array_instrument_data[2]
    start_part = array_instrument_data[3]
    array_notesevents = create_notes_array(array_instrument_notes)
    array_notes = array_notesevents[0]
    array_events = array_notesevents[1]
    notes_found = 0
    result = 0

    for x in range(0, len(array_notes)):
        note = array_notes[x]
        if notes_dict[note[2]][1] == "notes_x":
            result = RPR_MB( "Expert notes found. Do you want to delete those, and the tom and animations markers and proceed?", "Expert notes found", 1 )
            break
 
    if result == 1 or notes_found == 0:
        array_temp = list(array_notes)
        array_notes = []
        for x in range(0, len(array_temp)):
            note = array_temp[x]
            if notes_dict[note[2]][1] != "notes_x":
                if "Tom" not in notes_dict[note[2]][0]:
                    if notes_dict[note[2]][1] != "animations":
                        array_notes.append(note)

    w = 1920 #whole note
    h = 960 #1/2 note
    q = 480 #1/4 note
    e = 240 #1/8 note
    s = 120 #1/16
    t = 60 #1/32
    S = 30 #1/64
    T = 15 #1/128

    Tw = 1280 #triplet whole
    Th = 640 #triplet 1/2
    Tq = 320 #triplet 1/4
    Te = 160 #triplet 1/8
    Ts = 80 #triplet 1/16
    Tt = 40 #triplet 1/32
    TS = 20 #triplet 1/64
    TT = 10 #triplet 1/128

    selection = "E"
    pitches = [["Ride Cymbal (blue)", [99]], ["Crash Cymbal (green)", [100]], ["Hi-Hat (yellow)", [98]], ["Snare (red)", [97]], ["Bass Drum", [96]], ["High Tom (yellow)", [98, 110]], ["Mid Tom (blue)", [99, 111]], ["Low/Floor Tom (green)", [100, 112]]]
    velocity = hex(96)
    channel = 90 #channel 1

    offset1 = float(offset)
    offset2 = q * offset1
    offset3 = int(offset2)

    for item in GPnotes:
        location = item[1] + offset3
        if item[3] == "normal":
            for note in item[2]:
                for n in notedata:
                    if n[2] == 0 and int(n[0]) == note:
                        for data in pitches:
                            if data[0] == n[1]:
                                for i in data[1]:
                                    array_notes.append([selection, location, i, velocity, t, channel])

    #array_notes.append([selection, 0, pitches[0][1][0], velocity, 60, channel])

    write_midi(instrument_track, [array_notes, array_events], end_part, start_part)

def startup():
    global instrument_ticks
    global measures_array
    global tracks_array
    global config

    path = os.path.join( sys.path[0], "cat.ini" )
    f = open(path, 'r')
    config = {}
    for line in f:
        k, v = line.strip().split('=')
        config[k.strip()] = v.strip()
    f.close()
    
    try:
        prep_tracks()
    except UnicodeDecodeError:
        RPR_MB("Invalid file name found in one of your tracks. "\
                "Make sure there are no items with special characters in your project. \n\n"\
                "The culprit is usually the song file itself. Look for accents and symbols. " \
                "You can rename an item in Item Properties (F2).", 
                "Unicode Error", 0)
        raise
    #We start off getting the end event and the instrument ticks
    array_instrument_data = process_instrument(tracks_array["EVENTS"]) #This toggles the processing of the EVENTS chunk that sets end_event
    instrument_ticks = array_instrument_data[0] #Number of ticks per measure of the instrument
    measures_array = get_time_signatures(instrument_ticks) #Let's create the array with all measures with BPM, ticks and time signatures 
    if isinstance(measures_array, list) == False:
        result = RPR_MB( "No time markers found, aborting", "Invalid tempo map", 0)
        return

###########################################################

###########################################################
#
# EXTERNAL COMMANDS
#
###########################################################



#PM("\nMeasures:\n")
#PM(measures_array)
#instrument_dialogbox()
#PM(str(end_part)+" - "+str(start_part))
#PM(vars_array_string)
#PM(notestring)
#PM(array_instrument_notes)
#PM(str(instrument_ticks))
