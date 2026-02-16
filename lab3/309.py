class Circle:
    def __init__(self, rad):
        self.rad = rad
        
    def area(self):
        return 3.14159 * self.rad * self.rad

r = int(input())
circle = Circle(r)
result = circle.area()
print(f"{result:.2f}")

