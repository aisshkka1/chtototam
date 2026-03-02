import math

# Read input
r = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

# Vector from A to B
dx = x2 - x1
dy = y2 - y1

# Quadratic coefficients for intersection with circle x^2 + y^2 = r^2
a = dx*dx + dy*dy
b = 2*(dx*x1 + dy*y1)
c = x1*x1 + y1*y1 - r*r

discriminant = b*b - 4*a*c

if discriminant < 0:
    # No intersection
    length_inside = 0.0
else:
    sqrt_disc = math.sqrt(discriminant)
    t1 = (-b - sqrt_disc) / (2*a)
    t2 = (-b + sqrt_disc) / (2*a)
    
    # Clip t values to [0,1] segment
    t_enter = max(0, min(t1, t2))
    t_exit = min(1, max(t1, t2))
    
    if t_enter > t_exit:
        length_inside = 0.0
    else:
        segment_length = math.hypot(dx, dy)
        length_inside = (t_exit - t_enter) * segment_length

print(f"{length_inside:.10f}")