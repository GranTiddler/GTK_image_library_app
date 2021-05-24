from os import listdir
from os.path import isfile, join

import json

from ScaledImage import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Image Library")
        self.currentImage = 0
        self.sorted = []

        self.builder = Gtk.Builder()
        self.builder.add_from_file("image_library.glade")

        path = "./image_files"
        self.images = [f for f in listdir(path) if isfile(join(path, f))]
        for i in range(len(self.images)):
            self.images[i] = "./image_files/" + self.images[i]

        self.add(self.builder.get_object("main"))


        self.image = imageContainer(self.images[self.currentImage], 1000, 700, expand=True)
        self.builder.get_object("box").add(self.image)

        self.builder.get_object("tag_entry").connect("activate", self.on_return)
        self.builder.get_object("button_left").connect("clicked", self.left)
        self.builder.get_object("button_right").connect("clicked", self.right)
        self.builder.get_object("ESC").connect("clicked", self.escape)

        self.tag_init()

        self.grid_state()

    def tag_init(self):
        with open("tags.json", "r") as read_file:
            self.tags = json.load(read_file)

        for i in self.images:
            if i not in self.tags:
                self.tags[i] = []
        print(self.tags)

    def grid_state(self):
        self.builder.get_object("single_view").set_visible(False)
        self.builder.get_object("grid_view").set_visible(True)

        self.button_list = []
        self.image_list = []

        self.builder.get_object("scroll").set_size_request(1000, 200)
        for i in range(len(self.images)):
            new_image = imageContainer(self.images[i], 300, 200)
            self.image_list.append(new_image)

            new_button = IdButton(i)
            new_button.add(new_image)
            new_button.connect("clicked", self.grid_clicked)
            self.button_list.append(new_button)

        """self.tag_list = []
        for i in self.tags["all"]:
            new_button = IdToggleButton(i)
            new_button.add(Gtk.Label(label=i))
            new_button.connect("toggled", self.tag_button)
            self.tag_list.append(new_button)


        for i in range(len(self.tag_list)):
            if i == 0:
                self.builder.get_object("tag_grid").attach(self.tag_list[i], i, 0, 1, 1)
            else:
                self.builder.get_object("tag_grid").attach(self.tag_list[i], i % 6, (i - (i % 6)) / 3, 1, 1)"""

        for i in range(len(self.image_list)):
            if i == 0:
                self.builder.get_object("image_grid").attach(self.button_list[i], i, 0, 1, 1)
            else:
                self.builder.get_object("image_grid").attach(self.button_list[i], i%3, (i-(i%3))/3, 1, 1)

    def single_view(self, id):
        print(self.images[id])
        self.builder.get_object("grid_view").set_visible(False)
        self.builder.get_object("single_view").set_visible(True)
        self.currentImage = id
        self.image.switch_image(self.images[id])

        self.change_title()
        self.get_tags()

    def on_return(self, entry):
        text = entry.get_text()
        entry.set_text("")
        if text != "":
            self.add_tag(text)

    def grid_clicked(self, button):
        self.single_view(button.get_id())

    def escape(self, button):
        self.grid_state()

    def left(self, button):
        self.currentImage = (self.currentImage-1) % len(self.images)
        self.image.switch_image(self.images[self.currentImage])
        self.image.update()
        self.builder.get_object("box").remove(self.builder.get_object("switch"))
        self.builder.get_object("box").add(self.builder.get_object("switch"))

        self.get_tags()
        self.change_title()

    def right(self, button):
        self.currentImage = (self.currentImage + 1) % len(self.images)
        self.image.switch_image(self.images[self.currentImage])
        self.builder.get_object("box").remove(self.builder.get_object("switch"))
        self.builder.get_object("box").add(self.builder.get_object("switch"))

        self.get_tags()
        self.change_title()

    def add_tag(self, tag):
        if tag not in self.tags[self.images[self.currentImage]]:
            self.tags[self.images[self.currentImage]].append(tag)
        if tag not in self.tags["all"]:
            self.tags["all"].append(tag)

        with open("tags.json", "w") as write_file:
            json.dump(self.tags, write_file)

        self.get_tags()

    def get_tags(self):
        box = self.builder.get_object("list")

        box.set_text("\n\n".join(self.tags[self.images[self.currentImage]]))

    def change_title(self):
        name = self.images[self.currentImage]
        name = name.split("/")
        name = name[-1].split(".")[0]
        self.builder.get_object("header").set_text(name)
        self.builder.get_object("title2").set_text(name)

    def tag_button(self, button):

        if button.get_active():
            self.sorted.append(button.get_id())
        else:
            self.sorted.remove(button.get_id())
        print(self.sorted)


        for i in range(len(self.button_list)):
            for j in self.sorted:
                if j in self.tags[self.images[i]]:
                    pass
                    self.button_list[i].set_visible(True)
                else:
                    self.button_list[i].set_visible(False)













win = window()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()