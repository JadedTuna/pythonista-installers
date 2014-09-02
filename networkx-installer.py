import requests
import zipfile
import tarfile

try:
    from cStringIO import StringIO
except:
    from StringIO  import StringIO
import os

jsonurl = "https://pypi.python.org/pypi/{}/json"
path    = os.path.join(os.path.expanduser("~"),
                       "Documents",
                       "site-packages")
inxpath = os.path.join(path,
                       "networkx")
idcpath = os.path.join(path,
                       "decorator.py")

def getpkg(pkgname):
    """ Retrieve package
    """
    req = requests.get(jsonurl.format(pkgname))
    data = req.json()
    req.close()
    
    version = data["info"]["version"]
    verinfo = data["releases"][version]
    urls    = [i for i in verinfo]
    url     = None
    for _url in urls:
        if _url["filename"].endswith(".zip"):
            url = _url["url"]
            break
    
    if not url:
        for _url in urls:
            if _url["filename"].endswith(".tar.gz"):
                url = _url["url"]
                break
    #print url
    pkgdata = requests.get(url).content
    return pkgdata

if os.path.exists(inxpath):
    print "networkx already installed, skipping."
else:
    print "Downloading networkx."
    networkx = StringIO(getpkg("networkx"))
    print "Extracting networkx."
    nxzfp    = zipfile.ZipFile(networkx)
    folderpath = nxzfp.namelist()[0].split("/")[0]
    nxpath = os.path.join(folderpath, "networkx") + "/"
    for name in nxzfp.namelist():
        if not name.startswith(nxpath): continue
        data = nxzfp.read(name)
        name = os.path.join(*name.split("/")[1:])
        savepath = os.path.join(path, name)
        dirpath  = "/" + os.path.join(*savepath.split("/")[:-1])
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        with open(savepath, "wb") as fp:
            fp.write(data)

if os.path.exists(idcpath):
    print "decorator already installed, skipping."
else:
    print "Downloading decorator."
    decorator = StringIO(getpkg("decorator"))
    print "Extracting decorator."
    deczfp = tarfile.open(fileobj=decorator, mode="r:gz")
    folderpath = deczfp.getnames()[0].split("/")[0]
    decpath = os.path.join(folderpath, "src", "decorator.py")
    with open(os.path.join(path, "decorator.py"), "w") as fp:
        data = deczfp.extractfile(decpath).read()
        fp.write(data)
print "Done."
