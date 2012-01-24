//======================================================================
//  hardkeys.c - A module for disabling maemo hardware keys.
//
//  Dov Grobgeld <dov.grobgeld@gmail.com>
//  Sun Feb 28 12:11:51 2010
//----------------------------------------------------------------------

#include <Python.h>
#include <gdk/gdkx.h>
#include <X11/Xlib.h>
#include <X11/Xatom.h>
#include <stdio.h>
#include <pygobject.h>           
#include <pygtk/pygtk.h>

static PyTypeObject *PyGObject_Type=NULL;    

static PyObject *
hardkeys_grab_zoom_keys(PyObject *self, PyObject *args);

static PyMethodDef HardKeyMethods[] = {
    {"grab_zoom_keys",  hardkeys_grab_zoom_keys, METH_VARARGS,
     "Grab zoom keys."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC
inithardkeys(void)
{
    Py_InitModule("hardkeys", HardKeyMethods);
    PyObject *module;
    
    init_pygobject();
    init_pygtk();
    module = PyImport_ImportModule("gobject");
    if (module) {
        PyGObject_Type =
            (PyTypeObject*)PyObject_GetAttrString(module, "GObject");
        Py_DECREF(module);
    }
}

static PyObject *
hardkeys_grab_zoom_keys(PyObject *self, PyObject *args)
{
    PyGObject *py_widget;                         
    GtkWidget *widget;
    int grab;

    if (!PyArg_ParseTuple(args,
                          "O!i", PyGObject_Type, &py_widget,
                          &grab))
        return NULL;
    widget = GTK_WIDGET(py_widget->obj);
    
    Display *dpy = gdk_x11_drawable_get_xdisplay(widget->window);
    Window win = GDK_WINDOW_XID(widget->window);

    Atom atom = XInternAtom( dpy, "_HILDON_ZOOM_KEY_ATOM", 0);
    unsigned long val = grab?1:0;
    XChangeProperty (dpy, win,
                     XInternAtom( dpy, "_HILDON_ZOOM_KEY_ATOM", 0),
                     XA_INTEGER, 32,
                     PropModeReplace, (unsigned char *) &val,
                     1);

    return Py_None;
}

