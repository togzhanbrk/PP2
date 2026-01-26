sentence = input()
target = input()
replacement = input()

if target in sentence:
    sentence = sentence.replace(target, replacement)


print(sentence)