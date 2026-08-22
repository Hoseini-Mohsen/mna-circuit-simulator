import numpy as np

def solve_circuit(G_matrix, I_vector):
    G = np.array(G_matrix)
    I = np.array(I_vector)
    try:
        x = np.linalg.solve(G, I)
        return x.tolist()  # Convert the result back to a list
    except np.linalg.LinAlgError as e:
        raise ValueError("The circuit cannot be solved. The G_matrix may be singular.") from e
