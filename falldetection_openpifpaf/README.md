# Fall Detection using Pose Estimation

## Introduction
Fall Detection model based on [OpenPifPaf](https://github.com/vita-epfl/openpifpaf)

PyPI Library: https://pypi.org/project/openpifpaf/

The detection can run on both GPU and CPU, on multiple videos, RTSP streams, and webcams/USB cameras. Unlike most open-source fall detection models that work on large single subjects, this improved model integrates a person tracker that can detect falls in scenes with more than one person.

## Demo Videos
![Walking Trip](https://github.com/cwlroda/falldetection_openpifpaf/blob/master/media/walking_trip.gif)
![Stubbed Toe](https://github.com/cwlroda/falldetection_openpifpaf/blob/master/media/stubbed_toe.gif)
![Drunk](https://github.com/cwlroda/falldetection_openpifpaf/blob/master/media/drunk.gif)

Video credits: 50 Ways to Fall ([Link](https://www.youtube.com/watch?v=8Rhimam6FgQ)), ran on a single NVIDIA Quadro P1000

## Test Results
UR Fall Detection Dataset ([Link](http://fenix.univ.rzeszow.pl/~mkepski/ds/uf.html)), tested on two NVIDIA Quadro GV100s.
- Precision: 100%
- Recall: 83.33%
- F1 Score: 90.91%

_Note: Due to lack of available datasets, false positives and true negatives were not tested._

## Environment
- Ubuntu 18.04 x86_64
- Python 3.7.6
- Anaconda 3
- CUDA 10.2

## Usage
**Setup Conda Environment**
```console
$ conda create --name falldetection_openpifpaf python=3.7.6
$ conda activate falldetection_openpifpaf
```

**Clone Repository**
```console
$ git clone https://github.com/cwlroda/falldetection_openpifpaf.git
```

**Download OpenPifPaf 0.11.9 (PyPI)**
```console
$ pip3 install openpifpaf
```

**Copy Source Files**
```console
$ cd {home_dir}/anaconda3/lib/python3.7/site-packages/openpifpaf
Replace ALL files in that folder with the files in falldetection_openpifpaf
```

**Install Dependencies**
```console
$ pip3 install -r requirements.txt
```

**Execution**

For videos/RTSP streams, navigate to _config/config.xml_ to edit the video/RTSP stream path, then run:
```console
$ python3 -m openpifpaf.video --show
$ (use --help to see the full list of command line arguments)
```
For webcams/USB cameras, run:
```console
$ python3 -m openpifpaf.video --source {CAMERA_ID} --show
$ (use --help to see the full list of command line arguments)
```

## Example Usage

1. First activate virtual environment  
   
    ```console
    conda activate falldetection_openpifpaf
    ```

2. Running the model

    - Run model on video:

        ```console
        python3 -m openpifpaf.video --source=videos/video.mp4 --show --scale=0.2
        ```

    - Run model on webcam (Might need to kill active camera first if already in use):

        ```console
        sudo fuser -k /dev/video0
        python3 -m openpifpaf.video --source=0 --show
        ```

    - Run model from streaming:

        ```console
        python3 -m openpifpaf.video --source=url --show 
        --scale=0.2
        ```
    
    - Expose `/predict` endpoint to predict by frame:

        ```console
        python3 -m openpifpaf.video --source=server --show 
        ```

3. After making changes to the model

    - Navigate to your Anaconda environment's openpifpaf directory

        ```
        cd ~/anaconda3/envs/falldetection_openpifpaf/lib/python3.7/site-packages/openpifpaf
        ```

    - Remove all existing files

        ```console
        rm -rf *
        ```

    - Copy all files from your cloned repository

        ```console
        cp -r ~/Documents/unitree-fall-detection-pipeline/falldetection_openpifpaf/* .
        ```

## Citations
PifPaf: Composite Fields for Human Pose Estimation ([Link](http://openaccess.thecvf.com/content_CVPR_2019/html/Kreiss_PifPaf_Composite_Fields_for_Human_Pose_Estimation_CVPR_2019_paper.html))

    @InProceedings{Kreiss_2019_CVPR,
        author = {Kreiss, Sven and Bertoni, Lorenzo and Alahi, Alexandre},
        title = {PifPaf: Composite Fields for Human Pose Estimation},
        booktitle = {Proceedings of the IEEE/CVF Conference on
                    Computer Vision and Pattern Recognition (CVPR)},
        month = {June},
        year = {2019}
    }

If you use the dataset above, please cite the following work: ([Link](http://home.agh.edu.pl/~bkw/research/pdf/2014/KwolekKepski_CMBP2014.pdf))

    Bogdan Kwolek, Michal Kepski,
    Human fall detection on embedded platform using depth maps and wireless accelerometer,
    Computer Methods and Programs in Biomedicine,
    Volume 117,
    Issue 3,
    December 2014,
    Pages 489-501,
    ISSN 0169-2607
