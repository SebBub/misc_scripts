
import gdown

file_id = "1GsZOlbMbhWdItUR5r1P3ZHK7G6QdyW4u"
url="https://drive.google.com/uc?id={}".format(file_id)
gdown.download(url)

print("DONE")