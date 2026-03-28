# toil-programming-question

**installation:** 
Its configured as a package so it should be able to be installed as a local package. 

first clone the repo into your destination of choice
```
    git clone https://github.com/SkylineDriftin/toil-programming-question
    cd genomics_lab_question
```

I suggest creating a virtual environment to isolate project dependencies

```
    pip install .
```

verify install with

```
    attack_planner --help
```

usage:
```
    # Basic usage
    attack_planner path/to/input.json path/to/output.json

    # Run the automated test runner
    py -m src.attack_planner.tests.test_runner
```

**Notes about making the tool:**

I haven't had much exposure to making maintainable CLI tools in the past, so I had to do a bit of research to figure out the best methods. In my search, I looked for a well-documented package for Python. I chose to use Python for its widespread use and maintainability. 

There were three tools I decided between:
- Argparse
- Typer
- Click

I ultimately chose to use click for these reasons:
- Less boilerplate, using decorators tto define args and commands instead
- supports more feauteres ( nesting commands, validdating inputs,)
- active development 


**Attacking the problem**
I chose to model the netwrok as a directed graph.
Because of the multiple sources and nodes, used a super-source and super-sink limited by pipe capacity to represent the production and consumption of each node. This results in the net consumption of the facilities being the net flow. 

Initially I was thinking about a brute-force simulation, but I thought there must be a better method, so I read Wikipedia pages and found the Minimum cut theorem. 

I was going to implement everything myself, but I soon realized that there were many other researchers who had dealt with the same problem, and sought out a library. I encountered igraph, a library largely implemented in c, which is much faster than python. 


**notes about file structure**
I followed the Python Packaging User Guide and used a src layout for the file structure
src layout moves code that is intended to be importable into a subdirector 'src'
 https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/

The project should mostly conform to modern Python standards. 