import sys
import json
import numpy as np
from src import compute_ephemerality_measures


if __name__ == '__main__':
    frequency_vector_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(frequency_vector_file, 'r') as f:
        frequency_vector = np.array(f.read().split(','), dtype=float)

    ephemeralities = compute_ephemerality_measures(frequency_vector=frequency_vector,
                                                   threshold=0.8)

    with open(output_file, 'w+') as f:
        json.dump(ephemeralities, f)
