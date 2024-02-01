import math

class SphericalCoordinate:

    def __init__(self, rho, theta, phi):
        self.rho = rho
        self.theta = theta
        self.phi = phi

    def __repr__(self):
        return f"SphericalCoordinate({self.rho}, {self.theta}, {self.phi})"

    def __str__(self):
        return self.__repr__()

    def to_rectangular(self):
        x = self.rho * math.sin(self.theta) * math.cos(self.phi)
        y = self.rho * math.sin(self.theta) * math.sin(self.phi)
        z = self.rho * math.cos(self.theta)
        return RectangularCoordinate(x, y, z)

class RectangularCoordinate:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def normalize(self):
        magnitude = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        self.x /= magnitude
        self.y /= magnitude
        self.z /= magnitude

    def __repr__(self):
        return f"RectangularCoordinate({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return self.__repr__()
    

    