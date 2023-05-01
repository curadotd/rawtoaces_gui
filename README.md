# RAW to ACES GUI

<img src="/images/rawtoaces_gui.jpg" alt="Alt text" title="RawtoAces GUI">

## Table of Contents
1. [Introduction](#introduction)
2. [Package Contents](#package-contents)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)

## Introduction
The RAW to ACES Gui, is a helper tool to convert digital camera RAW files to ACES container files containing image data encoded according to the Academy Color Encoding Specification (ACES) as specified in [SMPTE 2065-1](http://ieeexplore.ieee.org/document/7289895/).  Using the underlining software package from https://github.com/AcademySoftwareFoundation/rawtoaces.git.

1. The gui allows the user to input an image, then select a few options, like convert into a sequence of files, rename the files with padding and move them into a exr subfolder.
   The output image complies with the ACES Container specification [(SMPTE S2065-4)](http://ieeexplore.ieee.org/document/7290441).

The original source code for rawtoaces was forked to add support to the latest version of libraw v0.21.1, add compatibility to CR3 canon files for example.
Provided here: https://github.com/mjbacurado/rawtoaces.git

## Package Contents

The source code contains the following:

* [`bin/`](./rawtoaces_gui) - Helper shelscritp for runing the gui.
* [`python/`](./main.py) - gui python run file.
* [`install_rawtoaces_mac`](install_rawtoaces_mac) - Helper shelscritp to install rawtoaces and setup on MacOs
* [`install_rawtoaces_linux`](install_rawtoaces_linux) - Helper shelscritp to install rawtoaces and setup on Linux, tested in rocky linux.

## Prerequisites
###### pip

https://pypi.org/project/pip/

###### Pyside6

https://pypi.org/project/PySide6/

pip install PySide6

###### Raw to Aces 
https://github.com/mjbacurado/rawtoaces#installation

* macOS
	
	Install homebrew if not already installed
	
	```sh
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	```
    Remember to add the paths to your .zprofile as instructed an the end of the installation.
	
	Install dependencies
	
	```sh
	$ brew install cmake ilmBase autoconf automake libtool pkg-config boost eigen aces_container gcc glog libraw ceres-solver
	```
    ```sh
    $ git clone https://github.com/ceres-solver/ceres-solver.git
    ```
    #Change to version 1.14.0
    ```sh
    $ git checkout 1.14.0
    ```
    #unlink ceres-solver from homebrew
    ```sh
    $ brew unlink ceres-solver
    ```
    ```sh
    $ mkdir build_ceres && cd build_ceres
    ```
    ```sh
    $ cmake \
    -DCMAKE_INSTALL_PREFIX=/opt/homebrew/Cellar/ceres-solver/1.14.0 \
    -DBUILD_SHARED_LIBS=ON -DBUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF \
    ..
    ```
    ```sh
    $ make -j 8
    ```
    ```sh
    $ make install
    ```
    #link ceres-solver to homebrew
    ```sh
    $ brew link ceres-solver
    ```
    #Raw to Aces build and install.
    ```sh
    $ git clone https://github.com/mjbacurado/rawtoaces.git
    ``` 
    ```sh
    $ cmake \
    -DCMAKE_CXX_STANDARD=11 -DCMAKE_C_COMPILER=/opt/homebrew/Cellar/gcc/12.2.0/bin/gcc-12 \
    -D_IlmBase_HINT_LIB=/opt/homebrew/opt/ilmbase/lib \
    -D_IlmBase_HINT_INCLUDE=/opt/homebrew/opt/ilmbase/include \
    -D_libraw_HINT_LIB=/opt/homebrew/opt/libraw/install/lib \
    -D_libraw_HINT_INCLUDE=/opt/homebrew/opt/libraw/install/include \
    -DCERES_INCLUDE_DIRS=/opt/homebrew/opt/ceres-solver/include \
    -DCERES_LIBRARY_DIRS=/opt/homebrew/opt/ceres-solver/lib \
    -DCMAKE_INSTALL_PREFIX=/opt/homebrew/Cellar/rawtoaces/master ..
    ```
    ```sh
   $  make
    ```
    ```sh
    $ make install
    ```
    #link rawtoaces to homebrew
    ```sh
    $ brew link rawtoaces
    ```
    #set some needed environment variables
    ```sh
    $ echo "export LD_LIBRARY_PATH=/opt/homebrew/lib" >> ~/.zprofile
    ```
    ```sh
    $ echo "export LD_INCLUDE_DIR=/opt/homebrew/include:/opt/homebrew/include/rawtoaces" >> ~/.zprofile
    ```
    ```sh
    $ echo "export AMPAS_DATA_PATH=/opt/homebrew/include/rawtoaces/data" >> ~/.zprofile
    ```
    #install rawto aces gui
    #install python dependencies
    ```sh
    $ pip install pyside6
    ```
    ```sh
    $ mkdir /opt/homebrew/Cellar/rawtoaces_gui/master
    ```
    ```sh
    $ cp -r python /opt/homebrew/Cellar/rawtoaces_gui/master
    ```
    ```sh
    $ cp -r bin /opt/homebrew/Cellar/rawtoaces_gui/master
    ```
    ```sh
    $ brew link rawtoaces_gui
    ```


* RockyLinux
	
    #enable powertools
    ```sh
    sudo dnf install dnf-plugins-core
    ```
    ```sh
    sudo dnf install epel-release
    ```
    ```sh
    sudo dnf update
    ```
    ```sh
    sudo dnf config-manager --enable crb
    ```
    ```sh
    sudo dnf install cmake autoconf automake libtool pkg-config boost-devel \
    gcc glog-devel gflags-devel openexr-devel eigen3-devel g++ libjpeg-devel \
    libjasper-devel lcms2-devel suitesparse-devel metis-devel tbb-devel blas-devel \
    lapack-devel openblas-serial dcraw
    ```
    ```sh
    git clone https://github.com/mjbacurado/rawtoaces.git
    ```
    ```sh
    cd rawtoaces
    ```
    ```sh
    mkdir _build && cd _build
    ```
    ```sh
    mkdir raw_to_aces_deps_aces_container && cd raw_to_aces_deps_aces_container
    ```
    ```sh
    git clone https://github.com/miaoqi/aces_container.git src
    ```
    ```sh
    cd src
    ```
    ```sh
    mkdir build && cd build
    ```
    ```sh
    cmake ..
    ```
    ```sh
    make -j 4
    ```
    ```sh
    sudo make install
    ```
    ```sh
    mkdir raw_to_aces_deps_libraw && cd raw_to_aces_deps_libraw
    ```
    ```sh
    git clone https://github.com/LibRaw/LibRaw-cmake.git src
    ```
    ```sh
    cd src
    ```
    ```sh
    git clone https://github.com/LibRaw/LibRaw.git libraw
    ```
    ```sh
   cd LibRaw-cmake && mkdir build && cd build
    ```
    ```sh
    cmake -DLIBRAW_PATH=/home/mcurado/git/rawtoaces/_build/raw_to_aces_deps_libraw/src/libraw -DENABLE_DCRAW_DEBUG=ON ..
    ```
    ```sh
    make -j 4
    ```
    ```sh
    sudo make install
    ```
    ```sh
    mkdir raw_to_aces_deps_ceres_solver && cd raw_to_aces_deps_ceres_solver
    ```
    ```sh
    git clone https://github.com/ceres-solver/ceres-solver.git src
    ```
    ```sh
    cd src
    ```
    #Change to version 1.14.0
    ```sh
    git checkout 1.14.0
    ```
    ```sh
    mkdir build_ceres && cd build_ceres
    ```
    ```sh
    cmake \
    -DBUILD_SHARED_LIBS=ON -DBUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF \
    ..
    ```
    ```sh
    make -j 8
    ```
    ```sh
    make install
    ```
    ```sh
    cd $build_path/rawtoaces/_build
    ```
    #Raw to Aces build and install.
    ```sh
    cmake \
    -DCMAKE_CXX_STANDARD=11 -DCMAKE_C_COMPILER=/usr/bin/gcc \
    -D_IlmBase_HINT_LIB=/usr/lib64 \
    -DIlmBase_INCLUDE_DIR=/usr/include/Imath \
    -D_libraw_HINT_LIB=/usr/local/lib64 \
    -D_libraw_HINT_INCLUDE=/usr/local/include/libraw \
    -DCERES_INCLUDE_DIRS=/usr/local/include/ceres \
    -DCERES_LIBRARY_DIRS=/usr/local/lib64 \
    -DAcesContainer_INCLUDE_DIRS=/usr/local/include/aces/ \
    -DAcesContainer_LIBRARY_DIRS=/usr/local/lib \
    ..
    ```
    ```sh
    make -j 4
    ```
    ```sh
    suod make install
    ```

    #set some needed environment variables
    ```sh
    echo "export LD_LIBRARY_PATH=/usr/local/lib" >> ~/.bashrc
    echo "export LD_INCLUDE_DIR=/usr/local/include/rawtoaces" >> ~/.bashrc
    echo "export AMPAS_DATA_PATH=/usr/local/rawtoaces/data" >> ~/.bashrc
    ```

    cd $build_path/rawtoaces/_build

    #install rawtoaces_gui for macOS
    #Get rawtoaces_gui source
    ```sh
    git clone https://github.com/mjbacurado/rawtoaces_gui.git
    ```
    ```sh
    cd rawtoaces_gui
    ```

    #install python dependencies
    ```sh
    pip install pyside6
    ```
    ```sh
    cp -r python /usr/local/rawtoaces_gui
    ```
    ```
    cp -r bin /usr/local/bin
    ```sh

## Usage

### Overview

Input a Raw Camera image for example a .CR3 image file in the file path slot.

Choose if you would like to create a sequence, create a exr subfolder and or change the image name.

Then choose the conversion options for `rawtoaces`.

`rawtoaces` uses one of three methods to convert RAW image files to ACES.

1. Camera spectral sensitivities and illuminant spectral power distributions
2. Camera file metadata
3. Camera data included in the `libraw` software

The preferred, and most accurate, method of converting RAW image files to ACES is to use camera spectral sensitivities and illuminant spectral power distributions, if available.  If spectral sensitivity data is available for the camera, `rawtoaces` uses the method described in Academy document [P-2013-001](http://j.mp/P-2013-001) (.pdf download).

While preferred, camera spectral sensitivity data is not commonly known to general users. When that is the case, `rawtoaces` can use either the metadata embedded in the camera file or camera data included in `libraw` to approximate a conversion to ACES.

### Help message

A help message with a description of all command line options can be obtained by typing the following command:
	
	$ rawtoaces --help
	rawtoaces - convert RAW digital camera files to ACES

	Usage:
  	  rawtoaces file ...
  	  rawtoaces [options] file
  	  rawtoaces --help
  	  rawtoaces --version

	IDT options:
  	  --help                  Show this screen
  	  --version               Show version
  	  --wb-method [0-4]       White balance factor calculation method
	                            0=white balance using file metadata 
	                            1=white balance using user specified illuminant [str] 
	                            2=Average the whole image for white balance
	                            3=Average a grey box for white balance <x y w h>
	                            4=Use custom white balance  <r g b g>
	                            (default = 0)
  	  --mat-method [0-2]      IDT matrix calculation method
	                            0=Calculate matrix from camera spec sens
	                            1=Use file metadata color matrix
	                            2=Use adobe coeffs included in libraw
	                            (default = 0)
	                            (default = /usr/local/include/rawtoaces/data/camera)
  	  --headroom float        Set highlight headroom factor (default = 6.0)
  	  --cameras               Show a list of supported cameras/models by LibRaw
  	  --valid-illums          Show a list of illuminants
  	  --valid-cameras         Show a list of cameras/models with available
	                          spectral sensitivity datasets

	Raw conversion options:
  	  -c float                Set adjust maximum threshold (default = 0.75)
  	  -C <r b>                Correct chromatic aberration
  	  -P <file>               Fix the dead pixels listed in this file
  	  -K <file>               Subtract dark frame (16-bit raw PGM)
  	  -k <num>                Set the darkness level
  	  -S <num>                Set the saturation level
  	  -n <num>                Set threshold for wavelet denoising
  	  -H [0-9]                Highlight mode (0=clip, 1=unclip, 2=blend, 3+=rebuild) (default = 0)
  	  -t [0-7]                Flip image (0=none, 3=180, 5=90CCW, 6=90CW)
  	  -j                      Don't stretch or rotate raw pixels
  	  -W                      Don't automatically brighten the image
  	  -b <num>                Adjust brightness (default = 1.0)
  	  -q [0-3]                Set the interpolation quality
  	  -h                      Half-size color image (twice as fast as "-q 0")
  	  -f                      Interpolate RGGB as four colors
  	  -m <num>                Apply a 3x3 median filter to R-G and B-G
  	  -s [0..N-1]             Select one raw image from input file
  	  -G                      Use green_matching() filter
  	  -B <x y w h>            Use cropbox
	
	Benchmarking options:
  	  -v                      Verbose: print progress messages (repeated -v will add verbosity)
  	  -F                      Use FILE I/O instead of streambuf API
  	  -d                      Detailed timing report
  	  -E                      Use mmap()-ed buffer instead of plain FILE I/O
