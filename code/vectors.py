from math import sqrt, cos, sin, pi

class Vct:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __add__(self, other):
        if isinstance(other, Vct):
            return Vct(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple):
            return Vct(self.x + other[0], self.y + other[1])

    def __mul__(self, n):
        return Vct(self.x * n, self.y * n)

    def __div__(self, n):
        return Vct(self.x / n, self.y / n)

    def __rmul__(self, n):
        return self*n

    def __sub__(self, other):
        if isinstance(other, Vct):
            return Vct(self.x - other.x, self.y - other.y)
        if isinstance(other, tuple):
            return Vct(self.x - other[0], self.y - other[1])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
            
    def norm(self):
        c = sqrt((self.x ** 2) + (self.y ** 2))
        if c > 0:
            return Vct(self.x / c, self.y / c)
        else:
            return Vct(0, 1)


    def mag(self):
        return sqrt((self.x ** 2) + (self.y ** 2))

    def rotate(self, angle):
        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)
        return(Vct(x, y))

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __getitem__(self, key): # self[key]
        return (self.x, self.y)[key]

    def int_tuple(self):
        return (int(self.x), int(self.y))

    def copy(self):
        return Vct(self.x, self.y)

    def fromTuple(t):
        return Vct(t[0], t[1])
