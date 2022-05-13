# Ephemerality metric
In [[1]](#1) we formalized the ephemerality metrics used to estimate the healthiness of online discussions. It shows how 'ephemeral' topics are, that is whether the discussions are more or less uniformly active or only revolve around one or several peaks of activity.

### Requirements
The code was tested to work with Python 3.8.6 and Numpy 1.20.3, but is expected to also run on their previous versions.

## How to run the experiments
The code can be run directly via the calculate_ephemerality.py script or via a Docker container built with the provided Dockerfile.

### Input
The script/container expect the following input arguments:

* **Frequency vector file**. The file should contain a vector of numbers in csv format. It does not need to be normalized, if it is not --- it will be done automatically.
* **Output file**. Optional. If it is provided, the results will be written into this file in JSON format.

### Output
The results are printed to STDOUT in **(ε<sub>2</sub>, ε<sub>4</sub>)** format. Additionally, if the output file was specified among the input arguments, the results will also be written into this file in JSON format.

### Example

Input file `test_input.csv`:
```
0.0,0.0,0.0,0.2,0.55,0.0,0.15,0.1,0.0,0.0
```

#### Python execution:

```
python calculate_ephemerality.py ./test_input.csv ./test_output.json
```

Output:
```
0.2, 0.25
```

`test_output.json` content:
```
{"ephemerality2": 0.2, "ephemerality4": 0.25}
```

#### Docker execution
```
docker run -a STDOUT -v [PATH_TO_FOLDER]/tmp/:/tmp/ ephemerality:0.1 /tmp/test_input.csv /tmp/test_output.json
```

Output:
```
0.2, 0.25
```

`test_output.json` content:
```
{"ephemerality2": 0.2, "ephemerality4": 0.25}
```


## References
<a id="1">[1]</a>
Gnatyshak, D., García-Gasulla, D., Alvarez-Napagao, S., Arjona, J., & Venturini, T. (2022). Healthy Twitter discussions? Time will tell. arXiv preprint arXiv:2203.11261
