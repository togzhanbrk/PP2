import sys
import math

EPS = 1e-12
TWOPI = 2.0 * math.pi

def dist_point_to_segment_sq(ax, ay, bx, by):
    """Squared distance from origin (0,0) to segment AB."""
    dx = bx - ax
    dy = by - ay
    dd = dx*dx + dy*dy
    if dd < EPS:
        return ax*ax + ay*ay  
    t = -(ax*dx + ay*dy) / dd
    if t < 0.0:
        x, y = ax, ay
    elif t > 1.0:
        x, y = bx, by
    else:
        x = ax + t*dx
        y = ay + t*dy
    return x*x + y*y

def ang_diff(a, b):
    """Minimal absolute angular distance between angles a and b (radians)."""
    d = (a - b) % TWOPI
    if d > math.pi:
        d = TWOPI - d
    return abs(d)

def main():
    data = sys.stdin.read().strip().split()
    r = float(data[0])
    ax, ay = float(data[1]), float(data[2])
    bx, by = float(data[3]), float(data[4])

    dseg2 = dist_point_to_segment_sq(ax, ay, bx, by)
    straight = math.hypot(bx - ax, by - ay)

    if dseg2 >= r*r - 1e-10:
        print(f"{straight:.10f}")
        return


    da = math.hypot(ax, ay)
    db = math.hypot(bx, by)


    ta_len = math.sqrt(max(0.0, da*da - r*r))
    tb_len = math.sqrt(max(0.0, db*db - r*r))


    angA = math.atan2(ay, ax)
    angB = math.atan2(by, bx)


    gammaA = 0.0 if da <= r + EPS else math.acos(max(-1.0, min(1.0, r / da)))
    gammaB = 0.0 if db <= r + EPS else math.acos(max(-1.0, min(1.0, r / db)))

    best = float("inf")

    for sA in (-1.0, 1.0):
        tA = angA + sA * gammaA  
        for sB in (-1.0, 1.0):
            tB = angB + sB * gammaB
            arc_angle = ang_diff(tA, tB)  
            total = ta_len + tb_len + r * arc_angle
            if total < best:
                best = total

    print(f"{best:.10f}")

if __name__ == "__main__":
    main()