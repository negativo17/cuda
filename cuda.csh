if ( -x /usr/bin/nvcc ) then
  setenv NVVMIR_LIBRARY_DIR /usr/share/cuda
endif

if ( -x /usr/libexec/cuda/open64/bin/nvopencc ) then
  setenv PATH ${PATH}:/usr/libexec/cuda/open64/bin
endif

if ( -d /usr/include/cuda ) then
  setenv CUDA_INC_PATH /usr/include/cuda
endif
