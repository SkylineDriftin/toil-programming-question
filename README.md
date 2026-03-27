# toil-programming-question



Notes about making the tool:

I haven't had much exposure to making maintainable CLI tools in the past, so I had to do a bit of research to figure out the best methods. In my search, I looked for a well-documented package for Python. I chose to use Python for its widespread use and maintainability. 

There were three tools I decided between:
- Argparse
- Typer
- Click

Argparse:
- built in
- no need for external dependencies
- lightweight
- very customizable and well-documented
- verbose and requires more boilerplate to set up
- less user friendly by default

Click: 
- Less boilerplate, using decorators tto define args and commands instead
- supports more feauteres ( nesting commands, validdating inputs,)
- active development 
- requires external dependency


Typer:
- minimal boilerplate
- built on click
- smaller and newer
- type hint integration 


I chose to use typer for its simplicity and large community support. 

-- notes about file structure
I followed the Python Packaging User Guide and used a src layout for the file structure
src layout moves code that is intended to be importable into a subdirector 'src'
 https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/


-- attacking the problem itself

This problem seems to be an optimization problem in which we need to minimize the total possible consumption by removing one edge from the graph. 

The basic solution seems to be  
- set up directed graph
- find initial total consumption
- iterate through every edge and remove one and calculate the result
- store lowest edge result
- output edge at filepath

This is the brute-force method for minimizing with an efficiency of o(n**2). This may work for a small pipeline count, but for large n values (n>10000), it might take a bit longer. I don't think this is very time-sensitive, but I think it doesn't hurt to optimize it anyways. 



I noticed each of the nodes is directionally connected to another node, and therefore can be represented by a directional graph. 


-- setting up the initial graph

the directional graph should be pretty simple to implement.
Each node should have 3 attributes:
max consumption, production, and connected nodes. 
I used json parser and parsed through the nodes to obtain the file. 