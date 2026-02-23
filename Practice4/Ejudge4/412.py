import sys
import json

MISSING = object()

def to_compact_json(value):
    """Serialize a JSON value as compact JSON, or <missing> for absent side."""
    if value is MISSING:
        return "<missing>"
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), sort_keys=True)

def deep_diff(a, b):
    diffs = []

    def walk(path, v1, v2):
        if isinstance(v1, dict) and isinstance(v2, dict):
            keys = set(v1.keys()) | set(v2.keys())
            for k in keys:
                new_path = f"{path}.{k}" if path else k
                if k not in v1:
                    diffs.append((new_path, MISSING, v2[k]))
                elif k not in v2:
                    diffs.append((new_path, v1[k], MISSING))
                else:
                    walk(new_path, v1[k], v2[k])
            return

        if v1 != v2:
            diffs.append((path, v1, v2))

    walk("", a, b)
    return diffs

def main():
    lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip() != ""]
    obj1 = json.loads(lines[0])
    obj2 = json.loads(lines[1])

    diffs = deep_diff(obj1, obj2)
    if not diffs:
        print("No differences")
        return

    diffs.sort(key=lambda x: x[0])  
    for path, old_val, new_val in diffs:
        print(f"{path} : {to_compact_json(old_val)} -> {to_compact_json(new_val)}")

if __name__ == "__main__":
    main()