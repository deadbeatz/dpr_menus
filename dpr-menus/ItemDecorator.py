from . import Utils

class ItemDecorator:
    def __init__(self, decorator, colors):
        self.decorator = decorator
        self.colors = colors

    def draw(self):
        writexy(self.x, self.y, self.colors + self.decorator)
    
    def clear(self):
        writexy(self.x, self.y, ' ' * len(self.decorator))