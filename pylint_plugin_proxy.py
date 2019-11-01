"""
astroid plugin for loading transforms and in future possilby
type inferences from module level astoid plugin modules instead
of specifying on command line or in pyling config
"""

# TODO if reqired add typeinference hint proxy

import os.path as ospath
import importlib.util
import astroid

def register(linter):
    pass

_knownmodules = dict()
_nomodule = ()
_nodesofinterest = (
    astroid.ClassDef,
)

def transform_proxy(node):
    """
    loads custom astroid transform definitions from local
    astroid plugin files and makes them available to any
    parser or linter utilizing them. for example pylint
    """
    if not isinstance(node, _nodesofinterest):
        # node not of interest
        return node
    _nodename = node.qname()
    _nodemodule = _knownmodules.get(_nodename)
    if _nodemodule:
        # transform plugin already loaded do not bother any further
        return node
    # find defining module
    _module = node
    while _module:
        if not isinstance(_module, astroid.Module):
            _module = _module.parent
            continue
        break
    if _module is None:
        # no module found along ast tree ignore node
        _knownmodules[_nodename] = _nomodule
        return node
    # check if module defining node has already been checked
    _modulename = _module.qname()
    _nodemodule = _knownmodules.get(_modulename)
    if _nodemodule:
        # node is defined by module corresponding astoid transforms and type inferences
        # have already been loaded
        _knownmodules[_nodename] = _nodemodule
        return node
    # check if on the same path a astroid transform and type inference plugin
    # can be found and import it
    if not _module.file:
        _knownmodules[_modulename] = _knownmodules[_nodename] = _nomodule
        return node
    _package = _module
    _moduleastpath,_fn = ospath.split(_module.file)
    _moduleprefix = ospath.splitext(_fn)[0]
    _moduleastname = "{}_astroid".format(_moduleprefix)
    _moduleastfile = ospath.join(_moduleastpath, "{}.ast.py".format(_moduleprefix))
    _modulespec = importlib.util.spec_from_file_location(_moduleastname,_moduleastfile)
    if _modulespec is None:
        # remember that no ast module exists for node and corresponding module
        _knownmodules[_modulename] = _knownmodules[_nodename] = _nomodule
        return node
    # try to import plugin module
    _nodemodule = importlib.util.module_from_spec(_modulespec)
    if _nodemodule is None:
        _knownmodules[_modulename] = _knownmodules[_nodename] = _nomodule
        return node
    try:
        _modulespec.loader.exec_module(_nodemodule)
    except FileNotFoundError:
        # remember that no ast module exists for node and corresponding module
        _knownmodules[_modulename] = _knownmodules[_nodename] = _nomodule
        return node

    _knownmodules[_modulename] = _knownmodules[_nodename] = _modulespec
    # done let the local ast node transforms for astroid.ClassDef nodes do
    # the transforms and typeinferences just imported

for _interestedin in _nodesofinterest:
    astroid.MANAGER.register_transform(_interestedin, transform_proxy)
