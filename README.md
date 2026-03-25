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


