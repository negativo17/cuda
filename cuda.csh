if ( -x /usr/bin/cuda-g++ ) then
  setenv HOST_COMPILER /usr/bin/cuda-g++
endif

if ( -x /usr/libexec/cuda/open64/bin/nvopencc ) then
  setenv PATH ${PATH}:/usr/libexec/cuda/open64/bin
endif
