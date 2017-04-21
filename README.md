Simple project aimed to detect and take picture(one picture for each moving object!) if someone passed in camera view.  
Project uses opencv 3.x and opencv_contrib extra modules.

#Usage
Run detection.py without parameters to use web camera or specify video file or stream with -v param. Examples:
```bash
./detection.py -v 1.mp4
./detection.py -v rtsp://192.168.10.10:554/s0
```

#Note: building opencv with opencv_contrib
```bash
wget https://github.com/opencv/opencv/archive/3.2.0.zip -O opencv-3.2.0.zip
wget https://github.com/opencv/opencv_contrib/archive/3.2.0.zip -O opencv_contrib-3.2.0.zip
unzip opencv-3.2.0.zip
unzip opencv_contrib-3.2.0.zip
cd opencv-3.2.0
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_CUDA=OFF -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.2.0/modules ..
make -j 8
sudo make install
```
