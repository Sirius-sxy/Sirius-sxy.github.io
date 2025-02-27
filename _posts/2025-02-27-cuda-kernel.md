---
title: 'My Cuda Note 2: Build a kernel in PyTorch'
date: 2025-02-24
permalink: /posts/2025/02/cuda/note/kernel
tags:
  - cuda
  - note
---
**You can also find the official example in [Github](https://github.com/pytorch/extension-cpp)**
###### _Last modified: 2025-02-27_

# I.How to build a kernel

First, create a `.cu` and use cuda to build a kernel:
```c++
__global__ void test_kernel_cuda(
    int numel,
    const float* a,
    const float* b,
    float* output
) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < numel) {
        output[i] = a[i] + b[i];
    }
}
```

numel: the size of the array
a, b: input array
output: output array

Then, use a function to wrap it, take pytorch as an example:

```c++
at::Tensor test_kernel_cuda_wrapper(
    const at::Tensor& a,
    const at::Tensor& b
) {
    TORCH_CHECK(a.device().is_cuda(), "input tensor a must be a CUDA tensor");
    TORCH_CHECK(b.device().is_cuda(), "input tensor b must be a CUDA tensor");
    TORCH_CHECK(a.dtype() == b.dtype(), "input tensor a and b must have the same dtype");
    TORCH_CHECK(a.sizes() == b.sizes(), "input tensor a and b must have the same shape");
    auto numel = a.numel();
    auto output = at::empty_like(a);
    test_kernel_cuda<<<(numel + 256 - 1) / 256, 256>>>(
        numel,
        a.data_ptr<float>(),
        b.data_ptr<float>(),
        output.data_ptr<float>()
    );
    return output;
}
```

After that, use `TORCH_LIBRARY_IMPL` to register the implement:

```c++
TORCH_LIBRARY_IMPL(cuda_test, CUDA, m) {
    m.impl("test_kernel", &test_kernel_cuda_wrapper);
}
```

Create a `.cpp` to register the module:

```c++
extern "C" {
    PyObject* PyInit__C(void)
    {
        static struct PyModuleDef module_def = {
            PyModuleDef_HEAD_INIT,
            "_C",   /* name of module */
            NULL,   /* module documentation, may be NULL */
            -1,     /* size of per-interpreter state of the module,
                     or -1 if the module keeps state in global variables. */
            NULL,   /* methods */
        };
        return PyModule_Create(&module_def);
    }
}
```

Then register this library to pytorch:

```c++
TORCH_LIBRARY(cuda_test, m) {
    m.def("test_kernel(Tensor a, Tensor b) -> Tensor");
}
```

Create `__init__.py` and `ops.py` as follow:
```python
# __init__.py
import torch
from pathlib import Path
from . import _C, ops

# ops.py
import torch
from torch import Tensor

__all__ = ["test_kernel"]

def test_kernel(a: Tensor, b: Tensor) -> Tensor:
    return torch.ops.cuda_test.test_kernel.default(a, b)
```

Createa `setup.pt`:
```python
import os
import torch
import glob

from setuptools import find_packages, setup

from torch.utils.cpp_extension import (
    CppExtension,
    CUDAExtension,
    BuildExtension,
    CUDA_HOME,
)

library_name = "cuda_test"

if torch.__version__ >= "2.6.0":
    py_limited_api = True
else:
    py_limited_api = False


def get_extensions():
    debug_mode = os.getenv("DEBUG", "0") == "1"
    use_cuda = os.getenv("USE_CUDA", "1") == "1"
    if debug_mode:
        print("Compiling in debug mode")

    use_cuda = use_cuda and torch.cuda.is_available() and CUDA_HOME is not None
    extension = CUDAExtension if use_cuda else CppExtension

    extra_link_args = []
    extra_compile_args = {
        "cxx": [
            "-O3" if not debug_mode else "-O0",
            "-fdiagnostics-color=always",
            "-DPy_LIMITED_API=0x03090000",  # min CPython version 3.9
        ],
        "nvcc": [
            "-O3" if not debug_mode else "-O0",
        ],
    }
    if debug_mode:
        extra_compile_args["cxx"].append("-g")
        extra_compile_args["nvcc"].append("-g")
        extra_link_args.extend(["-O0", "-g"])

    this_dir = os.path.dirname(os.path.curdir)
    extensions_dir = os.path.join(this_dir, "cuda_test",
                                  "csrc")
    sources = list(glob.glob(os.path.join(extensions_dir, "*.cpp")))

    cuda_sources = list(glob.glob(os.path.join(extensions_dir, "*.cu")))
    print(f"cuda_sources: {cuda_sources}")
    if use_cuda:
        sources += cuda_sources
    ext_modules = [
        extension(
            f"{library_name}._C",
            sources,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            py_limited_api=py_limited_api,
        )
    ]

    return ext_modules

setup(
    name=library_name,
    version="0.0.1",
    packages=find_packages(),
    ext_modules=get_extensions(),
    install_requires=["torch"],
    cmdclass={"build_ext": BuildExtension},
    options={"bdist_wheel": {"py_limited_api": "cp39"}} if py_limited_api else {},
)
```

Finally, install this package:
```bash
python setup.py install
```

### Note:
Remember: As the source directory name `cuda_test` is the same as the packege's, you may need to leave this directory to run test.

# Copyright:

<p xmlns:cc="http://creativecommons.org/ns#" >This work is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt=""></a></p>


