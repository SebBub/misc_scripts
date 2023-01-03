from pathlib import Path

def decompress(folder, compression):
    import shutil
    slice_object = slice(0,-len(compression))

    out_folders = []

    i=0
    print('Starting decompression')
    files = list(folder.glob('*.' + compression))
    for file in files:
        if (file.stat().st_size / (1024 ** 2)) < 40:  # ignore only partially loaded files, e.g. initially aborted downloads
            print(file.name + ' not decompressed, possibly unfinished download...')
            continue
        else:
            path = file.parent / file.parts[-1][slice_object]
            shutil.unpack_archive(file, path, format=compression)
            print('Successfully decompressed ' + str(file.parts[-1][slice_object]))
            file.unlink() #!! deletes the local file after successful decompression !! comment out if you want to keep
            i=i+1
    print('Successfully decompressed ' + str(i) + ' files!')

if __name__ == "__main__":
    path = Path(r"H:\01Satellite_Data\Rwanda\Sentinel-2")
    compression = "zip"
    decompress(path, compression)