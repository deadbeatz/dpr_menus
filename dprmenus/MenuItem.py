from .Utils import Utils

class MenuItem:
    def __init__(self, name, id, string=None, selected_color="|23|00", unselected_color="|16|15", highlighted_color="|19|00", decorator = None, attr1 = None, attr2 = None, is_header=False, attributes={}):
        self.name = name
        self.id = id
        self.__string = string
        self.__selected_color = selected_color
        self.__unselected_color = unselected_color
        self.__highlighted_color = highlighted_color
        self.decorator = decorator
        self.is_active = False
        self.string = string
        self.attr1 = attr1
        self.attr2 = attr2
        self.is_header = is_header
        self.attributes = {}
        self.attributes.update(attributes)


    @property
    def selected(self):
        string = ""
        if self.is_active and self.decorator is not None:
            string += self.decorator.colors + self.decorator.decorator
        string += str(self.__selected_color + Utils.strip_mci(self.string))
        return string

    @property
    def unselected(self):
        string = ""
        if self.is_active and self.decorator is not None:
            string += self.decorator.colors + self.decorator.decorator
        string += str(self.__unselected_color + self.string)
        return string

    @property
    def highlighted(self):
        string = ""
        if self.is_active and self.decorator is not None:
            string += self.decorator.colors + self.decorator.decorator
        string += str(self.__highlighted_color + Utils.strip_mci(self.string))
        return string

    # actual length of string is the string as rendered + MCI codes. So we need to tell the draw
    # function how long the MCI codes are but differencing the regular and stripped strings
    @property
    def raw_mci_len(self):
        return len(self.string) - len(Utils.strip_mci(self.string))

    @property
    def mci_len(self):
        return len(self.selected) - len(Utils.strip_mci(self.selected))

    @property
    def decorator_len(self):
        if self.decorator is not None and self.is_active:
            return len(self.decorator.decorator)
        return 0