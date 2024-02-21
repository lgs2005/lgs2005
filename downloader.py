import yt_dlp
import shutil
import sys
import os
import pathlib

help_str = 'Usage: python downloader.py <url> <foldername> <device> <template>'
temp_folder = './_downloader_temp'
temp_template = f'{temp_folder}/%(title)s.%(ext)s'

def log(message: str):
    print(f'[downloader.py]: {message}')

def main():
    if len(sys.argv) != 5:
        log('Wrong argument count.')
        log(help_str)
        return
    
    [_, url, foldername, device, template] = sys.argv
    
    if not device in ['pc', 'mb']:
        log('Unknown device.')
        return
    
    if not template in ['list', 'split']:
        log('Unknown template.')
        return
    
    download_path = None
    
    if device == 'pc':
        download_path = f'./{foldername}'
    elif device == 'mb':
        download_path = f'/storage/emulated/0/Music/{foldername}'

    if download_path == None:
        log('Couldn\'t resolve download path.')
        return

    output_template = None

    if template == 'list':
        output_template = {
            'default': f'{download_path}/%(title)s.%(ext)s'
        }
    elif template == 'split':
        output_template = {
            'default': temp_template,
            'chapter': f'{download_path}/%(section_title)s.%(ext)s'
        }
    
    if output_template == None:
        log('Couldn\'t resolve template.')
        return
    
    log(f'Will download to {output_template}.')
    # FUCKIGN,.                                        FIRNANTUBTG
    # input('[downloader.py]: Confirm?')
    # Bmv thanmks for the idea
    log(f'Confirm?')
    input()
    
    if device == 'mb':
        os.system('termux-wake-lock')

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

    if template in ['split']:
        postprocessors.append({
            'key': 'FFmpegSplitChapters',
            'force_keyframes': False,
        })

    file_list = []

    def push_file_name_hook(info):
        nonlocal file_list

        if info.get('status') == 'finished':
            path = pathlib.Path(info.get('filename'))
            final_path = path.with_suffix('.mp3')
            file_list.append(str(final_path))

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
        'progress_hooks': [push_file_name_hook]
    }) as downloader:
        downloader.download(url)

    if os.path.exists(temp_folder):
        log('Deleting temp folder')
        shutil.rmtree(temp_folder)

    log('Generating m3u file')
    
    file = open(download_path + '.m3u', 'w', encoding='utf-8')
    file.write("#EXTM3U\n")

    for name in file_list:
        file.write(f"{name}\n")

    file.close()
    log('Done')

    if device == 'mb':
        # }Uhmmm this doent work Xdd
        # Haha well         i uhm ,,,,,,,,,,,,,,, Wrong.
        log(f'Running termux media rescan')
        os.system(f'termux-media-scan -r "{download_path}"')
        os.system(f'termux-media-scan "{download_path}.m3u"')
        os.system('termux-wake-unlock')
        os.system(f'termux-notification --content "Download Complete: {foldername}"')

if __name__ == '__main__':
    if os.path.exists('./underscores - wallsocket'):
        shutil.rmtree('./underscores - wallsocket')

    try:
        main()
    except KeyboardInterrupt:
        log('Interrupted.') # Newline fans?
