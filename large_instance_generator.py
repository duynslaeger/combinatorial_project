import numpy as np
import pandas as pd

def generate_csv(n, m, filename):

    np.set_printoptions(formatter={'float': '{:.18e}'.format})

    row_zero = np.zeros(m)

    random_rows = np.random.rand(n-1, m)

    instance = np.vstack((row_zero, random_rows))

    df = pd.DataFrame(instance)
    df.to_csv(filename, index=False, header=False, float_format='%.18e')

# Generate the two CSV files
generate_csv(10, 100, 'data/large-mu.csv') # TO DO change n to 1.000.000
generate_csv(10, 100, 'data/large-r.csv') # TO DO change n to 1.000.000
