#!/bin/sh
echo "Proceeding to install neccesary packages"
sudo apt-get tightvncserver build-essential cmake pkg-config libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev libgtk2.0-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libatlas-base-dev gfortran python2.7-dev python-numpy
echo "Removing wolfram-engine to save memory"
sudo apt-get purge wolfram-engine
echo "Downloading pip"
wget https://bootstrap.pypa.io/get-pip.py
echo "Installing pip"
sudo python get-pip.py
echo "Downloading OpenCV 2.4.10 from source"
wget -O opencv-2.4.10.zip http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.10/opencv-2.4.10.zip/download
echo "Unzipping OpenCV 2.4.10"
unzip opencv-2.4.10.zip
echo "Entering OpenCV 2.4.10 directory"
cd opencv-2.4.10
echo "Creating build directory"
mkdir build
echo "Entering build directory"
cd build
echo "Using CMake to configure compiling of OpenCV"
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_NEW_PYTHON_SUPPORT=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON  -D BUILD_EXAMPLES=ON ..
echo "Making...This will take a while (about 3 hours on a RPi2)"
make
echo "Installing compiled OpenCV"
sudo make install
sudo ldconfig
echo "Finished!"
echo "Attempting test of OpenCV install on python2.7"
python2.7 test.py
echo "If no errors were thrown, the install is ready!"
echo "Setting up scripts"
chmod +x run.sh
chmod +x vnc_720p.sh
echo "Scripts ready for use!"
