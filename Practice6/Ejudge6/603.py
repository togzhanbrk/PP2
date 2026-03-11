number_of_words = int(input())

words = list(input().split())

for index, word in enumerate(words):
    print(f"{index}:{word} ", end = "")