jsontool
========

`jsontool` is utility to fighting with JSON files using CLI

Current stable version
----------------------

0.2.0

How to use it
-------------

    cat data1.json data2.json | jsontool --sort-by='timestamp'

    jsontool --color=always < data.json | less -R
    
More
----

    % jsontool -h
    usage: jsontool [-h] [-f SORT_BY] [-r] [-g GREP] [-v] [--sort-keys]
                    [--indent INDENT] [--color {auto,always,never}]
    
    optional arguments:
      -h, --help            show this help message and exit
      -f SORT_BY, --sort-by SORT_BY
                            sort given list of JSONs by this field
      -r, --sort-reversed   sort in reverse order
      -g GREP, --grep GREP  filter list of JSONs using this rules (can be added
                            more then once)
      -v, --version         show version and exit
      --sort-keys           sort keys in printed JSONs (default: not sorted)
      --indent INDENT       indent JSONs with INDENT spaces
      --color {auto,always,never}
                            manipulate colorizing of JSONs (default: auto)
    
    Argument to --grep option should be in format:
      field:value:modifier
    Where:
    - "field" must be in all JSONs.
    - "value" is value to search
    - "modifier" is optional, and say how to treat "value": allowed
      options are: s (string - default), b (boolean), i (integer), f (float)

Installation
------------

`jsontool` should work on any platform where [Python](http://python.org) is available, it means Linux, Windows, MacOS X etc. There is no required dependencies, plain Python power :)

To install, simply use `pip`:

    pip install jsontool

If you do not want to use `pip` tool, then go to [GitHub releases](https://github.com/mysz/jsontool/releases), download newest release, unpack and put somewhere in `PATH` (ie. `~/bin` or `/usr/local/bin`).

If You want to install newest unstable version, then just copy file to your PATH, for example:

    curl https://raw.github.com/mysz/jsontool/master/jsontool.py > /usr/local/bin/jsontool

or:

    wget https://raw.github.com/mysz/jsontool/master/jsontool.py -O /usr/local/bin/jsontool

Voila!

Authors
-------

Marcin Sztolcman <marcin@urzenia.net>

Contact
-------

If you like or dislike this software, please do not hesitate to tell me about this me via email (marcin@urzenia.net).

If you find bug or have an idea to enhance this tool, please use GitHub's [issues](https://github.com/mysz/jsontool/issues).

License
-------

The MIT License (MIT)

Copyright (c) 2014 Marcin Sztolcman

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

ChangeLog
---------

### v0.2.0

* renamed --field argument to --sort-by
* more formatting options (--sort-keys, --indent)
* allow to disable colorizing
* allow to not sort at all
* allow to sort reversed
* documentation and help added

### v0.1.0

* initial version
