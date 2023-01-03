
import os
import urllib.request


out_file = 'manual.pdf'

#url = "https://u.pcloud.link/publink/show?code=XZ1USJXZ2taEoqh485ygPUfk8MAInjW65ls7"
url = "https://nimbus.igb-berlin.de/index.php/s/q7eTtjBfWR9EteQ"
try:
	urllib.request.urlretrieve(url, out_file)
	print("Downloaded: "+str(out_file))
except:
	errors.append(url)

print("DONE")