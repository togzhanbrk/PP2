import sys
import math

def dot(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2

def inside_len(r, ax, ay, bx, by):
    dx = bx - ax
    dy = by - ay
    seg_len = math.hypot(dx, dy)
    if seg_len == 0.0:
        return 0.0 if ax * ax + ay * ay > r * r else 0.0


    a = dot(dx, dy, dx, dy)         
    b = 2.0 * dot(ax, ay, dx, dy)     
    c = dot(ax, ay, ax, ay) - r * r         

    disc = b * b - 4.0 * a * c

    if disc < 0.0:
        return seg_len if (ax * ax + ay * ay) <= r * r else 0.0

    sqrt_disc = math.sqrt(max(0.0, disc))
    t1 = (-b - sqrt_disc) / (2.0 * a)
    t2 = (-b + sqrt_disc) / (2.0 * a)
    if t1 > t2:
        t1, t2 = t2, t1

    left = max(0.0, t1)
    right = min(1.0, t2)
    if right <= left:
        return 0.0

    return seg_len * (right - left)

def main():
    data = sys.stdin.read().strip().split()
    r = float(data[0])
    ax, ay = float(data[1]), float(data[2])
    bx, by = float(data[3]), float(data[4])

    ans = inside_len(r, ax, ay, bx, by)
    print(f"{ans:.10f}")

if __name__ == "__main__":
    main()