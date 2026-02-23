import sys

def main():
    input = sys.stdin.readline
    q = int(input().strip())

    g = 0
    n = 0

    for _ in range(q):
        scope, value = input().split()
        value = int(value)

        if scope == "global":
            g += value
        elif scope == "nonlocal":
            n += value

    print(g, n)

if __name__ == "__main__":
    main()