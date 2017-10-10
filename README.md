# RNN

The prototype of RNN for Intel platform, especially for Xeon and Xeon Phi.

* vRNN
* LSTM
* GRU
* peephole
* Stack-X
* Bidirection-X

## Introduction

This is a fast implemention for RNN with fused operations and better utilization of GEMM/Batch GEMM/Pack GEMM.
 
## Installation

Before the following steps, please make sure the pytorch is installed.

First get the code:

```
git clone https://github.com/pengzhao-intel/RNN.git
cd RNN
```

create a build directory:

```
mkdir build
cd build
cmake ..
make
cd ..
```
The C library should now be built along with test executables.

Then we bind this C library to pytorch:

```
cd pytorch_binding
python setup.py install
cd ..
```

## Test

For a simple test to varify that all the interface are called correctly:

```
python test.py
```



