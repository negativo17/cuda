if [ -x /usr/bin/cuda-g++ ]; then
  export HOST_COMPILER=/usr/bin/cuda-g++
fi

if [ -x /usr/libexec/cuda/open64/bin/nvopencc ]; then
  export PATH=$PATH:/usr/libexec/cuda/open64/bin
fi

if [ -d /usr/include/cuda ]; then
  export CUDA_INCLUDE_DIRS=/usr/include/cuda
  export CUDA_INC_PATH=/usr/include/cuda
fi
