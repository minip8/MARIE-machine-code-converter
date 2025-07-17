# MARIE-machine-code-converter
**NOTE: This little quest was done with the goal of simply ~~completing~~ verifying my university assignment for me, so don't be shocked by poor code quality.**

---

## MARIE breakdown
[MARIE](https://marie.js.org) - Machine Architecture that is Really Intuitive and Easy - is essentially a simulator created to help developers learn how a basic CPU can work.

Each MARIE program has source code that can be compiled into 16-bit machine code.

The first 4 bits are dedicated to the **instruction**, which basically says "do this". The following 12 bits represents the memory address, which completes the previous statement, saying "do it to this place".

The full instruction set can be found by going [here](https://marie.js.org), and clicking on `Instruction Set` in the top right corner.

However, there is an important distinction we have to make. How does MARIE hold variables?

Simply put, if MARIE executes the code directly, then it will interpret the value at the memory address to be an instruction. Otherwise, if it is simply fetching a value from another address, then MARIE will interpret all 16 bits as one number.

Hopefully, the information above is enough to have a basic understanding of MARIE.

## The goal
What do we do if we are given the machine code of some MARIE program, and we need to convert it to MARIE source code?

Using [this](converter/converter.py), we can do exactly that!

## How to use
### Downloading
To run this program, first download or clone the repository.
If you chose to download, extract the `.zip` file.

### Changing directories
Now, open your favourite terminal. Note that if you're using bash, use `python3` instead of `python` in your command line.

First, `cd` into wherever you located the directory.

```bash
cd path-to-directory
```

Now, `cd` into the `converter` directory.
```bash
cd converter
```

### Usage
Now that you're in the proper directory, we can run the `converter.py` file with ease, with the command below.

```bash
python converter.py
```

**NOTE: The default input file path is [machine_code/machine_code.txt](machine_code/machine_code.txt) and the default output file path is [source_code/MARIE_source_code.txt](source_code/MARIE_source_code.txt).**


If you wish to read from a custom file, simply run:

```bash
python converter.py path-to-file.txt
```

## Flags
Additionally, you can use `-o` or `--output` to specify the output file:

```bash
python converter.py path-to-file.txt -o path-to-output-file.txt
```

If you wish to print the output to `stdout`, simply add the `-v` or `--verbose` flag:

```bash
python converter.py -v
```


## The process behind making this possible
Below uses [this machine code](machine_code/machine_code.txt) as a reference.


### Find the `HALT` AKA `7000`
Given [this machine code](machine_code/machine_code.txt), we first make one crucial observation: the `HALT` instruction lies on line 35.

We can call this the `pivot`.


### Variables
As per the convention of MARIE source code, all variables, both constant and non-constant, will be placed **after** the `HALT` instruction.<br>
This observation allows us to assign variables to each value that appears after the `HALT` instruction.

We can now assign each address after the `pivot` to a variable name, starting from `Var1`.

### Subroutines AKA functions
Whenever we `JnS` or `Jump` to some address, that address is most likely the start of some function.

So, we can find every destination of a `JnS` or `Jump`, and assign a function name to that address, starting from `Func1`, **given that the target address does not contain the `Halt` instruction**.


### Putting it all together
Now that we know when an address corresponds to a variable or a function, we can respectively replace each instance of each address with the corresponding variable or function name.

Finally, we can neatly format the final data for a neat output!


### Other important stuff
This program should be pretty fool proof if the machine code provided follows MARIE conventions. Of course, I haven't extensively tested it, but it seems to have worked for my own use, as well as some of my friends' usage too.

However, it is still important that the source code is double checked by compiling it in [MARIE's online IDE](https://marie.js.org), and cross-checking with the machine code that it generates.<br>
It should be the same as your own machine code.

Something also noted in the start of [the program](converter/converter.py) is that the instruction pair `(Jns, Adr)` has the same instruction in machine code: `6`.<br>
The program will output `Jns/Adr` when this happens. It is up to you to decide which is more suitable for the context, though using either will work.

Obviously, the variable and function names will also not have much meaning, so it is again, up to you, to decide what meaningful names are suitable in the context of the program.