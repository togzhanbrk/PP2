import sys

def main():
    ax, ay = map(float, sys.stdin.readline().split())
    bx, by = map(float, sys.stdin.readline().split())

    t = ay / (ay + by)

    x = ax + (bx - ax) * t
    y = 0.0

    print(f"{x:.10f} {y:.10f}")

if __name__ == "__main__":
    main()