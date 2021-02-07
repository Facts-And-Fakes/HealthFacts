def factorial(x):
    if x == 1:
        return 1
    return x*factorial(x-1)


for i in range(int(input())):
    n = int(input())
    pairs = 0
    words = list(map(str, input().split()))
    first_letters = set()
    for word in words:
        first_letters.add(list(word)[0])

    print((factorial(len(first_letters))/(factorial(2)*factorial(len(first_letters)-2))))


