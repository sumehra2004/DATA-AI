'''def power(a, b):
    if a == 1 or b == 0:
        return 1
    if b == 1:
        return a
    return a * power(a, b - 1)

a, b = 2, 3
print(power(a, b))'''


def isprime(n, i=2):
    if n <= 1:
        return False
    if i * i > n:
        return True
    if n % i == 0:
        return False
    return isprime(n, i + 1)


num = 7
print(isprime(num))

   