[ -x /usr/bin/nvcc ] && export NVVMIR_LIBRARY_DIR=/usr/share/cuda
[ -x /usr/libexec/cuda/open64/bin/nvopencc ] && export PATH=$PATH:/usr/libexec/cuda/open64/bin
[ -d /usr/include/cuda ] && export CUDA_INC_PATH=/usr/include/cuda
