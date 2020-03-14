import mystic_bbs as bbs
from enum import Enum
import sys, os, time, math, re
from enum import Enum

def writexy(x,y,string):
    bbs.write("|[X"+str(x).zfill(2)+"|[Y"+str(y).zfill(2)+str(string))

def strip_mci(string):
    # Strip only color and location codes so we can get an effective length
    rgx_list = [r'(\|\[[XY]\d{2})' , r'(\|\d{2})']
    new_text = string
    for rgx_match in rgx_list:
        new_text = re.sub(rgx_match, '', new_text)
    return new_text

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

class MenuDecorator:
    def __init__(self, x, y, decorator, colors):
        self.x = x
        self.y = y
        self.decorator = decorator
        self.colors = colors

    def draw(self):
        writexy(self.x, self.y, self.colors + self.decorator)
    
    def clear(self):
        writexy(self.x, self.y, ' ' * len(self.decorator))

class ItemDecorator:
    def __init__(self, decorator, colors):
        self.decorator = decorator
        self.colors = colors

    def draw(self):
        writexy(self.x, self.y, self.colors + self.decorator)
    
    def clear(self):
        writexy(self.x, self.y, ' ' * len(self.decorator))

class Menu(object):
    def __init__(self, name, x, top_y, bottom_y, col_width, left_pad=1, right_pad=1, decorators = [], isselectable = True, blockscroll = False, wraparound = True, scrollbar = True):
        self.top_index = 0
        self.__index = -1
        self.__onKeys = {}
        self.__onExtendedKeys = {}
        self.__tabIndex = -1
        self.items = []

        # Args
        self.name = name
        self.x = x
        self.top_y = top_y
        self.bottom_y = bottom_y
        self.col_width = col_width
        # Sanity check padding, allow at least 1 char for string
        if left_pad + right_pad >= col_width - 2:
            self.lpad = 1
            self.rpad = 1
        else:
            self.lpad = left_pad
            self.rpad = right_pad
        self.decorators = []
        self.decorators.extend(decorators)
        self.isselectable = isselectable
        self.blockscroll = blockscroll
        self.wraparound = wraparound
        self.scrollbar = scrollbar

        # Helper values
        self.num_scr_lines = bottom_y - top_y + 1
        self.act_width = self.col_width - (self.lpad + self.rpad) + 1
        self.xpadded = self.x + self.lpad

        # Ref to parent class
        self.menu_list = None
        
        # Callbacks function wiring
        self.onAction = None
        self.onEnter = None
        self.onLeave = None
        self.onSelect = None
        self.onScroll = None
        self.onRedraw = None
        self.onInit = None
        self.onKey = None

    @property
    def index(self):
        return self.__index
        
    @index.setter
    def index(self, new_index):
        # Do nothing
        if self.__index is new_index:
            return
        else:
            # Update index		
            self.__index = new_index
            # Only fire if index is non-negative
            if self.__index < 0:
                return
            # Fire on select
            self.on_select()
    
    @property
    def key_bindings(self):
        return self.__onKeys

    @key_bindings.setter
    def key_bindings(self, char):
        #ToDo
        pass

    #Returns active selection. This saves lifes
    @property
    def curr_item(self):
        if len(self.items) is 0:
            return 
        # This should return None on index < 0, but that breaks everything right now
        #BUG fix index < 0 in program. 
        return self.items[self.__index]

    # ***Callbacks***
    # Keyed of action for current menu item
    def on_action(self, *args):
        if self.onAction is None:
            return
        return self.onAction(self, *args)

    # Keyed off menu change to this menu
    def on_enter(self):
        if self.onEnter is None:
            return
        self.onEnter(self)
    
    # Keyed off menu change from this menu
    def on_leave(self):
        if self.onLeave is None:
            return
        self.onLeave(self)

    # Fired before scrolling occurs
    def on_scroll(self, direction):
        if self.onScroll is None:
            return
        self.onScroll(self, direction)
    
    # Fired before redrawing occurs
    def on_redraw(self):
        if self.onRedraw is None:
            return
        self.onRedraw(self)
        
    # Keyed off index change after scroll 
    def on_select(self):
        if self.onSelect is None:
            return
        self.onSelect(self)
    
    # Called before any input is received and before first draw menu command after startup
    def on_init(self):
        if self.onInit is None:
            return
        self.onInit(self)
    # ***End of Callbacks***

    def draw(self, is_active = False):
        self.on_redraw()
        counter = 0
        # Clear column
        for i in range(self.top_y, self.top_y + self.num_scr_lines):
            writexy(self.x, i, ' ' * self.col_width)
        # Clear decorator if not selected
        if is_active:
            for decorator in self.decorators:
                decorator.draw()
        else:
            for decorator in self.decorators:
                decorator.clear()
        for item in self.items[self.top_index:self.top_index + self.num_scr_lines]:
            
            xpad = self.xpadded - item.decorator_len
            if self.isselectable:
                # If the item is the current selected item and this menu is selected
                if self.index == self.top_index + counter and is_active:
                    # These writexys return the string of the menu item. The item.mci_len is the length
                    # of the string plus color_string length. 
                    writexy(xpad, self.top_y + counter, item.selected[:item.mci_len + self.act_width + item.decorator_len])
                # If the item is the current selected item and this menu is not selected
                elif self.index == self.top_index + counter and not is_active:
                    writexy(xpad, self.top_y + counter, item.highlighted[:item.mci_len + self.act_width])
                # All other items in the menu
                else:
                    writexy(xpad, self.top_y + counter, item.unselected[:item.mci_len + self.act_width])
            else:
                writexy(xpad, self.top_y + counter, item.unselected[:item.raw_mci_len + self.act_width])
            counter = counter + 1

        if self.scrollbar is True:
            self.draw_scroll_bar()

        bbs.write("|16|08")

    def draw_marquee(self, curr_index, is_active=False):
        counter = 0
        for item in self.items[self.top_index:self.top_index + self.num_scr_lines]:
            if self.index == self.top_index + counter and self.isselectable:
                # Check if item can be marqueed (longer than act_width)
                if self.act_width >= len(strip_mci(item.selected)):
                    break

                xpad = self.xpadded - item.decorator_len

                # Check our item_index to see if we need to reset to beginning
                if curr_index > len(strip_mci(item.selected)):
                    curr_index = 0

                text_start = curr_index + item.mci_len + item.decorator_len
                text_end = item.mci_len + self.act_width + item.decorator_len + curr_index
                text_trail = ""
                if self.act_width - len(item.selected[text_start:]) > 0:
                    text_trail = (self.act_width - len(item.selected[text_start:])) * ' '

                writexy(xpad, self.top_y + counter, item.selected[:item.decorator_len + item.mci_len] + \
                    item.selected[text_start:text_end] + text_trail)
                curr_index += 1
            counter = counter + 1

        bbs.write("|16|08")
        return curr_index

    def scroll(self, direction):
        # Call callback before scrolling to give menu chance to populate any fields
        self.on_scroll(direction)

        last_index = len(self.items) - 1
        if direction == ScrollDir.up:
            if self.blockscroll:
                # If there is text above the top of the window, scroll 1 line
                if self.top_index is not 0:
                    self.top_index = self.top_index - 1
                    self.index = self.top_index
            else:
                # If we're at top of screen
                if self.index == self.top_index:
                    # if there are more file groups to scroll
                    if self.index > 0:
                        #cycle top index 1 row
                        self.top_index = self.top_index - 1
                        self.index = self.index - 1
                    elif self.index == 0:
                        if self.wraparound:
                            self.index = last_index
                            # If our file groups count is less than or equal to the available screen lines
                            if last_index <= self.num_scr_lines - 1:
                                self.top_index = 0
                            # We have more fg than screen lines, start at bottom
                            else:
                                self.top_index = last_index - self.num_scr_lines + 1
                # If we're in between bottom up to top, don't scroll, just index 1
                elif self.index < self.top_index + self.num_scr_lines:
                    self.index = self.index - 1
        elif direction == ScrollDir.down:
            if self.blockscroll:
                # If there is text below the bottom of the window, scroll 1 line
                if self.top_index + self.num_scr_lines - 1 < last_index:
                    self.top_index = self.top_index + 1
                    self.index = self.top_index
            else:
                if self.index == self.top_index + self.num_scr_lines - 1:
                    # if there are more items to scroll
                    if self.index < last_index:
                        #cycle top index 1 row
                        self.top_index = self.top_index + 1
                        self.index = self.index + 1
                    elif self.index == last_index:
                        if self.wraparound:
                            self.index = 0
                            self.top_index = 0
                # If we're in between bottom up to top, don't scroll, just index 1
                elif self.index < self.top_index + self.num_scr_lines - 1:
                    if self.index < last_index:
                        self.index = self.index + 1
                    elif self.index == last_index:
                        if self.wraparound:
                            self.index = 0
                            self.top_index = 0
        elif direction == ScrollDir.down_page:
            # If there is a page of text below the bottom of the window, scroll 1 page
            if self.top_index + self.num_scr_lines <= last_index:
                self.top_index += self.num_scr_lines 
                # Check that we can index that far down. If there is not a full page, we got to las
                # index
                if self.index + self.num_scr_lines <= last_index:
                    self.index += self.num_scr_lines 
                else:
                    self.index = last_index
            # If we are on the last page and user pages down, go to last index
            elif self.top_index + self.num_scr_lines - 1 >= last_index:	
                self.index = last_index
        elif direction == ScrollDir.up_page:
            # If there is a page of text above the top of the window, and we're at top of window, scroll 1 page
            if self.top_index - self.num_scr_lines >= 0:
                self.top_index -= self.num_scr_lines 
                self.index -= self.num_scr_lines
            # If there is less than a page of text above the top window, scoll up to top index
            else:
                self.top_index = self.index = 0
        elif direction == ScrollDir.home:
            # Easy, go to top index and reset:
            self.top_index = self.index = 0
        elif direction == ScrollDir.end:
            # Not so easy, need to check our last index vs num_scr_lines
            # If we have more items than will fit in one window
            if last_index > self.num_scr_lines:
                self.index = last_index
                self.top_index = last_index - self.num_scr_lines + 1
            # Otherwise we only have less than one page
            else:
                self.index = last_index
                self.top_index = 0
            pass

    def draw_scroll_bar(self):
        # Clear scrollbar area on redraw
        for i in range (0,self.num_scr_lines):
            writexy(self.x + self.col_width, self.top_y + i, '|16 ')
        # For sanity, we need to make sure we even need a scrollbar
        if len(self.items) <= self.num_scr_lines:
            return

        # Setup scrollbar
        # Top
        scroll_bar = ["|16|08" + chr(179)] * self.num_scr_lines
        # Between top and bottom
        scroll_bar[0] = "|16|08" + chr(194)
        # Bottom 
        scroll_bar[-1] = "|16|08" + chr(193)
        # Indicator charactor
        indicator = "|16|12" + chr(240)

        # Now let's do some math to figure what screen line to put indicator
        # First, let's get the chunk of items each line on the scroll bar represents:
        num_items = float(len(self.items))
        chunk_size = num_items / self.num_scr_lines
        # Next, lets find the index (screen line) of the menu windows the indicator
        # is at.
        scroll_bar_index = int(math.floor(float(self.index) / chunk_size))
        # Apply indicator
        if self.index is -1:
            scroll_bar[0] = indicator
        else:
            scroll_bar[scroll_bar_index] = indicator
        counter = 0
        for item in scroll_bar:
            writexy(self.x+self.col_width, self.top_y+ counter, item)
            counter+=1

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
        string += str(self.__selected_color + strip_mci(self.string))
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
        string += str(self.__highlighted_color + strip_mci(self.string))
        return string

    # actual length of string is the string as rendered + MCI codes. So we need to tell the draw
    # function how long the MCI codes are but differencing the regular and stripped strings
    @property
    def raw_mci_len(self):
        return len(self.string) - len(strip_mci(self.string))

    @property
    def mci_len(self):
        return len(self.selected) - len(strip_mci(self.selected))

    @property
    def decorator_len(self):
        if self.decorator is not None and self.is_active:
            return len(self.decorator.decorator)
        return 0

class ScrollDir(Enum):
    up = 1
    up_block = 2
    down = 3
    down_block = 4
    up_page = 5
    down_page = 6
    home = 7
    end = 8
