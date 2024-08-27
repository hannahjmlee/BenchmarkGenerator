# BenchmarkGenerator

BenchmarkGenerator is a user-friendly GUI tool designed for generating custom Multi-Agent Path Finding (MAPF) benchmarks. The benchmarks created with this tool adhere to the format specified in the widely used [MAPF Benchmarks](https://movingai.com/benchmarks/mapf/index.html). For a detailed explanation of the file formats, please refer to the [MAPF file formats documentation](https://movingai.com/benchmarks/formats.html).

## Installation

This tool requires `networkx` and `numpy`. You can install these dependencies with the following commands:

```
pip install networkx
pip install numpy
```

## Usage
To launch the BenchmarkGenerator GUI, run: 
```
python main.py 
```

This command will open an interactive GUI where you can define the size of your environment and click `Set Grid Size`. Clicking `Set Grid Size` will also clear your existing environment if you'd like to start over! 

You can customize this environment by clicking (and dragging) cells to create or remove obstacles. Once your environment is configured, you can save it as a `.map` file by providing a name for the environment and clicking the `Generate Environment` button.

If you wish to generate random scenarios for your environment, enter the desired number of scenarios and click the `Generate Scenarios` button. This will create a `.scen` file containing feasible motion tasks for the specified environment.
