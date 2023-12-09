from math_func import *
from quantum_order_finding import *
import random


class Shor:

    def __init__(self):
        self.quantum_order_finding = None

    def compute(self, N, epsilon = 1e-3, max_iterations = 20):
        print_title("Shor Algorithm for: " + str(N))

        print_section("Step 1: Checking if N is even...")
        if is_even(N):
            print_correct("N is even! Solution Found!")
            return 2
        else:
            print("Step 1: N is odd. Continue...")
        
        print_section("Step 2: Searching for a so that a^b = N...")
        a, b = find_power_factor(N)
        if a != -1:
            print_correct("Solution Found! a = " + str(a))
            return a
    
        print_section("Step 2: Can't find power numbers such that a^b=N. Continue... ")
        print_section("Step 3: Searching for random factorial k...")
        return self.__search_random(N, max_iterations, epsilon)

    def __search_random(self, N, max_iterations,epsilon):
        iter = 0
        while iter < max_iterations:
            k = random.randint(2, N - 1)
            print("k =", k)

            a = gcd(k, N)
            if a > 1:
                print_correct("You were lucky! k is already a divisor of N")
                return a, N/a
        
            self.quantum_order_finding = QuantumOrderFinding()
            r = self.quantum_order_finding.compute(k, N, epsilon)
            if r != -1:
                k_r_1_2 = k**(r/2)
                if r%2 == 0 and k_r_1_2%N != -1:
                    p = gcd(k_r_1_2-1, N)
                    q = gcd(k_r_1_2 + 1, N)
                    if p * q == N:
                        return p, q
              
            iter += 1
        
        print("Error: Algorithm already reached maximum number of iterations! Modify your parameters")

    def get_measurements_table(self):
        return self.quantum_order_finding.get_measurements_table()
    
    def get_U(self):
        return self.quantum_order_finding.U
    
    def get_quantum_circuit(self):
        return self.quantum_order_finding.quantum_circuit

    









