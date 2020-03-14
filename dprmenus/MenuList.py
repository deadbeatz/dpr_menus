
# Top level class. Contains references to all Menus, which in turn hold all respective menu items
class MenuList(object):
    def __init__(self):
        # List of all menus. Should be indexed off curr_menu. So the order you add them is the order
        # they will index using next/prev menu functions
        self.menus = []
        self.__curr_menu = 0
        
    @property
    def curr_menu(self):
        return self.__curr_menu
        
    @curr_menu.setter
    def curr_menu(self, new_menu):
        # Do nothing
        if self.__curr_menu is new_menu:
            return
        # If we are on the last menu, new menu will be first menu
        if new_menu > len(self.menus) -1:
            new_menu = 0
        elif new_menu < 0:
            new_menu = len(self.menus) -1

        # Fire on leave for curr_menu before selecting new menu
        self.menus[self.__curr_menu].on_leave()
        # Update index		
        self.__curr_menu = new_menu
        # Fire on enter for new menu
        self.menus[self.__curr_menu].on_enter()
    
    def init(self):
        for menu in self.menus:
            menu.on_init()

    def next_menu(self, exclude=None):
        if self.curr_menu +1 is exclude:
            return
        self.menus[self.curr_menu].on_leave()
        self.curr_menu = self.curr_menu + 1
        self.menus[self.curr_menu].on_enter()
        #self.menus[self.curr_menu].on_select()

    def prev_menu(self, exclude=None):
        if self.curr_menu -1 is exclude:
            return
        self.menus[self.curr_menu].on_leave()
        self.curr_menu = self.curr_menu - 1
        self.menus[self.curr_menu].on_enter()
        #self.menus[self.curr_menu].on_select()

    def add(self, menu):
        menu.id = len(self.menus)
        menu.menu_list = self
        self.menus.append(menu)
    
    def action(self, *args):
        return self.menus[self.curr_menu].on_action(*args)

    def draw_menus(self):
        for menu in self.menus:
            if menu.id == self.curr_menu:
                menu.draw(is_active=True)
            else:
                menu.draw(is_active=False)

    def draw_marquees(self, marquee_index):
        for menu in self.menus:
            if menu.id == self.curr_menu:
                return menu.draw_marquee(marquee_index)

    def scroll(self, direction):
        menu = self.menus[self.curr_menu]
        if menu.index is -1:
            return
        
        menu.scroll(direction)

    # Save some keystrokes by returning active menu
    def active_menu(self):
        return self.menus[self.curr_menu]










