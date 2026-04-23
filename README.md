## WBS to ProjectLibre

A simple tool that inserts WBS from a `.txt` file into an `.xml` format compatible with ProjectLibre (Microsoft Project XML format). 
Indentation in the wbs file is **optional** and used only for better readability. The hierarchy is determined by the numbering, not by spaces or tabs.
The input file should be a plain text, for example:

```txt
1 Lorem ipsum
    1.1 Lorem ipsum
        1.1.1 Lorem ipsum
```

### Usage

```bash
$ python3 script.py wbs.txt project.xml
```

>⚠️ **Warning:** Do not use existing output files as they will be overwritten. Input files are read only and will not be modified.

### Output

Generates a `.xml` file compatible with ProjectLibre, preserving the hierarchy of tasks:

![project.xml](img/output.png)