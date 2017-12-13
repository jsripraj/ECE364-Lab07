class Rectangle:
    def __init__(self, llPoint, urPoint):
        xll, yll = llPoint
        xur, yur = urPoint
        if xll >= xur or yll >= yur:
            raise ValueError("Lower-Left point must be less than Upper-Right point.")
        self.lowerLeft = llPoint
        self.upperRight = urPoint
    def isSquare(self):
        xll, yll = self.lowerLeft
        xur, yur = self.upperRight
        if xur - xll == yur - yll:
            return True
        return False
    def isPointInside(self, point):
        x, y = point
        xll, yll = self.lowerLeft
        xur, yur = self.upperRight
        if x > xll and x < xur and y > yll and y < yur:
            return True
        return False
    def intersectsWith(self, rect):
        xll, yll = rect.lowerLeft
        xur, yur = rect.upperRight
        if self.isPointInside(rect.lowerLeft) or self.isPointInside(rect.upperRight) \
                or self.isPointInside((xll, yur)) or self.isPointInside((xur, yll)):
            return True
        return False

if __name__ == "__main__":
    r = Rectangle((-2,-2),(2,2))
    # r.isPointInside((0,-4))
    r2 = Rectangle((-1,-2), (4,1))
    print(r.intersectsWith(r2))