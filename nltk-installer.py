import os
import requests
import shutil
import sys
import zipfile
try:
    from cStringIO import StringIO
except:
    from StringIO  import StringIO

sitepath = os.path.join(os.path.expanduser("~"),
                       "Documents",
                       "site-packages")
nltkpath = os.path.join(sitepath,
                       "nltk")
if os.path.exists(nltkpath):
    print("NLTK already installed")
    sys.exit()

def error(msg):
    print >>sys.stderr, msg
    sys.exit()

def geturl(release):
    pkg = [i for i in release if i["url"].endswith(".zip")]
    if pkg:
        url = sorted(pkg)[-1]["url"]
        return url

nltk_json    = "https://pypi.python.org/pypi/nltk/json"
data         = requests.get(nltk_json).json()
nltk_version = data["info"]["version"]
release      = data["releases"][nltk_version]

nltk_url = geturl(release)
if not nltk_url:
    error("NLTK zip package not found")

print("Downloading NLTK")
io = StringIO(requests.get(nltk_url).content)
print("Decompressing")
with zipfile.ZipFile(io) as zp:
    zp.extractall()
print("Installing")
io.close()
foldername = "nltk-{}".format(nltk_version)
shutil.move(os.path.join(foldername, "nltk"), sitepath)
shutil.rmtree(foldername)
nltk_data_path = os.path.join("~", "Documents", "nltk_data")
os.environ["NLTK_DATA"] = nltk_data_path
# And also to make sure it works
linenum = 75
data_path = os.path.join(nltkpath, "data.py")
hackline = "    path.append(os.path.expanduser(str('{}')))".format(nltk_data_path)
with open(data_path) as in_file:
    lines = in_file.read().splitlines()
lines[linenum - 1] = hackline
with open(data_path, "w") as fp:
    fp.write(os.linesep.join(lines))
full = os.path.expanduser(nltk_data_path)
if not os.path.exists(full):
    os.mkdir(full)
print("Done.")
