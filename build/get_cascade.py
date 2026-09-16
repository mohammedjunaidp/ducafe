import urllib.request, os

URL = ("https://raw.githubusercontent.com/opencv/opencv/4.x/data/"
       "haarcascades/haarcascade_frontalface_default.xml")
dst = os.path.join(os.path.dirname(__file__), "haarcascade_frontalface_default.xml")
try:
    urllib.request.urlretrieve(URL, dst)
    print("OK", os.path.getsize(dst), "bytes ->", dst)
except Exception as e:
    print("FAILED:", type(e).__name__, e)
