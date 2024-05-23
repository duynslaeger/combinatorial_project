import numpy as np
import pandas as pd

def generate_csv(n, m, filename):

    np.set_printoptions(formatter={'float': '{:.18e}'.format})

    row_zero = np.zeros((1, m))
    matrix_instance = []

    for _ in range(m):
        # loop sur toute une column
    
        # Generate a list of unique floating-point values
        values = set()
        
        while len(values) < n:
            new_values = np.random.uniform(1e-10, 1.0, n - len(values))
            values.update(new_values)
        
        unique_values = sorted(values, reverse=True)
        matrix_instance.append(unique_values)

    matrix_instance = np.array(matrix_instance)
    
    # Add the row_zero horizontally to the matrix_instance
    instance = np.vstack((row_zero, matrix_instance.T))
    df = pd.DataFrame(instance)
    df.to_csv(filename, index=False, header=False, float_format='%.18e', sep=";")

# Generate the two CSV files
generate_csv(1000000, 100, 'data/large-mu.csv') # TO DO change n to 1.000.000
generate_csv(1000000, 100, 'data/large-r.csv') # TO DO change n to 1.000.000
