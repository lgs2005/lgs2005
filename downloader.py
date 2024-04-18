import yt_dlp
import shutil
import sys
import os

help_str = 'Usage: python downloader.py <url> <foldername> <device> <template>'
temp_folder = './_downloader_temp'
temp_template = f'{temp_folder}/%(title)s.%(ext)s'

def log(message: str):
    print(f'[downloader.py]: {message}')

def main(args):
    if len(args) != 5:
        log('Wrong argument count.')
        log(help_str)
        return
    
    [_, url, foldername, device, template] = args
    
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

    if template == 'split':
        postprocessors.append({
            'key': 'FFmpegSplitChapters',
            'force_keyframes': False,
        })

    file_list = []

    def file_list_hook(info):
        # making sure befcuase GOF DUFKCING KNOWS what this fuckin lnguage
        # scoping rules are like holysh it PYthon WHY CNAYT YOU BE NORMAL
        nonlocal file_list

        if template == 'list':
            if info.get('postprocessor') == 'MoveFiles' and info.get('status') == 'finished':
                file_list.append(info.get('info_dict').get('filepath'))
        elif template == 'split':
            if info.get('postprocessor') == 'SplitChapters' and info.get('status') == 'finished':
                # How i miss javascript
                chapter_list = info.get('info_dict').get('chapters')
                chapter_files = map(lambda v: v.get('filepath'), chapter_list)
                file_list.extend(chapter_files)

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
        'postprocessor_hooks': [file_list_hook]
    }) as downloader:
        downloader.download(url)

    if os.path.exists(temp_folder):
        log('Deleting temp folder')
        shutil.rmtree(temp_folder)

    log('Generating m3u file')
    
    m3u_path = f'{download_path}.m3u'
    entries = []

    try:
        with open(m3u_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines.pop(0)
            entries.extend(lines)
    except FileNotFoundError:
        pass
    
    for name in file_list:
        path = f'{name}\n'
        
        if path not in entries:
            entries.append(path)
    
    # You kno  whyam i using Python when i could just,. ,,, InstallnoodOOH right i need otyuubedl
    
    with open(m3u_path, 'w', encoding='utf-8') as file:
        file.write(f"#EXTM3U\n{''.join(entries)}")

    log('Done')

    if device == 'mb':
        # }Uhmmm this doent work Xdd
        # Haha well         i uhm ,,,,,,,,,,,,,,, Wrong. (NOT! DUMBASS
        # It work now :?
        log(f'Running termux media rescan')
        os.system(f'termux-media-scan -r "{download_path}"')
        os.system(f'termux-media-scan "{download_path}.m3u"')
        os.system('termux-wake-unlock')
        os.system(f'termux-notification --content "Download Complete: {foldername}"')

if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        log('Interrupted.') # Newline fans?
