import sys
import importlib

def main():
    input = sys.stdin.readline
    q = int(input().strip())

    for _ in range(q):
        module_path, attr = input().split()

        try:
            module = importlib.import_module(module_path)
        except Exception:
            print("MODULE_NOT_FOUND")
            continue

        if not hasattr(module, attr):
            print("ATTRIBUTE_NOT_FOUND")
            continue

        obj = getattr(module, attr)

        if callable(obj):
            print("CALLABLE")
        else:
            print("VALUE")

if __name__ == "__main__":
    main()