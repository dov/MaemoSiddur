# Description

This is a Siddur (Jewish prayer book) written for Maemo (N900) and other 
Python/Gtk environment.

# Installation

The MaemoSiddur requires a python/gtk environment. This is standard 
under most Linux desktop environments, and may be downloaded for 
Windows from http://www.pygtk.org/downloads.html .

MaemoSiddur is especially suited for the Maemo Linux environment 
(therefore its name!) available on the Nokia N900 phone. MaemoSiddur supports flipping the pages by the volume keys, but to get that supported binary python module hardkeys.so must be copied to its the python directory, see below. (Please let me know if you want me to create a real installer!)

The font used is Culmus Frank Reuhl that was updated in December 2011 to include opentype tables for proper Nikud placement.

# Prayer texts

The Siddur currently comes with five books:

* Shacharit ashekenaz (not finished)
* Mincha
* Maariv
* Birkat hamazon
* Megilat Esther

The prayer texts are encoded in "conditional markups", where certain sections are made conditional on flags through the <cond flag="foo">...</fcond> specification. The flags are automatically calculated from the current date.

# Maemo installation commands

    root
    mv arm*/hardkeys.so /opt/pymaemo/usr/lib/python2.5/site-packages/
    exit
    cp Frank* ~/.fonts
    python MaemoSiddor.py

# Running 

Run by doing 

    python MaemoSiddor.py
    
which shows a list of support prayer books.

# Screenshot

![screenshot](./MaemoSiddurScreenshot.png)

# License

This script is released under the GPL licence version 3.0 by Dov Grobgeld <dov.grobgeld@gmail.com>.

Thanks to Jacob Tardell <python@tardell.se>, the author of the calendrial module.

Thanks Thomas Perl and the gPodder Team for the portrait.py module.

Thanks to David Greve for the calendar logics at http://www.david-greve.de/luach-code/holidays.html .
