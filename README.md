# Description

This is a Siddur (Jewish prayer book) written for Maemo (N900) and other 
Python/Gtk environment.

# Installation

The MaemoSiddur requires a python/gtk environment. This is standard 
under most Linux desktop environments, and may be downloaded for 
Windows from http://www.pygtk.org/downloads.html .

MaemoSiddur is especially suited for the Maemo Linux environment 
(therefore its name!) available on the Nokia N900 phone. MaemoSiddur supports flipping the pages by the volume keys, but to get that supported binary python module hardkeys.so must be copied to its the python directory, see below. (Please let me know if you want me to create a real installer!)

There was no suitable free font available that was suitable for a siddur so 
I modified the Culmus Frank-Ruehl font to add opentype tables for proper 
nikud placement. The resulting fonts have been given the working name 
AAA*.otf . 

# Maemo installation commands

    root
    mv arm*/hardkeys.so /opt/pymaemo/usr/lib/python2.5/site-packages/
    exit
    cp AAA*.otf ~/.fonts
    python MaemoSiddor.py

# Running 

Run by doing 

    python MaemoSiddor.py
    
which shows a list of support prayer books.

# Screenshot

![screenshot](./MaemoSiddurScreenshot.png)

# License

This script is released under the GPL licence version 3.0

Thanks to Jacob Tardell <python@tardell.se>, the author of the calendrial module.

Thanks Thomas Perl and the gPodder Team for the portrait.py module.

Thanks to David Greve for the calendar logics at http://www.david-greve.de/luach-code/holidays.html .
