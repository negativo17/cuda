if ( -x /usr/bin/cuda-g++ ) then
  setenv HOST_COMPILER /usr/bin/cuda-g++
endif

if ( -x /usr/libexec/cuda/open64/bin/nvopencc ) then
  setenv PATH ${PATH}:/usr/libexec/cuda/open64/bin
endif

if ( -d /usr/include/cuda ) then
  setenv CUDA_INCLUDE_DIRS /usr/include/cuda
  setenv CUDA_INC_PATH /usr/include/cuda
endif
