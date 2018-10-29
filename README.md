CGRA PnR [![Build Status](https://travis-ci.org/Kuree/cgra_pnr.svg?branch=master)](https://travis-ci.org/Kuree/cgra_pnr)
---
Generic place and route tool for CGRA.
## Getting started
### Prerequisites
Because the C++ implementation, exposed to Python via `pybind11`, uses lots
of C++14/17 features, a modern C++ compiler is required.
+ `g++` 7.0 and above
+ `gcc` 7.0 and above.
+ `cmake` 3.5 and above.
+ `Python` 2.7+/3.6+
### Install
```
$ make
$ pip install thunder/
$ pip install -r requirements.txt
```
#### Use Thunder in other projects
The core library, `thunder`, can be used outside this repo. Simply do
```
pip install -e git+https://github.com/Kuree/cgra_pnr#egg=pkg\&subdirectory=thunder
```
Usage of this library can be found in `place.py`.

### Usage
```
$ ./scripts/pnr_flow.sh [--no-reg-fold] <cgra_info.txt> <mapped_design.json> [output.bsb]
```
  - `--no-reg-fold` optimizes for the routing path as it turns some registers into PE tiles. Without using `--no-reg-fold` we will have about 15% area reduction, but it may have longer path, based on the current CGRA design. So given timing information as well as more flexible hardware generation in the future, this option needs to be used on a case by case basis.
  - if `<output.bsb>` not specified, it will output `<mapped_design.bsb>` to the same directory as` <netlist.json>`

Files created in the same directory as `<mapped_design.json>`:
+ `<mapped_design.n2v>`: random walk on the star-expanded netlist graph
+ `<mapped_design.emb>`: netlist embedding computed by `word2vec`
+ `<mapped_design.packed>`: packed netlists, including information on converted netlist as well as id information used internally throughout the toolchain.
+ `<mapped_design.place>`, placement result, using internal id
+ `<mapped_design.route>`, routing result. Each section is the route for a single net. More details see the header section in the result file
+ `<mapped_design.bsb`, bsbuilder files can be compiled to bitstream via `bsbuilder.py` in `CGRAGenerator`

### Analysis Tool
The toolchain has a tool to produce post-PnR report on area usage, route channel usage, and timing. Here is an example on harris:
```
Area Usage:
I    █                                                                   2.94%
P    ██████████████████████████                                          39.58%
M    ██████████                                                          15.62%
--------------------------------------------------------------------------------
Total wire: 530
--------------------------------------------------------------------------------
Critical Path:
Delay: 9.75 ns Max Clock Speed: 102.56 MHz
MUL  ███████████████████████████                                         41.03%
SB   █████████████████████                                               32.31%
ALU  ██████████████████                                                  26.67%
CB                                                                       0.00%
MEM                                                                      0.00%
REG                                                                      0.00%
--------------------------------------------------------------------------------
BUS: 16
TRACK 0 ████████████████                                                 24.38%
TRACK 1 █████████████                                                    20.44%
TRACK 2 █████████                                                        14.10%
TRACK 3 ████████                                                         12.47%
TRACK 4                                                                  0.85%
BUS: 1
TRACK 0 █████                                                            8.56%
TRACK 1 █                                                                1.92%
TRACK 2                                                                  0.00%
TRACK 3                                                                  0.00%
TRACK 4                                                                  0.00%

```

### FPGA
It supports both `VPR` and `bookshelf` format. As a result, it can place any
packed version of VPR benchmark or ISPD FPGA benchmark. However, because it's
not designed to place generic netlists, it may not obtain an optimal solution,
or may be very slow to converge.
### Work in progress
1. ~~Integrate DAG kernel based partition.~~
2. ~~Use register folding instead of wasting PE tiles for registers that drives more than one net.~~ Done
3. ~~reimplement in C++ for efficiency.~~
