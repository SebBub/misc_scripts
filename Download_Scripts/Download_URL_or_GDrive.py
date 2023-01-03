# https://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive/39225039#39225039

import gdown
import urllib

def download_file(id_or_url, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    if id_or_url.startswith('http:') or id_or_url.startswith('https:'):
        print(f'http download of "{id_or_url}"...')
        try:
            #ssl._create_default_https_context = ssl._create_unverified_context  # "workaround" the certification
            urllib.request.urlretrieve(id_or_url, destination)
        except Exception:
            print(f"Cannot download {id_or_url}")

    else:
        print(f'GoogleDrive download')
        file_id = "1GsZOlbMbhWdItUR5r1P3ZHK7G6QdyW4u"
        url = "https://drive.google.com/uc?id={}".format(file_id)
        gdown.download(url)
        
    print("DONE")

if __name__ == "__main__":
    import sys
    if len(sys.argv) is not 3:
        print("Usage: python google_drive.py drive_file_id_or_URL destination_file_path")
    else:
        # TAKE ID FROM SHAREABLE LINK or use http... url
        file_id_or_url = sys.argv[1]
        # DESTINATION FILE ON YOUR DISK
        destination = sys.argv[2]
        download_file(file_id_or_url, destination)