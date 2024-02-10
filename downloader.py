import yt_dlp
import shutil
import sys
import os

help_str = '[downloader.py]: Usage: python downloader.py <url> <foldername> <device> <template>'
temp_folder = './_downloader_temp'
temp_template = f'{temp_folder}/%(title)s.%(ext)s'

def main():
    if len(sys.argv) != 5:
        print('[downloader.py]: Wrong argument count.')
        print(help_str)
        return
    
    [_, url, foldername, device, template] = sys.argv
    
    if not device in ['pc', 'pp']:
        print('[downloader.py]: Unknown device.')
        return
    
    if not template in ['order', 'free', 'ordersplit', 'freesplit']:
        print('[downloader.py]: Unknown template.')
        return
    
    download_path = None
    
    if device == 'pc':
        download_path = f'./{foldername}'
    elif device == 'pp':
        download_path = f'/storage/emulated/0/Music/{foldername}'

    if download_path == None:
        print('[downloader.py]: Couldn\'t resolve download path.')
        return

    output_template = None

    if template == 'order':
        output_template = {
            'default': f'{download_path}/%(playlist_index)s - %(title)s.%(ext)s'
        }
    elif template == 'free':
        output_template = {
            'default': f'{download_path}/%(title)s.%(ext)s'
        }
    elif template == 'ordersplit':
        output_template = {
            'default': temp_template,
            'chapter': f'{download_path}/%(section_number)02d - %(section_title)s.%(ext)s'
        }
    elif template == 'freesplit':
        output_template = {
            'default': temp_template,
            'chapter': f'{download_path}/%(section_title)s.%(ext)s'
        }
    
    if output_template == None:
        print('[downloader.py]: Couldn\'t resolve template.')
        return
    
    print(f'[downloader.py]: Will download to {output_template}.')
    input('[downloader.py]: Confirm?')
    
    postprocessors = [
        {
            'key': 'FFmpegExtractAudio',
            'nopostoverwrites': False,
            'preferredcodec': 'mp3',
            'preferredquality': 0,
        },
        {
            'key': 'FFmpegConcat',
            'only_multi_video': True,
            'when': 'playlist',
        }
    ]

    if template in ['ordersplit', 'freesplit']:
        postprocessors.append({
            'key': 'FFmpegSplitChapters',
            'force_keyframes': False,
        })

    with yt_dlp.YoutubeDL({
        'extract_flat': 'discard_in_playlist',
        'final_ext': 'mp3',
        'format': 'ba',
        'fragment_retries': 10,
        'ignoreerrors': True,
        'outtmpl': output_template,
        'overwrites': False,
        'postprocessors': postprocessors,
        'retries': 10,
        'retry_sleep_functions': { 'http': lambda: 1 },
    }) as downloader:
        downloader.download(url)

    if os.path.exists(temp_folder):
        print('[downloader.py]: Deleting temp folder')
        shutil.rmtree(temp_folder)

    print('[downloader.py]: Generating m3u file')
    
    file_list = os.listdir(download_path)
    file_list.sort()

    file = open(download_path + '.m3u', 'w', encoding='utf-8')
    file.write("#EXTM3U\n")

    for name in file_list:
        print(f'[downloader.py]: m3u entry: {name}')
        file.write(f"{foldername}/{name}\n")

    file.close()

    if device == 'pp':
        # }Uhmmm this doent work Xdd
        print(f'[downloader.py]: Running termux media rescan')
        os.system(f'termux-media-scan -r {download_path}')
        os.system(f'termux-media-scan {download_path}.m3u')

if __name__ == '__main__':
    main()