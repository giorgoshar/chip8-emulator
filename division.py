def divide_unsigned(N, D):
    Q = 0
    R = N
    while R >= D:
        Q = Q + 1
        R = R - D
    return (Q, R)

def divide(N, D):
    if D == 0: raise ZeroDivisionError
    if D < 0:
        Q, R = divide(N, -D)
        return (-Q, R)

    if N < 0:
        Q, R = divide(-N, D)
        if R == 0: return (-Q, 0)
        else: return (-Q - 1, D - R)

    return divide_unsigned(N, D)

# return result of division, remainder
print(divide(10, 2))
print(divide(10, 3))


def division2(x, y):
    q = 0
    while x >= y:
        a = x >> 1 # x shr 1
        b = y
        counter = 1
        while a >= b:
            b = b << 1 # b shl 1
            counter = counter << 1 # counter shl 1
        x = x - b
        q = q + counter
    return q, x

print(division2(10, 3))