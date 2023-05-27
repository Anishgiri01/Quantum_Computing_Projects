#!/usr/bin/env python
# coding: utf-8

# In[31]:


from qiskit import * # import everything
import numpy as np

def create_oracle(circuit, element, element_list):    #oracle knows where the element is, but it is not known outside.
    # Determine the number of qubits based on the length of the element_list
    num_qubits = len(element_list).bit_length() #The .bit_length() method is a built-in Python method that 
                                                #returns the number of bits required to represent an integer in binary

    # Find the index of the element in the element_list
    marked_index = [i for i, e in enumerate(element_list) if e == element]

    # Apply X gates to the indices of the marked element
    for index in marked_index:
        binary_str = bin(index)[2:].zfill(num_qubits) #bin(index) converts the integer index to a binary string. 
                                                      #zfill() function pads the string on the left with zeros ('0') 
                                                      #until the string's length is equal to the num_qubits. This ensures that 
                                                      #the binary string has the same length as the number of qubits.  
        for i in range(num_qubits):
            if binary_str[i] == '0':
                circuit.x(num_qubits - i - 1)

    # Apply multi-controlled-Z gate
    circuit.h(num_qubits - 1)
    circuit.mct(list(range(num_qubits - 1)), num_qubits - 1)
    circuit.h(num_qubits - 1)

    # Apply X gates again to the indices of the marked element
    for index in marked_index:
        binary_str = bin(index)[2:].zfill(num_qubits)
        for i in range(num_qubits):
            if binary_str[i] == '0':
                circuit.x(num_qubits - i - 1)

def create_diffuser(circuit, num_qubits):
    # Apply Hadamard gates to all qubits
    circuit.h(range(num_qubits))

    # Apply X gates to all qubits
    circuit.x(range(num_qubits))

    # Apply multi-controlled-Z gate
    circuit.h(num_qubits - 1)
    circuit.mct(list(range(num_qubits - 1)), num_qubits - 1)
    circuit.h(num_qubits - 1)

    # Uncompute X gates
    circuit.x(range(num_qubits))

    # Uncompute Hadamard gates
    circuit.h(range(num_qubits))

def grover_search(element_list, element):
    num_elements = len(element_list)
    num_qubits = num_elements.bit_length()

    # Create the quantum circuit
    qr = QuantumRegister(num_qubits, 'q')
    cr = ClassicalRegister(num_qubits, 'c')
    circuit = QuantumCircuit(qr, cr)

    # Apply Hadamard gates to all qubits
    circuit.h(range(num_qubits))

    # Define the number of iterations to perform
    iterations = int(np.floor(np.pi / 4 * np.sqrt(num_elements)))

    # Apply Grover's search iterations
    for _ in range(iterations):
        # Create the oracle
        create_oracle(circuit, element, element_list)

        # Create the diffusion operator
        create_diffuser(circuit, num_qubits)

    # Measure the qubits and return the result
    circuit.measure(range(num_qubits), range(num_qubits))
    backend = Aer.get_backend('qasm_simulator')
    counts = execute(circuit, backend, shots=1024).result().get_counts()
    index = int(max(counts, key=counts.get), 2)
    
    return index

# Example usage
element_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O','P','Q','R', 'S'] #does not have to be sorted.
element = 'O'
index = grover_search(element_list, element)
print(f"The index of '{element}' in the list is: {index}")







