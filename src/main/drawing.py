from random import randrange
import math
from PIL import Image, ImageDraw, ImageFont


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def get_edge(self, node_a, node_b):
        for key in self.edges:
            if node_a in key and node_b in key:
                return key, self.edges[key]
        return (node_a, node_b), 0

    def add_node(self, name, x, y):
        self.nodes[name] = [x, y]

    def bond(self, node_a, node_b, amt):
        key, old = self.get_edge(node_a, node_b)
        self.edges[key] = old + amt

    def distance(self, node_a, node_b):
        xa, ya = self.nodes[node_a]
        xb, yb = self.nodes[node_b]
        xdist = xa - xb
        ydist = ya - yb
        return math.sqrt((xdist ** 2 + ydist ** 2))

    def move(self, node_p, node_q, force, new):
        xp, yp = self.nodes[node_p]
        xq, yq = self.nodes[node_q]
        xdist = xp - xq
        ydist = yp - yq
        c = force / 10
        a2b2 = c ** 2
        unit = a2b2 / (xdist + ydist)
        sign = ((force > 0) * 2) - 1
        a = (abs(unit * xdist) ** 0.5) * sign
        b = (abs(unit * ydist) ** 0.5) * sign
        if xp > xq:
            dxp, dxq = -a, a
        else:
            dxp, dxq = a, -a
        if yp > xp:
            dyp, dyq = -b, b
        else:
            dyp, dyq = b, -b
        new[node_p][0] += dxp
        new[node_p][1] += dyp
        new[node_q][0] += dxq
        new[node_q][1] += dyq
        for node in (node_p, node_q):
            for c in (0, 1):
                if new[node][c] > 950:
                    new[node][c] = 950
                elif new[node][c] < 50:
                    new[node][c] = 50

    def update(self):
        k = 10
        new = dict(self.nodes)
        # repulsive force
        for node in self.nodes:
            for other in self.nodes:
                if node != other:
                    dist = self.distance(node, other)
                    if dist > 250:
                        continue
                    force = k ** 4 / -dist
                    self.move(node, other, force, new)
        # attractive force
        maxval = max(self.edges.values())
        for edge in self.edges:
            val = self.edges[edge]
            node_a, node_b = edge
            dist = self.distance(node_a, node_b)
            force = (val / maxval) * (dist ** 2 / k ** 3)
            self.move(node_a, node_b, force, new)
        self.nodes = new


class Drawing:
    def __init__(self, points, width=1000, height=1000, loops=100):
        self.points = points
        self.width = width
        self.height = height
        self.graph = Graph()
        self.font = ImageFont.truetype('config/font.ttf', 30)
        self.image = Image.new('RGB', (width, height), (0, 0, 0, 0))
        self.setup()
        for _ in range(loops):
            self.graph.update()
        self.draw()

    def get_point(self):
        qw = self.width // 4
        qh = self.height // 5
        return randrange(qw, self.width-qw), randrange(qh, self.height-qh)

    def setup(self):
        for a, b, value in self.points.data.values():
            a, b = a.name, b.name
            if a not in self.graph.nodes:
                self.graph.add_node(a, *self.get_point())
            if b not in self.graph.nodes:
                self.graph.add_node(b, *self.get_point())
            self.graph.bond(a, b, value)

    def draw(self):
        im = ImageDraw.Draw(self.image)
        # find points -> width scale
        mult = 5 / max(map(math.log, self.graph.edges.values()))
        # draw lines
        for node_a, node_b in self.graph.edges:
            xa, ya = self.graph.nodes[node_a]
            xb, yb = self.graph.nodes[node_b]
            width = int(mult * math.log(self.graph.edges[node_a, node_b]))
            im.line((xa, ya, xb, yb), width=width, fill=(114, 137, 218, 255))
        # draw nodes
        for elem in self.graph.nodes:
            x, y = self.graph.nodes[elem]
            im.ellipse(((x-5, y-5), (x+5, y+5)), fill=(153, 170, 181, 255))
            im.text((x, y), elem, font=self.font)
    
