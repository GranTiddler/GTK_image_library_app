import gi
from arbitraryButton import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk








win = Gtk.Window()

grid = Gtk.Grid()


global image
image = imageContainer("weevil.png",1, 70, 50, expand=True)
button = Gtk.Button.new_with_label("egg")

grid.attach(button, 1, 0, 1, 1)
grid.attach(image, 0, 0, 1, 1)


win.add(grid)

win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
