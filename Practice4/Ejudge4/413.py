import sys
import json

def parse_query(q: str):
    """
    Convert query string like: user.friends[2].name
    into tokens: ["user", "friends", 2, "name"]
    """
    tokens = []
    i, n = 0, len(q)

    def read_name():
        nonlocal i
        start = i
        while i < n and (q[i].isalnum() or q[i] == '_' or q[i] == '-'):
            i += 1
        if start == i:
            return None
        return q[start:i]

    while i < n:
        if q[i] == '.':
            i += 1
            name = read_name()
            if name is None:
                return None
            tokens.append(name)

        elif q[i] == '[':
            i += 1
            if i >= n:
                return None
            start = i
            while i < n and q[i].isdigit():
                i += 1
            if start == i:
                return None
            if i >= n or q[i] != ']':
                return None
            idx = int(q[start:i])
            i += 1
            tokens.append(idx)

        else:
            name = read_name()
            if name is None:
                return None
            tokens.append(name)

    return tokens

def resolve(data, tokens):
    cur = data
    for t in tokens:
        if isinstance(t, str):
            if not isinstance(cur, dict) or t not in cur:
                return None, False
            cur = cur[t]
        else:  # int index
            if not isinstance(cur, list):
                return None, False
            if t < 0 or t >= len(cur):
                return None, False
            cur = cur[t]
    return cur, True

def main():
    lines = [line.rstrip("\n") for line in sys.stdin.readlines()]
    if not lines:
        return

    data = json.loads(lines[0].strip())
    q = int(lines[1].strip())

    out = []
    for k in range(q):
        query = lines[2 + k].strip()
        tokens = parse_query(query)
        if tokens is None:
            out.append("NOT_FOUND")
            continue

        value, ok = resolve(data, tokens)
        if not ok:
            out.append("NOT_FOUND")
        else:
            out.append(json.dumps(value, ensure_ascii=False, separators=(',', ':')))
    print("\n".join(out))

if __name__ == "__main__":
    main()