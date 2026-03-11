n = int(input())
words = list(input().split())

longest = max(words, key = len)

print(longest)