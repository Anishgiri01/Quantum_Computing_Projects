#!/usr/bin/env python
# coding: utf-8

# In[1]:


from qiskit import QuantumCircuit, transpile, Aer, execute
from qiskit.visualization import plot_histogram
from math import gcd
from numpy.random import randint
import numpy as np
import fractions

# Define the QFT function
def qft(n):
    """Creates an n-qubit QFT circuit"""
    circuit = QuantumCircuit(n)
    def swap_registers(circuit, n):
        for qubit in range(n//2):
            circuit.swap(qubit, n-qubit-1)
        return circuit
    def qft_rotations(circuit, n):
        """Performs qft on the first n qubits in circuit (without swaps)"""
        if n == 0:
            return circuit
        n -= 1
        circuit.h(n)
        for qubit in range(n):
            circuit.cp(np.pi/2**(n-qubit), qubit, n)
        qft_rotations(circuit, n)

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

# Get the period from the counts
def get_period(counts):
    # Get the key with the maximum count. This is the period.
    period = max(counts, key=counts.get)
    # Convert to decimal
    period = int(period, 2)
    return period

# Calculate factors
def calculate_factors(N, period, a):
    # If the period is even, we can calculate the factors
    if period % 2 != 0:
        period *= 2
    if period % 2 == 0:
        x = pow(a, period // 2, N)
        if x != 1 and x != N - 1:
            p = gcd(x + 1, N)
            q = gcd(x - 1, N)
            if p * q == N:  # Check if the factors are correct
                return p, q
    # If the period is odd or factors are not correct, return None
    return None

n_count = 8
N = 15  # number to factorize
attempts = 0  # number of attempts made
factors = None

while factors is None and attempts < N:
    a = randint(2, N)  # choose a random a < N
    while gcd(a, N) != 1:  # ensure a is coprime with N
        a = randint(2, N)
    qc = QuantumCircuit(n_count + 1, n_count)
    for q in range(n_count):
        qc.h(q)
    qc.x(n_count)

    for q in range(n_count):
        for _ in range(2**q):
            qc.cp(2*np.pi*a/(2**n_count), n_count-q-1, n_count)

    qc.append(qft(n_count).inverse(), range(n_count))

    qc.measure(range(n_count), range(n_count))

    # Simulate and get results
    backend = Aer.get_backend('qasm_simulator')
    results = execute(qc, backend, shots=1024).result()
    counts = results.get_counts()

    period = get_period(counts)
    factors = calculate_factors(N, period, a)
    attempts += 1
    
    
    if factors is None:
        print("Could not determine factors after", attempts, "attempts.")
    else:
        print("Factors are ", factors)

