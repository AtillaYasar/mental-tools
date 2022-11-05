import tkinter as tk
import tkinter.font
from datetime import datetime
import os, time
    
directory = r'C:\Users\Gebruiker\Desktop\mental tools'
filename = 'ram_aid_log.txt'
# creates txt if necessary
if filename not in os.listdir(directory):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('')

# app has:
##    - improved word boundaries
##    - tabsize set to 2 spaces
##    - window stays on top
##    - pretty colors
##    - press Escape to write contents of window + a time and date to a ram_aid.txt file.
##    - select text and hit ctrl or alt + a number to change the background color or text color

# returns date and time in 2 lines (tab in front by default), as a string
def date_time(infront='\t'):
    #from datetime import datetime
    t = datetime.now()
    date = t.date()
    h = t.hour
    m = t.minute
    return f'{infront}{date}\n{infront}{h}{m}'

# writes string to a file, and the timestamp.
# uses date_time() function if available, otherwise just uses time.time()
# requires os. (because who the hell doesnt import os)
def log_thing(thing, directory, filename, create_txt=False):
    path = f'{directory}/{filename}'

    # log the thing.
    to_add = thing
    #to_add = to_add.replace(', '.join([f'{k}-{v}' for k,v in color_numbers.items()]), '')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(to_add)

# improves word boundaries, so you can navigate better with (shift+) arrows
def set_word_boundaries(root):
    # this first statement triggers tcl to autoload the library
    # that defines the variables we want to override.  
    root.tk.call('tcl_wordBreakAfter', '', 0) 

    # this defines what tcl considers to be a "word". For more
    # information see http://www.tcl.tk/man/tcl8.5/TclCmd/library.htm#M19
    root.tk.call('set', 'tcl_wordchars', '[a-zA-Z0-9_.,]')
    root.tk.call('set', 'tcl_nonwordchars', '[^a-zA-Z0-9_.,]')

root = tk.Tk()
root.config(background='black')
#root.attributes('-topmost', True)

root.geometry('1000x600-0+0')

root.title('RAM aid')
set_word_boundaries(root)

c1 = 'cyan'
c2 = 'black'
sbg = 'grey'
t = tk.Text(root, fg=c1, bg=c2, insertbackground='white',
            selectforeground=c1, selectbackground=sbg,
            width=150, height=50)

w = t
font = tkinter.font.Font(font=w['font'])
tab = font.measure(' '*2)
w.config(tabs=tab)

# toggling the window being 'on top' or not
def toggle_topmost():
    window = root
    tup = window.attributes()
    ix = tup.index('-topmost')
    if tup[ix+1] == 1:
        window.attributes('-topmost', False)
    else:
        window.attributes('-topmost', True)

# logs contents of editor. and re-creates color dictionary
def func():
    
    contents = t.get(1.0, 'end')[:-1]

    timestamp = date_time()
    edge = '---------------------'
    to_log = '\n' + '\n'.join([edge,timestamp,contents,edge])
    
    directory = r'C:\Users\Gebruiker\Desktop\mental tools'
    filename = 'ram_aid_log.txt'
    
    log_thing(to_log, directory, filename)

    root.title('Saved')
    root.after(1000, lambda *a:root.title('RAM aid'))

t.pack()

def get_color(index, key):
    text = t
    #print(text.tag_names(index)[::-1])
    #print(text.tag_names(index))
    for tag in text.tag_names(index)[::-1]:
        fg = text.tag_cget(tag, key)
        if fg != "":
            return fg
    return text.cget(key)

def get_highlight_hotkeys(line):
    '''
str(line) -> dict(highlight_hotkeys)

- in on_press, highlight_hotkeys is used to see how to color a selected piece of text
- ctrl + a number changes the foreground, alt + a number changes the background
'''
    color_numbers = {tup[0]:tup[1] for tup in [section.split('-') for section in line.split(', ')]}
    highlight_hotkeys = {'alt':{k:{'background':v} for k,v in color_numbers.items()},
                     'control':{k:{'foreground':v} for k,v in color_numbers.items()}}
    return highlight_hotkeys

default_color_line = '1-green, 2-red, 3-cyan, 4-black, 5-grey, 6-orange, 7-blue, 8-brown, 9-purple, 0-violet'
t.insert('end', f'\n\n\ngeneric highlight\npositive\nnegative\n{default_color_line}')

highlight_counter = 1
def on_press(event):
    '''
Escape -> write to ram_aid_log.txt
control/alt + number -> change highlighted text:
    control for text color
    alt for background color

( potential improvements: other hotkey system than elifelifelifelif, remove need for global highlight_counter (maybe using
    a class), remove code duplication in alt/control branching, remove need for colors['selectbackground']=sgb )
'''
    global highlight_counter
    root.title(event.keysym)
    #root.title(str(time.time()).partition('.')[0])
    widget = event.widget

    # code duplication. key 'alt' in one case, key 'control' in another
        # only difference in following bifurcation is:
            # to get 'colors' from highlight_hotkeys you use the key 'alt' in one case, and 'control' in another
    if event.state == 131080: # if 'alt' is held
        lastline = t.get(1.0, 'end').split('\n')[-2]
        highlight_hotkeys = get_highlight_hotkeys(lastline)
        n = event.keysym
        
        colors = highlight_hotkeys['alt'].get(n, False) # check if number is in dictionary, if yes, continue
        if colors:
            # this is so that the color you pick for the background is the one actually shown (because the text is selected)
                # and then when a key other than ctrl or alt is pressed, it fixes the selectbackground.
            colors['selectbackground'] = colors['background']
            
            first,last = widget.index('sel.first'), widget.index('sel.last') # selection indices
            widget.tag_add(highlight_counter, first, last) # add mark
            widget.tag_config(highlight_counter, **colors) # configure mark using colors dictionary, which uses highlight_hotkey
    
            existing_settings = {key:get_color(first,key) # get existing settings
                                 for key in ('foreground','background','selectforeground','selectbackground')}
            highlight_counter += 1 # count up the thingy
            
    elif event.state == 12: # if 'control' is held
        lastline = t.get(1.0, 'end').split('\n')[-2]
        highlight_hotkeys = get_highlight_hotkeys(lastline)
        n = event.keysym
        
        colors = highlight_hotkeys['control'].get(n, False) # check if number is in dictionary, if yes, continue
        if colors:
            first,last = widget.index('sel.first'), widget.index('sel.last') # selection indices
            widget.tag_add(highlight_counter, first, last) # add mark
            widget.tag_config(highlight_counter, **colors) # configure mark using colors dictionary, which uses highlight_hotkey
    
            existing_settings = {key:get_color(first,key) # get existing settings
                                 for key in ('foreground','background','selectforeground','selectbackground')}
            highlight_counter += 1 # count up the thingy
    else:
        # put selectbackground back
            # for explanation, see above, where I do colors['selectbackground'] = colors['background']
        for i in range(1, int(highlight_counter)+1):
            t.tag_config(str(i), selectbackground=sbg)

        if event.keysym == 'Escape':
            func()
        elif event.keysym == 'F1':
            toggle_topmost()

root.bind('<KeyPress>', on_press)

root.mainloop()






