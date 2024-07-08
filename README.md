# AV-ASD

## Install Dependencies
```
pip install -r requirements.txt
```

## Data Preparation

### 1. Download Original Videos from YouTube and Facebook

You can find original video URLs in ```dataset/csvs```.

To download the original videos, you can use the command:
```
python scripts/data_preparation/download_original_videos.py
```

Note: Some original videos may no longer be available online.

### 2. Extract Video Clips and Audio Clips from Original Videos

Make sure that a pre-compiled version of FFmpeg, which includes libx264 support, has been installed. If not, you can use the following command to install it:
<details>
<summary>Show more</summary>

```
sudo apt update
sudo apt install ffmpeg libx264-dev
```

If this doesn't work or you do not have sudo privileges, you can try:
```
conda install -c conda-forge ffmpeg
```
</details>

Then you can run the command to extract video and audio clips:
```
python scripts/data_preparation/extract_clips.py
```