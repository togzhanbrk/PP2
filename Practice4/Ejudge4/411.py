import json

def apply_patch(source, patch):
    if isinstance(source, dict) and isinstance(patch, dict):
        for key, pval in patch.items():
            if pval is None:
                source.pop(key, None)
            else:
                if key in source and isinstance(source[key], dict) and isinstance(pval, dict):
                    apply_patch(source[key], pval)
                else:
                    source[key] = pval
        return source

    return patch

source = json.loads(input().strip())
patch = json.loads(input().strip())

result = apply_patch(source, patch)

print(json.dumps(result, sort_keys=True, separators=(",", ":")))