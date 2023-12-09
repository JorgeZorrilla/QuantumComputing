from qiskit import QuantumCircuit, Aer, transpile
from qiskit.quantum_info.operators import Operator
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, Estimator, Options

from fractions import Fraction
import pandas as pd
import matplotlib.pyplot as plt
from math_func import *
from utils import *


class QuantumOrderFinding:

    def __init__(self) -> None:
        self.results = None
        self.U = None
        self.quantum_circuit = None
        self.t = 0
        
        pass

    def compute(self, a, N, eps = 0.0001):
        """
        Compute the order r of K with respect to N using a Quantum Period Finding Subroutine
        :param x:
        :param N:
        :return: Order r such that N%(x^r)=1
        """
        print_title("Calling Quantum Order Finding Algorithm")
        t, L = self.__compute_required_qubits(N, eps)
        print("Required qubits in the first register for N=", N, "and eps=", eps, "is equal to t=", t)
        print("Number of qubits to specificy N=", N, " is L=", L)

        self.t = t

        self.U = self.__create_operator(a, N, L)

        self.quantum_circuit = self.__setup_quantum_circuit(t, L, self.U, False)
      
        self.results = self.__simulate(self.quantum_circuit)

        return self.__find_period(N, a, t)

        # self.__analyze_results(results, t)

    def __find_period(self, N, a, t):
        for output in self.results:
            decimal = int(output, 2)  # Convert (base 2) string to decimal
            phase = decimal/(2**t)  # Find corresponding eigenvalue
            frac = Fraction(phase).limit_denominator(15)
            r = frac.denominator
            if (a**r) % N == 1:

                print("r =", r)
                return r
        print_error("Period r not found! Modify the precision parameters...")
        return -1
    
    def get_measurements_table(self):
            
        plot_histogram(self.results)
        rows = []
        for output in self.results:
            decimal = int(output, 2)  # Convert (base 2) string to decimal
            phase = decimal/(2**self.t)  # Find corresponding eigenvalue
            frac = Fraction(phase).limit_denominator(15)

            row = [output, decimal, phase, f"{frac.numerator}/{frac.denominator}", frac.denominator ]
            rows.append(row)
        
        # Print the rows in a table
        headers=["Register Output(bin)", "Register Output(dec)", "Phase", "Fraction", "r"]
        df = pd.DataFrame(rows, columns=headers)
        return df



    def __analyze_results(self, results, t):
        probs = [results[output] for output in results]
        total_counts = sum(probs)

        rows, measured_phases = [], []
        probs = []
        for output in results:
            probability = results[output]/total_counts
            decimal = int(output, 2)  # Convert (base 2) string to decimal
            phase = decimal/(2**t)  # Find corresponding eigenvalue
            measured_phases.append(phase)
            # Add these values to the rows in our table:
            rows.append([probability,
                        f"{output}(bin) = {decimal:>3}(dec)",
                        f"{decimal}/{2**t} = {phase:.2f}"])
        # Print the rows in a table
        headers=["Prob","Register Output", "Phase"]
        df = pd.DataFrame(rows, columns=headers)
        print(df)

        print("TOTAL:", df['Prob'].sum())
        
        rows = []
        for phase in measured_phases:
            frac = Fraction(phase).limit_denominator(15)
            rows.append([phase,
                        f"{frac.numerator}/{frac.denominator}",
                        frac.denominator])
        # Print as a table
        headers=["Phase", "Fraction", "Guess for r"]
        df = pd.DataFrame(rows, columns=headers)
        print(df)
   
    def __simulate(self, circuit, ibm=False, plot= False):
        print("Simulating...")
        if ibm:
            service = QiskitRuntimeService()
            backend = service.backend("ibm_brisbane")

            estimator = Estimator(backend=backend)
            job = estimator.run(circuit, observables = [""])
            print(f">>> Job ID: {job.job_id()}")
            print(f">>> Job Status: {job.status()}")

            result = job.result()
            print(f">>> {result}")
            print(f"  > Expectation value: {result.values[0]}")
            print(f"  > Metadata: {result.metadata[0]}")
        else:
            aer_sim = Aer.get_backend('aer_simulator')
            t_qc = transpile(circuit, aer_sim)
            result = aer_sim.run(t_qc).result().get_counts()
        if plot:
            plot_histogram(result)
            plt.show()
        print("Simulation finished!")
        return result

    def __create_operator(self, a, N, L):
        n_bits = 2**L
        U = np.zeros((n_bits, n_bits))
        for column in range(n_bits):
            row = module_finding(a * column, N) if column >= 0 and column <= (N -1) else column
            U[row, column] = 1

        return Operator(U)

    def __setup_quantum_circuit(self, t, L, U, plot = False):
        print("Creating the quantum circuit...")
        # Init circuit
        circuit = QuantumCircuit(t + L, t)
        for i in range(t):
            circuit.h(i)
        circuit.x(t) # Init in state 1

        # Controlled-U operations
        for q in range(t):
            index = [q] + [i for i in range(t, t +L)]
            circuit.append(self.__create_u_gate(U, q), index)

        #Compute inverse-QFT
        circuit.append(self.__qft_dagger(t), range(t))

        # Measure circuit
        circuit.measure(range(t), range(t))
        
        print("Quantum circuit completed!")
        if plot:
            print(circuit)
            self.draw_circuit(circuit)

        return circuit
    
    def __create_u_gate(self, U, power):
        iterator = 2**power
        result = U.power(iterator)
      
        gate = QuantumCircuit(U.num_qubits)
        gate.append(result, range(U.num_qubits))
        gate = gate.to_gate().control()
        gate.base_gate.name = "U^{2^{" + str(power) + "}}"
        return gate
 

    def __compute_required_qubits(self, n, eps):
        return math.ceil(math.log2(n) + math.log2(2 + 1/(2 * eps))), math.ceil(math.log2(n))

    def draw_circuit(self, circuit=None):
        if not circuit:
            circuit = self.quantum_circuit
        print(circuit)
        # circuit.draw('mpl')
        # plt.show()

    def __qft_dagger(self, n):
        """n-qubit QFTdagger the first n qubits in circ"""
        qc = QuantumCircuit(n)
        # Don't forget the Swaps!
        for qubit in range(n//2):
            qc.swap(qubit, n-qubit-1)
        for j in range(n):
            for m in range(j):
                qc.cp(-np.pi/float(2**(j-m)), m, j)
            qc.h(j)
        qc.name = "QFT†"
        return qc
    
   
if __name__ == "__main__":
    eps = 0.0001
    a = 5
    N = 21
    QRO = QuantumOrderFinding()
    result = QRO.compute(a, N, eps)

    QRO.draw_circuit()
