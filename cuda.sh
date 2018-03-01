if [ -x /usr/bin/cuda-g++ ]; then
  export HOST_COMPILER=/usr/bin/cuda-g++
fi

if [ -x /usr/libexec/cuda/open64/bin/nvopencc ]
  export PATH=$PATH:/usr/libexec/cuda/open64/bin
fi
