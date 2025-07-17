"""
Given the machine code of a Marie program (16-bit), this program will help convert it to Marie source code.
"""

# import stuff
import sys
import argparse
from collections import defaultdict
from copy import deepcopy


# defining default input/output files
machine_code_file_path = "../machine_code/machine_code.txt"
MARIE_source_code_file_path = "../source_code/MARIE_source_code.txt"

# sys args

parser = argparse.ArgumentParser( 
  description="A script that takes an input file of machine code and writes the converted MARIE source code to an output file." 
)   

# input arg
parser.add_argument("input", help="Machine code input file path.") 

# output arg
parser.add_argument( 
  "-o", "--output", help="The output file to write MARIE source code.",
)

# print
parser.add_argument("-v", "--verbose", help="Print the converted MARIE source code to stdout.", action="store_true")

# parse
args = parser.parse_args()

# check if custom file paths
if args.input:
    machine_code_file_path = args.input
if args.output:
    MARIE_source_code_file_path = args.output

# instructions
# NOTE: the instructions "A" and "0" map to different source codes.
# However, they are interchangeable, but some may be more suitable for certain contexts.
num_to_instruction = {
    "3" : "Add",
    "4" : "Subt",
    "B" : "AddI",
    "A" : "LoadImmi/Clear",
    "1" : "Load",
    "D" : "LoadI",
    "2" : "Store",
    "E" : "StoreI",
    "5" : "Input",
    "6" : "Output",
    "9" : "Jump",
    "8" : "SkipCond",
    "0" : "JnS/Adr",
    "C" : "JumpI",
    "7" : "Halt",
    "F" : "F"
}   


# get input
# NOTE: Put machine code separated by newlines or spaces in separate text file
with open(machine_code_file_path) as f:
    instructions = f.read().split()



# generate instructions
source_code = []
pivot = 0
for i, instruction in enumerate(instructions):
    # code = f"{num_to_instruction[instruction[0]]} {instruction[1:]}"
    code = [num_to_instruction[instruction[0]], instruction[1:]]
    address = hex(i).upper()
    source_code.append((address, code))
    if instruction[0] == "7":
        pivot = i + 1
        break

for i in range(pivot, len(instructions)):
    address = hex(i).upper()
    source_code.append((address, instructions[i]))



# unfiltered code
unfiltered = []
for _, code in source_code:
    unfiltered.append(code)



# define variables that will be used to replace the fixed addresses
var_to_val = defaultdict(str)
adr_to_var = defaultdict(str)
filtered_1 = deepcopy(unfiltered)
variables = ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1", "I1", "J1", "K1", "L1", "M1", "N1", "O1", "P1", "Q1", "R1", "S1", "T1", "U1", "V1", "W1", "X1", "Y1", "Z1",
             "A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2", "I2", "J2", "K2", "L2", "M2", "N2", "O2", "P2", "Q2", "R2", "S2", "T2", "U2", "V2", "W2", "X2", "Y2", "Z2"]
var_indx = 0
for i in range(pivot, len(unfiltered)):
    new_val = str(int(unfiltered[i], base = 16))

    new_var = variables[var_indx]
    var_to_val[new_var] = new_val

    var_adr = source_code[i][0][2:]
    adr_to_var["0" * (3 - len(var_adr)) + var_adr] = new_var

    var_indx += 1

    new_code = [f"{new_var}, DEC", new_val]

    filtered_1[i] = new_code



# sub address for variable names
filtered_2 = deepcopy(filtered_1)
for i in range(pivot):
    curr_code = filtered_2[i]
    instruction = curr_code[0]
    pointing_adr = curr_code[1]
    if pointing_adr in adr_to_var:
        pointing_var = adr_to_var[pointing_adr]
        new_code = [instruction, pointing_var]
        filtered_2[i] = new_code



# get rid of JnS/Adr and also unecessary 000's
# also define adr_to_func dict
filtered_3 = deepcopy(filtered_2)

curr_func = 1

adr_to_func = defaultdict(str)

for i in range(pivot):
    code = filtered_3[i]
    instruction, val = code
    adr = source_code[i][0]
    if val == "000":
        if instruction == "JnS/Adr":
            filtered_3[i][0] = f"Func{curr_func},"

            func_adr = source_code[i][0][2:]
            adr_to_func["0" * (3 - len(func_adr)) + func_adr] = f"Func{curr_func}"

            curr_func += 1

            filtered_3[i][1] = "HEX 000"

        elif instruction == "Output" or instruction == "Halt":
            filtered_3[i][1] = ""



# getting the address of 'functions'
# aka the addresses that are the destination of JnS
for i in range(pivot):
    code = filtered_3[i]
    instruction, val = code

    pointing_adr = val
    if instruction == "Jump" and val[:4] != "Func" and pointing_adr not in adr_to_func:
        func_adr = pointing_adr
        adr_to_func["0" * (3 - len(func_adr)) + func_adr] = f"Func{curr_func}"
        curr_func += 1



# now replace some addresses with function variables
filtered_4 = deepcopy(filtered_3)

for i in range(pivot):
    instruction, pointing_adr = filtered_4[i]
    curr_adr = hex(i).upper()[2:]
    curr_adr = "0" * (3 - len(curr_adr)) + curr_adr

    if instruction[:4] != "Func":
        if pointing_adr in adr_to_func:
            filtered_4[i][1] = adr_to_func[pointing_adr]
        if curr_adr in adr_to_func:
            new_instruction = f"{adr_to_func[curr_adr]}, {instruction}"
            filtered_4[i][0] = new_instruction



# final product
final_source_code = '\n'.join(' '.join(c) for c in filtered_4)

if args.verbose:
    print(final_source_code)


# write source code to file
# DEFAULT: "../source_code/MARIE_source_code.txt"
with open (MARIE_source_code_file_path, "w") as f:
    f.write(final_source_code)