LIGO-Virgo Veto Definitions
===========================

This repository hosts the veto definitions used by the joint LIGO-Virgo transient data anlysis groups.
The veto definitions are recorded in `LIGO_LW`-schema XML files.

All changes to these files should be made via the GitHub [fork-and-pull](https://guides.github.com/introduction/flow/) model.

Validation
----------
The python modules contained in this repository provides methods to validate a veto-definer file and its contents.

The `vetodef` python package can be installed by running

```python
python setup.py install
```

from the root of the repository.

The python executables in the `bin` directory will be installed as well as the `vetodef` package.

From there a blank veto-definer file can be created via

```bash
ligolw-vetodef-create <filename>
```

and then appended to via

```bash
ligolw-vetodef-append <filename> <flag> [<options>]
```

and finally validated against all standard checks via

```bash
ligolw-vetodef-validate <filename>
```
