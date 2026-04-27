x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

x_reflect = x1 + y1 * (x2 - x1) / (y1 + y2)
y_reflect = 0.0

print(f"{x_reflect:.10f} {y_reflect:.10f}")