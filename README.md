# Pylint Plugin Proxy #

The Pylint Plugin Proxy allows to define and distribute pylint astrioid
transform and in future also likely type inference plugins with the python
module they provide additional static knowledge for. 

## Usage ##
Add the path the Pylint Plugin Proxy module is stored to the PYTHON path
envirionment variable. Activate the plugin on the commandline by calling

` pylint --load-plugins=pylint_plugin_proxy <filetolint>.py `

or set the correspoinding parameter in the pylintrc file accordingly.

## Create local plugin ##

Change to the directory where `MyModule.py` is stored and create the corresponding
`MyModule.ast.py` plugin module by typing

`
editor MyModule.ast.py
`

An example on how to write a transform plugin can be found on 
<https://pylint.readthedocs.io/en/latest/how_tos/transform_plugins.html>


The next time pylint is called using the above line `MyModule.ast.py` plugin module will be loaded and used when a class defined in `MyModule.py` is encountered by Pylint. 

