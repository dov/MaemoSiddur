#!/usr/bin/python
# -*- Encoding: utf-8 -*-

import gtk, gobject, sys
import hardkeys
from condhtmltextview import *
try:
    import hildon
    do_hildon = True
    from portrait import FremantleRotation
except:
    do_hildon = False

# The following code is taken from
#   http://libre2.adacore.com/viewvc/trunk/gps/share/plug-ins/text_utils.py?view=markup&pathrev=131464
# and shows how to override key bindings.

SPACE=32
F7=65476
F8=65477
BACKSPACE=65288

def override (key, modifier, movement, step, select):
    gtk.binding_entry_remove (gtk.TextView, key, modifier)
    gtk.binding_entry_add_signal (gtk.TextView, key, modifier,
                                  "move_cursor",
                                  gobject.TYPE_ENUM, movement,
                                  gobject.TYPE_INT,  step,
                                  gobject.TYPE_BOOLEAN, select)

# Allow scrolling by tapping at the top or bottom of widget
def on_button_press(widget, event):
    height=widget.allocation.height
    if event.y < height/5:
        gtk.bindings_activate(widget, BACKSPACE, 0)
    elif event.y > height*4/5:
        gtk.bindings_activate(widget, SPACE, 0)

def override_key_bindings (select):
    """Override the default TextView keybinding to either always force
       the extension the selection, or not"""
    override (F7,        0, gtk.MOVEMENT_PAGES, 1, select)
    override (F8,    0, gtk.MOVEMENT_PAGES, -1, select)
    override (SPACE,        0, gtk.MOVEMENT_PAGES, 1, select)
    override (BACKSPACE,    0, gtk.MOVEMENT_PAGES, -1, select)

if do_hildon:
    w = hildon.Window()
    rotation = FremantleRotation('panvu', w, '1.0', FremantleRotation.AUTOMATIC)
    pa = hildon.PannableArea()
else:
    w = gtk.Window(gtk.WINDOW_TOPLEVEL)
    pa = gtk.ScrolledWindow()

w.connect("destroy", gtk.main_quit)
v=gtk.VBox()
w.add(v)

tv = CondHtmlTextView()
#tv = hildon.TextView()
#tv.set_editable(False)
tv.set_flag('purim')
tv.set_wrap_mode(gtk.WRAP_WORD)
tv.set_cursor_visible(False)
tv.connect("button-press-event", on_button_press)
override_key_bindings(select=False)
v.pack_start(pa, True, True, 0)
pa.add(tv)

txt = open(sys.argv[1]).read()
tv.display_html("""
    <body xmlns='http://www.w3.org/1999/xhtml'>
    <span style="font-family:AAA; font-size: large">%s
    </span>
    </body>
        """%txt)
w.show_all()
tv.grab_focus()
hardkeys.grab_zoom_keys(w, True)
gtk.main()


