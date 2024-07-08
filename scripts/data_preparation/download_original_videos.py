import os
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed

def video_exists(name, path_data, extensions):
    """Check if a video file exists for any of the given extensions."""
    for ext in extensions:
        if os.path.exists(os.path.join(path_data, f"{name}.{ext}")):
            return True
    return False

def download(name, path_data):
    # List of possible video file extensions
    video_extensions = ['mp4', 'webm', 'mkv']

    # Check if the video file already exists in any of the known formats
    if video_exists(name, path_data, video_extensions):
        print(f"Video {name} already downloaded in one of the supported formats. Skipping...")
        return None

    link_prefix1 = "https://www.youtube.com/watch?v="
    link_prefix2 = "https://www.youtube.com/shorts/"
    link_prefix3 = "https://www.facebook.com/watch/?v="

    link1 = link_prefix1 + name
    link2 = link_prefix2 + name
    link3 = link_prefix3 + name

    file_path = os.path.join(path_data, name) + ".%(ext)s"  # yt-dlp will choose the best format

    command1 = 'yt-dlp ' + link1.split('&')[0] + " -o " + '"' + file_path + '"'
    command2 = 'yt-dlp ' + link2.split('&')[0] + " -o " + '"' + file_path + '"'
    command3 = 'yt-dlp ' + link3.split('&')[0] + " -o " + '"' + file_path + '"'

    # Try downloading the video from different sources
    if os.system(command1) != 0:
        if os.system(command2) != 0:
            if os.system(command3) != 0:
                print(f"{name} cannot be found online")
                return name
    return None

def process_video(args):
    name, path_data = args
    try:
        return download(name, path_data)
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    csv_pth = 'dataset/csvs/dataset.csv'
    video_pth = 'dataset/original_videos'
    if not os.path.exists(video_pth):
        os.makedirs(video_pth)

    df = pd.read_csv(csv_pth)
    df['Original_ID'] = df['Video_ID'].str.rsplit('_', n=2).str[0]
    data = df.drop_duplicates(subset=['Original_ID']).reset_index(drop=True)

    args = [(data['Original_ID'][i], video_pth) for i in range(len(data['Original_ID']))]

    lost_videos = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_video, arg) for arg in args]
        for future in as_completed(futures):
            result = future.result()
            if result:
                lost_videos.append(result)

    print(f"{len(lost_videos)} videos cannot be found online:")
    for name in lost_videos:
        print(name)
    print(f"{len(os.listdir(video_pth))} out of {len(data)} videos downloaded.")
