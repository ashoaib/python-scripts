# python-scripts

## Description

This is/will be a repository for the library of various python scripts I've written to make certain development tasks easier. It will be updated with more scripts as and when I create them.

## google_closure_compiler.py

This is wrapper class for compiling JavaScript file(s) into a single minified file, using Google's Closure Compiler API. It can read an individual file, be passed a list of files, or read files from a directory. It writes to an output file in the same directory as the source.

### Example usage

#### Command-line

The script can be called from the command line:

```
python google_closure_compiler.py <path_to_source> <output_file_name>
```

`<path_to_source>` can be a path to a file or a directory

`<output_file_name>` is an optional argument - this is the name of the output file to write the compiled JavaScript to. If not passed, defaults to js-min.js

#### Within python

```python
import google_closure_compiler

foo = google_closure_compiler.GoogleClosureCompiler(path_to_source, output_file_name)
foo.compile()
```

## txt2dat.py

This is a simple script for converting an IP filter text (.txt or P2P format) file to a more recognisable .dat file. Typically used to generate IP filter list for uTorrent or Vuze.
