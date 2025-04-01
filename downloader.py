from yt_dlp import YoutubeDL
import os

def on_progress(d):
    if d['status'] == 'downloading':
        print(f"\r⬇️ Downloading: {d.get('_percent_str','0%')} | Speed: {d.get('_speed_str','N/A')} | ETA: {d.get('_eta_str','N/A')}", end='')
    elif d['status'] == 'finished':
        print("\n✅ Download Complete!")

def choose_format(formats):
    print("\n📋 Available Formats:")
    for i, f in enumerate(formats):
        note = ""
        if f.get('filesize'):
            size = f['filesize'] / 1024 / 1024
            note = f" | Size: {size:.2f}MB"
        print(f"{i+1}. {f['ext']} ({f['format_note']}){note}")

    while True:
        try:
            choice = int(input("\nChoose a format (enter number): "))
            if 1 <= choice <= len(formats):
                return formats[choice-1]['format_id']
            print("Invalid number!")
        except ValueError:
            print("Please enter a number!")

def main():
    url = input("🎬 Enter YouTube URL: ")

    ydl_opts = {
        'progress_hooks': [on_progress],
        'outtmpl': os.path.join(os.getcwd(), 'Downloads', '%(title)s.%(ext)s'),
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # Filter unique formats
            unique_formats = {f['format_id']: f for f in formats if f.get('format_note')}.values()
            format_id = choose_format(list(unique_formats))
            
            ydl.params['format'] = format_id
            print(f"\n🚀 Downloading: {info['title']}")
            ydl.download([url])
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()