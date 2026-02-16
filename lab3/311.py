class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def add(self, other):
        self.a+=new_a
        self.b+=new_b
        return self.a + other.a, self.b + other.b


a, b, c, d = map(int, input().split())
pair1 = Pair(a1, b1)
pair2 = Pair(a2, b2)

result = pair1.add(pair2)

print(f"Result: {result[0]} {result[1]}")




