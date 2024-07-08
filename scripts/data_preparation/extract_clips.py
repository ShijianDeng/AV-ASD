import subprocess
import os
import pandas as pd

# Set paths
csv_file_path = 'dataset/csvs/dataset.csv'
original_videos_dir = 'dataset/original_videos'
clips_video_dir = 'dataset/clips_video'
clips_audio_dir = 'dataset/clips_audio'

# Create output directories if they don't exist
os.makedirs(clips_video_dir, exist_ok=True)
os.makedirs(clips_audio_dir, exist_ok=True)

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Function to run FFmpeg commands
def run_ffmpeg(command):
    subprocess.run(command, shell=True, check=True)

num_failed = 0

# Process each row in the CSV
for index, row in df.iterrows():
    # Split Video_ID into parts
    parts = row['Video_ID'].rsplit('_', 2)
    if len(parts) < 3:
        print(f"Invalid format for Video_ID: {row['Video_ID']}")
        continue
    video_id = '_'.join(parts[:-2])
    start_time = int(parts[-2])
    end_time = int(parts[-1])
    duration = end_time - start_time
    
    # Find the original video file
    original_video_path = None
    for ext in ['.mp4', '.mkv', '.webm']:
        possible_path = os.path.join(original_videos_dir, f"{video_id}{ext}")
        if os.path.exists(possible_path):
            original_video_path = possible_path
            break

    if not original_video_path:
        print(f"Original video for {video_id} not found.")
        continue

    # Set output paths for clips
    video_clip_path = os.path.join(clips_video_dir, f"{video_id}_{start_time}_{end_time}.mp4")
    audio_clip_path = os.path.join(clips_audio_dir, f"{video_id}_{start_time}_{end_time}.wav")
    
    # Create FFmpeg commands
    video_command = f"ffmpeg -n -ss {start_time} -t {duration} -i \"{original_video_path}\" -c:v libx264 -c:a aac \"{video_clip_path}\""
    audio_command = f"ffmpeg -n -ss {start_time} -t {duration} -i \"{original_video_path}\" \"{audio_clip_path}\""

    try:
        run_ffmpeg(video_command)
        run_ffmpeg(audio_command)
    except subprocess.CalledProcessError as e:
        num_failed += 1
        print(f"Error processing {video_id}: {e}")

print(f"Processing completed. {num_failed} files failed.")
