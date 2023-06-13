U-TOE: Universal TinyML On-board Evaluation Toolkit for Low-Power AIoT
=====================

# Get Source Code

It is important to clone the submodules along, with `--recursive` option.

```
git clone --recursive git@github.com:zhaolanhuang/U-TOE.git
```

Or open the git shell after clone, and type the following command.

```
git submodule init
git submodule update
```

# Prequisites
This toolkit is tested under:
- Linux Mint 21.1 (5.15.0-58-generic)
- Python 3.10.8
- LLVM 14.0.0
- CMAKE 3.22.1


## Install TVM from Source
First, Follow the instruction from [official docs](https://tvm.apache.org/docs/install/from_source.html).

It is recommended to switch on the following options in `config.cmake`:
```
USE_GRAPH_EXECUTOR 
USE_PROFILER 
USE_MICRO
USE_LLVM
```
For CUDA users, it is recommended to switch `USE_CUDA` on.  
For PyTorch users, it is recommended to set `(USE_LLVM "/path/to/llvm-config --link-static")` and `set(HIDE_PRIVATE_SYMBOLS ON)`.

After built up the TVM libraries, set the environment variable to tell python where to find the packages:
```
export TVM_HOME=/path/to/tvm
export PYTHONPATH=$TVM_HOME/python:${PYTHONPATH}
```
### Patch Graph Debug Executor
The vanilla executor in TVM calls inexistent *__nop* operators, which will crash the RPC runtime on the board. If you want to try the Per-Operator evaluation, please patch the executor and (re)build TVM with the following commands:

```
cp <path-to-utoe>/patch/fixup_skip_nop_op.patch /path/to/tvm
cd /path/to/tvm
git apply fixup_skip_nop_op.patch
( (re)build tvm )

```

## Install RIOT Toolchains
Please refer to the doc [Getting started - Compiling RIOT](https://doc.riot-os.org/getting-started.html#compiling-riot)

For RISC-V toolchain, please enable __multilib__ support.

## Install Python Packages
Use the command below to install the dependencies:
```
pip install -r requirements.txt
```
## (Optional) FIT IoT-LAB
To use remote boards on [FIT IoT-LAB](https://www.iot-lab.info/docs/getting-started/introduction/), please first [register a testbed account](https://www.iot-lab.info/docs/getting-started/user-account/) and set up [SSH access](https://www.iot-lab.info/docs/getting-started/ssh-access/). After that, use following commands to store the credentials for U-TOE:

```
iotlab-auth -u <login user name>
iotlab-auth --add-ssh-key
```
# Usage
Befor running the evaluation, please get your model files ready from ML frameworks (TFLite, PyTorch etc.). You can find some model file examples in `model_zoo` folder.  

U-TOE provides a command line interface (CLI) entry `u-toe.py`, see below:

```
> python u-toe.py -h

usage: u-toe.py [-h] [--per-model | --per-ops] [--board BOARD] [--use-iotlab] [--iotlab-node IOTLAB_NODE] [--random-seed RANDOM_SEED] [--trials-num TRIALS_NUM] model_file

positional arguments:
  model_file            path to machine leearning model file.

options:
  -h, --help            show this help message and exit
  --per-model           Per-Model Evaluation (default).
  --per-ops             Per-Operator Evaluation.
  --board BOARD         IoT board name
  --use-iotlab          use remote board in FIT IoT-LAB.
  --iotlab-node IOTLAB_NODE
                        remote node url. It will start an new experiment if this field is empty.
  --random-seed RANDOM_SEED
                        default: 42
  --trials-num TRIALS_NUM
                        defalut: 10
```

## Per-Model Evaluation
- Local example:

```
python u-toe.py --per-model --board stm32f746g-disco ./model_zoo/mnist_0.983_quantized.tflite
```
This command will start a Per-Model evaluation on local board `stm32f746g-disco`, using `LeNet-5 INT8` model.

- FIT-IoT Lab example:

```
python u-toe.py --per-model --use-iotlab  --board iotlab-m3 ./model_zoo/mnist_0.983_quantized.tflite
```
This command will start a IoT-Lab experiment and execute a Per-Model evaluation on remote board `iotlab-m3`, using `LeNet-5 INT8` model.

- Output example:
```
Board        Memory (KB)    Storage (KB)  95-CI (ms)          Mean (ms)    Median (ms)    Min. (ms)    Max. (ms)
---------  -------------  --------------  ----------------  -----------  -------------  -----------  -----------
iotlab-m3          11.08          65.232  [97.739, 97.757]       97.748         97.751       97.733       97.764
```
## Per-Operator Evaluation
! Please first [patch TVM executor](#patch-graph-debug-executor) before trying out this feature. !

- Local example
```
python u-toe.py --per-ops --board stm32f746g-disco ./model_zoo/sinus_float.tflite
```
This command will start a Per-Operator evaluation on local board `stm32f746g-disco`, using `sinus` model.

- FIT IoT-Lab Example: comming soon...

- Output example

```
Ops                                            Time (us)    Time (%)  Params          Memory (KB)    Storage (KB)
-------------------------------------------  -----------  ----------  ------------  -------------  --------------
tvmgen_default_fused_nn_dense_add_nn_relu          8.853      15.217  ['p0', 'p1']          0.128           0.128
tvmgen_default_fused_nn_dense_add_nn_relu_1       46.682      80.236  ['p2', 'p3']          0.128           1.088
tvmgen_default_fused_nn_dense_add                  2.646       4.548  ['p4', 'p5']          0.02            0.068
```

# Model Zoo
| Model        | Description                                         | File name                    |
| ------------ | --------------------------------------------------- | ---------------------------- |
| LeNet-5 INT8 | Quantized LeNet-5 in INT8, trained on MINST dataset | mnist_0.983_quantized.tflite |
|              |                                                     |                              |
