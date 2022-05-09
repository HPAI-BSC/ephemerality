import sys
import json
from src import compute_ephemerality_measures


if __name__ == '__main__':
    frequency_vector = sys.argv[1]
    output_file = sys.argv[2]

    ephemeralities = compute_ephemerality_measures(frequency_vector=frequency_vector,
                                                   threshold=0.8)

    with open(output_file, 'w+') as f:
        json.dump(ephemeralities, f)
