import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, Gdk

class IdButton(Gtk.Button):
    def __init__(self, id,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id

    def get_id(self):
        return self.id


class IdToggleButton(Gtk.ToggleButton):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id

    def get_id(self):
        return self.id


class imageContainer(Gtk.Button):
    def __init__(self, path, min_w, min_h, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.min_h = min_h
        self.min_w = min_w
        self.set_size_request(min_w, min_h)

        self.path = path
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.path)
        self.aspect_ratio = self.pixbuf.get_width() / self.pixbuf.get_height()
        self.img_surface = Gdk.cairo_surface_create_from_pixbuf(
            self.pixbuf, 1, None
        )

    def get_id(self):
        return self.id

    def get_useful_height(self):
        aw = self.get_allocated_width()
        pw = self.pixbuf.get_width()
        ph = self.pixbuf.get_height()
        return aw/pw * ph

    def get_scale_factor(self):
        return self.get_allocated_width() / self.pixbuf.get_width()

    def do_draw(self, context):
        height = self.get_useful_height()
        y_origin = 0
        x_origin = 0
        if height < self.get_allocated_height():
            sf = self.get_scale_factor()
            context.scale(sf, sf)
            
            y_origin = (self.get_allocated_height() / (2 * sf)) - (self.pixbuf.get_height() / 2)


        if height > self.get_allocated_height():
            sf = self.get_allocated_height() / self.pixbuf.get_height()
            context.scale(sf, sf)
            x_origin = (self.get_allocated_width() / (2 * sf)) - (self.pixbuf.get_width() / 2)

        context.set_source_surface(self.img_surface, x_origin, y_origin)
        context.paint()

    def switch_image(self, imagePath):
        self.path = imagePath
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.path)
        self.img_surface = Gdk.cairo_surface_create_from_pixbuf(self.pixbuf, 1, None)
        self.update()

    def update(self):
        self.set_size_request(self.min_w + 1, self.min_h)
