# ievv-coderefactor

Simple and well structured refactoring of code.

Uses a JSON config file to specify what to refactor, and
a CLI that takes a directory + path to the JSON config file
to run the refactoring.

Suitable for cases where you have need for re-usable
refactoring configurations. It was made to handle refactoring
of code that can be refactored between major releases of a project.

The docs are lacking for now, but you can try it out, and get
started by by looking at, and running the example in
``examples/simple/``. The config is in ``examples/simple/refactor-config.json``.

To refactor the example using the example config, use:

```
$ ievv-coderefactor refactor examples/simple --config examples/simple/refactor-config.json
```


## TODO:
- Document the JSON config format
