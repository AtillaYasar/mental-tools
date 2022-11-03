import tkinter as tk
import tkinter.font

# app has:
##    - improved word boundaries
##    - tabsize set to 2 spaces
##    - window stays on top
##    - pretty colors
##    - press Escape to print contents of windoww


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
root.attributes('-topmost', True)
root.geometry('400x100-0+0')

root.title('RAM aid')
set_word_boundaries(root)

c1 = 'cyan'
c2 = 'black'
t = tk.Text(root, fg=c1, bg=c2, insertbackground='white',
            selectforeground=c2, selectbackground=c1)

w = t
font = tkinter.font.Font(font=w['font'])
tab = font.measure(' '*2)
w.config(tabs=tab)

# prints contents of "ram" so you can paste it before closing the app
def func(event):
    print('---------------------')
    print(t.get(1.0, 'end')[:-1])
    print('---------------------')

root.bind('<Escape>', func)
t.pack()

root.mainloop()
