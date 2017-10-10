# build.py
import os
import platform
import sys
from distutils.core import setup

from torch.utils.ffi import create_extension

extra_compile_args = ['-std=c++11', '-fPIC']
intel_RNN_path = "../build"


if platform.system() == 'Darwin':
    lib_ext = ".dylib"
else:
    lib_ext = ".so"

headers = ['src/binding.h']

if "INTEL_RNN_PATH" in os.environ:
    intel_RNN_path = os.environ["INTEL_RNN_PATH"]
if not os.path.exists(os.path.join(intel_RNN_path, "libintelRNN" + lib_ext)):
    print(("Could not find libintelRNN.so in {}.\n"
           "Build intelRNN and set INTEL_RNN_PATH to the location of"
           " libintelRNN.so (default is '../build')").format(intel_RNN_path))
    sys.exit(1)
include_dirs = [os.path.realpath('../include')]

ffi = create_extension(
    name='intel_rnn',
    language='c++',
    headers=headers,
    sources=['src/binding.cpp'],
    with_cuda=False,
    include_dirs=include_dirs,
    library_dirs=[os.path.realpath(intel_RNN_path)],
    runtime_library_dirs=[os.path.realpath(intel_RNN_path)],
    libraries=['intelRNN'],
    extra_compile_args=extra_compile_args)
ffi = ffi.distutils_extension()
ffi.name = 'intelrnn_pytorch._intel_rnn'
setup(
    name="intelrnn_pytorch",
    version="0.1",
    description="PyTorch wrapper for intel-rnn",
    url="https://github.com/intel/intel-rnn",
    author="Xiaohui zhao, Patric zhao",
    author_email="Xiaohui.zhao@intel.com, Partric.zhao@intel.com",
    license="Apache",
    packages=["intelrnn_pytorch"],
    ext_modules=[ffi],
)
