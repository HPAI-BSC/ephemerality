# Ephemerality metric
In [[1]](#1) we formalized the ephemerality metrics used to estimate the healthiness of online discussions. It shows how
'ephemeral' topics are, that is whether the discussions are more or less uniformly active or only revolve around one or
several peaks of activity.

We defined 3 versions of ephemerality: original, filtered, and sorted. Let us suppose we have a discussion that we can divide in $N$ bins of equal time length and for each bin we can calculate activity in that time period (e.g. number of tweets, watches, visits etc.). Let $t$ denote a normalized vector of frequency corresponding to this discussion, $t_i$ corresponds to normalized activity in during time bin $i$. Let $\alpha\in\left[0, 1\right)$ denote a parameter showing which portion of activity we consider to be the "core" activity. Then we can define ephemerality as a normalized portion of $t$ that contains the remaining $1-\alpha$ activity. We can interpret this defenition in three slightly different ways depending on what we consider to be the core activity:

1. **Original ephemerality**. We calculate core activity as the minimal portion of $t$ starting from the beginning of the vector that contains at least $\alpha$ of the total activity (which is 1 in case of normalized $t$). Then the ephemerality formula can be computed as follows:

$$
\varepsilon_{orig}\left(t_i\right) = 1 - \frac1\alpha \frac{\arg\min_{m\in [1,N]}: \left( \sum_{i=1\dots m} t_i \right) \ge \alpha}{N}
$$

2. **Filtered ephemerality**. We calculate core activity the minimal *central* portion of $t$ that contains at least $\alpha$ of the total activity. For that we exclude portions of $t$ from the beginning and the end of $t$, so that the sum of each of these portions is as close to $\frac{1-\alpha}{2}$ as possible without reaching it:

$$
\varepsilon_{filt}\left(t_i\right) = 1 - \frac1\alpha \frac{\arg\min_{m\in [1,N]}: \left( \sum_{i=1\dots m} t_i - \max_{p\in [1,N]}: \left( \sum_{j=1\dots p} t_j \right) < \frac{1-\alpha}{2} \right) \ge \alpha}{N}
$$

3. **Sorted ephemerality**. Finally, we can define the core activity as the minimal number of time bins that cover $\alpha$ portion of the activity. For that we sort $t$ components in descending order (denoted as $\widehat{t}$) and then apply the formula of original ephemerality:

$$
\varepsilon_{sort}\left(t_i\right) = 1 - \frac1\alpha \frac{\arg\min_{m\in [1,N]}: \left( \sum_{i=1\dots m} \widehat{t}_i \right) \ge \alpha}{N}
$$

## Requirements
The code was tested to work with Python 3.8.6 and Numpy 1.21.5, but is expected to also run on their older versions.

## How to run the experiments
The code can be run directly via the calculate_ephemerality.py script or via a Docker container built with the provided
Dockerfile.

### Input
The script/container expect the following input arguments:

* **Frequency vector file**. `[-i PATH, --input PATH]` _Optional_. Path to a file containing one or several arrays of 
numbers in csv format (one array per line), representing temporal frequency vectors. They do not need to be normalized:
if they are not --- they will be normalized automatically.
* **Frequency vector**. _Optional_. If input file is not provided, a frequency vector is expected as a positional 
argument (either comma- or space-separated). 
* **Output file**. `[-o PATH, --output PATH]` _Optional_. If it is provided, the results will be written into this file
in JSON format.
* **Threshold**. `[-t FLOAT, -threshold FLOAT]` _Optional_. Threshold value for ephemerality computations. Defaults 
to 0.8.
* **Print**. `[-p, --print]`. _Optional_. If output file is provided, forces the results to still be printed to stdout.

### Output
If no output file specified or `-p` option is used, results are printed to STDOUT in [
$\varepsilon_{orig}$ ␣
span( $\varepsilon_{orig}$ ) ␣
$\varepsilon_{filt}$ ␣
span( $\varepsilon_{filt}$ ) ␣
$\varepsilon_{sort}$ ␣
span( $\varepsilon_{sort}$ )
] format, one line per each line of input file (or a single line for command line input).

If the output file was specified among the input arguments, the results will be written into that file in JSON format as 
a list of dictionaries, one per input line:

```
[
  {
    "ephemerality_original": FLOAT,
    "ephemerality_original_span": INT,
    "ephemerality_filtered": FLOAT,
    "ephemerality_filtered_span": INT,
    "ephemerality_sorted": FLOAT,
    "ephemerality_sorted_span": INT
  },
  ...
]
```

### Example

Input file `test_input.csv`:
```
0.0,0.0,0.0,0.2,0.55,0.0,0.15,0.1,0.0,0.0
0,1,1.,0.0,.0
```

#### Python execution:

Input 1:

```
python ephemerality.py -i tmp/test_input.csv -t 0.8 --output tmp/test_output.json -P
```

Output 1:
```
0.1250000000000001 7 0.5 4 0.625 3
0.2500000000000001 3 0.5 2 0.5 2
```

`test_output.json` content:
```
[
  {
    "ephemerality_original": 0.1250000000000001,
    "ephemerality_original_span": 7,
    "ephemerality_filtered": 0.5,
    "ephemerality_filtered_span": 4,
    "ephemerality_sorted": 0.625,
    "ephemerality_sorted_span": 3
  },
  {
    "ephemerality_original": 0.2500000000000001,
    "ephemerality_original_span": 3,
    "ephemerality_filtered": 0.5,
    "ephemerality_filtered_span": 2,
    "ephemerality_sorted": 0.5,
    "ephemerality_sorted_span": 2
  }
]
```

Input 2:

```
python ephemerality.py 0.0 0.0 0.0 0.2 0.55 0.0 0.15 0.1 0.0 0.0 -t 0.5
```

Output 2:
```
0.0 5 0.8 1 0.8 1
```

#### Docker execution
```
docker run -a STDOUT -v [PATH_TO_FOLDER]/tmp/:/tmp/ ephemerality:1.0.0 -i /tmp/test_input.csv -o /tmp/test_output.json -t 0.5 -p 
```

Output:
```
0.0 5 0.8 1 0.8 1
0.19999999999999996 2 0.6 1 0.6 1
```

`test_output.json` content:
```
[
  {
    "ephemerality_original": 0.0,
    "ephemerality_original_span": 5,
    "ephemerality_filtered": 0.8,
    "ephemerality_filtered_span": 1,
    "ephemerality_sorted": 0.8,
    "ephemerality_sorted_span": 1
  },
  {
    "ephemerality_original": 0.19999999999999996,
    "ephemerality_original_span": 2,
    "ephemerality_filtered": 0.6,
    "ephemerality_filtered_span": 1,
    "ephemerality_sorted": 0.6,
    "ephemerality_sorted_span": 1
  }
]
```


## References
<a id="1">[1]</a>
Gnatyshak, D., Garcia-Gasulla, D., Alvarez-Napagao, S., Arjona, J., & Venturini, T. (2022). Healthy Twitter discussions? Time will tell. arXiv preprint arXiv:2203.11261
