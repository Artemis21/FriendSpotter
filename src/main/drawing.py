from random import randrange
from PIL import Image, ImageDraw


class Graph:
    def __init__(self, points, width=500, height=500, loops=100):
        self.points = points
        self.width = width
        self.height = height
        self.nodes = {}
        self.edges = {}
        self.image = Image.new('RGB', (width, height))
        self.setup()
        for _ in range(loops):
            self.move()
        self.draw()

    def get_point(self):
        return randrange(50, self.width-50), randrange(50, self.height-50)

    def setup(self):
        for a, b, value in self.points.data.values():
            if a.name not in self.nodes:
                self.nodes[a.name] = self.get_point()
                self.edges[a.name] = {}
            if b.name not in self.nodes:
                self.nodes[b.name] = self.get_point()
            self.edges[a.name][b.name] = value

    def move(self):
        pass
        # adjust positions based on attractive forces in edges and a constant
        # relpusive force between every node, with a limited field size

    def draw(self):
        im = ImageDraw.Draw(self.image)
        # draw nodes
        for elem in self.nodes:
            x, y = self.nodes[elem]
            im.ellipse(((x-5, y-5), (x+5, y+5)), fill=(255, 0, 0, 255))
            im.text((x, y), elem)
        # find points -> width scale
        widths = []
        for a in self.edges:
            for b in self.edges[a]:
                widths.append(self.edges[a][b])
        mult = 5 / max(widths)
        # draw lines
        for node_a in self.edges:
            for node_b in self.edges[node_a]:
                xa, ya = self.nodes[node_a]
                xb, yb = self.nodes[node_b]
                width = int(mult * self.edges[node_a][node_b])
                im.line((xa, ya, xb, yb), width=width)
    
