import math
import numpy as np

def gcd( a, b): 
    if a == 0 : 
        return b 
    
    return gcd(b % a, a)


def is_even(n):
    return n % 2 == 0


def find_order(x, N):
    if x >= N:
        raise Exception("ERROR: x should be smaller than N")

    r = 1
    while r < N + 1:
        if (x**r) % N == 1:
            print("The order of", x, "is:", r, "(where N =", N, ")")
            return r
        r += 1
    print("WARNING: Reached maximum without finding the solution")
    return -1


def find_power_factor(N):
    alpha = math.log2(N)
    L = math.ceil(alpha) # Number of bits
    # print("Number of bits required:", L)

    iteration = 1
    for b in range(2, L):
        # print("%%%%%%%%%%% Iteration:", iteration, "%%%%%%%%%%%")
        iteration += 1
        x = alpha / b
        u = 2**x
        u_1 = math.floor(u)
        u_2 = math.ceil(u)
        u1_b = u_1**b
        u2_b = u_2**b
        #print("b =", b, "x=", x, "u=2^x=", u, "u_1=", u_1, "(u_1)^b=", u1_b, "u_2=", u_2, "(u_2)^b=", u2_b)

        if u1_b == N:
            return u_1, b
        elif u2_b == N:
            return u_2, b
    return -1, -1

def two_module_exponential(a, j, N):
    """
    Compute a^{2^ĵ} (mod N) by repeated squaring
    :param a:
    :param j:
    :param N:
    :return:
    """
    for _ in range(j):
        a = np.mod(a**2, N)
    return a

def module_finding(x, N):
    objective = x % N

    i = 0
    while True:
        if i % N == objective:
            return i
        else:
            i += 1


if __name__ == "__main__":
    N = 15
    a = 7
    # for i in range(7):
    #     print(two_module_exponential(a, i, 15))
    for i in range(0,15):
        print("U|" + str(i) + "> = |" + str(a)  + "x"+ str(i) + "(mod " + str(N) + ")> = |" + str(module_finding(i*a, N)) + ">")
        # print(module_finding(i*a, N))   

    # print(two_module_exponential(4, 1, 15))


