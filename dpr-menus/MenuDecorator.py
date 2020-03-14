from .Utils import Utils

class MenuDecorator:
    def __init__(self, x, y, decorator, colors):
        self.x = x
        self.y = y
        self.decorator = decorator
        self.colors = colors

    def draw(self):
        Utils.writexy(self.x, self.y, self.colors + self.decorator)
    
    def clear(self):
        Utils.writexy(self.x, self.y, ' ' * len(self.decorator))