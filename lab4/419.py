import math

r = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

def distance(xa, ya, xb, yb):
    return math.hypot(xb - xa, yb - ya)

def segment_intersects_circle(r, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    a = dx*dx + dy*dy
    b = 2*(x1*dx + y1*dy)
    c = x1*x1 + y1*y1 - r*r
    disc = b*b - 4*a*c
    if disc < 0:
        return False
    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc)/(2*a)
    t2 = (-b + sqrt_disc)/(2*a)
    return 0 <= t1 <= 1 or 0 <= t2 <= 1

if not segment_intersects_circle(r, x1, y1, x2, y2):
    print("{:.10f}".format(distance(x1, y1, x2, y2)))
else:
    d1 = distance(0,0,x1,y1)
    d2 = distance(0,0,x2,y2)

    alpha1 = math.acos(r / d1)
    alpha2 = math.acos(r / d2)

    angle1 = math.atan2(y1, x1)
    angle2 = math.atan2(y2, x2)

    theta = abs(angle2 - angle1)
    if theta > math.pi:
        theta = 2*math.pi - theta

    arc_length = r * (theta - alpha1 - alpha2)
    tangent1 = math.sqrt(d1*d1 - r*r)
    tangent2 = math.sqrt(d2*d2 - r*r)

    total_length = tangent1 + tangent2 + arc_length
    print("{:.10f}".format(total_length))