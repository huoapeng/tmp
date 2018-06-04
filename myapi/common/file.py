''' tk_image_view_url_io_resize.py
display an image from a URL using Tkinter, PIL and data_stream
also resize the web image to fit a certain size display widget
retaining its aspect ratio
Pil facilitates resizing and allows file formats other then gif
tested with Python27 and Python33 by vegaseat 18mar2013
'''
# import io
from PIL import Image#, ImageTk
from myapi.model.enum import file_type
from myapi import app
import os, random
from werkzeug.utils import secure_filename

# try:
#   # Python2
#   import Tkinter as tk
#   from urllib2 import urlopen
# except ImportError:
#   # Python3
#   import tkinter as tk
#   from urllib.request import urlopen
def resize(pil_image, w_box, h_box):
    '''
    resize a pil_image object so it will fit into
    a box of size w_box times h_box, but retain aspect ratio
    '''
    pil_image = Image.open(pil_image)
    w, h = pil_image.size
    f1 = 1.0 * w_box / w # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    #print(f1, f2, factor) # test
    # use best down-sizing filter
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

def getUploadFileUrl(fileType, folderName, fileName):
    if fileName:
        return 'http://{}/{}{}{}'.format(\
            app.config['IP_ADDRESS'], \
            app.config['UPLOAD_FOLDER'], \
            filePath[fileType](folderName), \
            fileName)
    else:
        return ''

def getDefaultImageUrl(fileName):
    return 'http://{}/{}{}'.format(\
        app.config['IP_ADDRESS'], \
        app.config['DEFAULT_IMAGE_FOLDER'], \
        fileName)

filePath = {
    file_type.profileLarge : lambda folderName: 'user/{}/profileLarge/'.format(folderName),
    file_type.profileMedium : lambda folderName: 'user/{}/profileMedium/'.format(folderName),
    file_type.profileSmall : lambda folderName: 'user/{}/profileSmall/'.format(folderName),
    file_type.version : lambda folderName: 'user/{}/version/'.format(folderName),
    file_type.privateFront : lambda folderName: 'user/{}/privateFront/'.format(folderName),
    file_type.privateBack : lambda folderName: 'user/{}/privateBack/'.format(folderName),
    file_type.companyLience : lambda folderName: 'user/{}/companyLience/'.format(folderName),
    file_type.companyContactCard : lambda folderName: 'user/{}/companyContactCard/'.format(folderName),
    file_type.work : lambda folderName: 'user/{}/work/'.format(folderName),
    file_type.workThumbnail : lambda folderName: 'user/{}/workThumbnail/'.format(folderName),
    file_type.recommend : lambda folderName: 'recommend/{}/'.format(folderName),
    file_type.workFile : lambda folderName: 'user/{}/workfile/'.format(folderName),
    file_type.bidFile : lambda folderName: 'user/{}/bidfile/'.format(folderName),
    file_type.workPic : lambda folderName: 'user/{}/workPic/'.format(folderName)
}

def isAllowedFile(fileType, fileName):
    ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
    ALLOWED_FILE_EXTENSIONS = set(['zip', 'rar'])

    flag = False
    for key in file_type.__dict__:
        if fileType == file_type.__dict__[key]:
            flag = True
            break

    if flag:
        if fileType > 50:
            return '.' in fileName and fileName.rsplit('.', 1)[1] in ALLOWED_FILE_EXTENSIONS
        else:
            return '.' in fileName and fileName.rsplit('.', 1)[1] in ALLOWED_IMAGE_EXTENSIONS
    else:
        return False

def getServerFilePath(fileType, folderName, filename):
    serverPath = os.path.join(app.config['ROOT_PATH'], \
        app.config['UPLOAD_FOLDER'], filePath[fileType](folderName))
    if not os.path.exists(serverPath):
        os.makedirs(serverPath)

    fname = secure_filename(filename)
    sf = os.path.join(serverPath, fname)
    
    while os.path.exists(sf):
        randomString = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ',10))
        sf = sf.replace(fname, randomString + fname)
    return sf

# root = tk.Tk()
# # size of image display box you want
# w_box = 400
# h_box = 350
# # find yourself a picture on an internet web page you like
# # (right click on the picture, under properties copy the address)
# # a larger (1600 x 1200) picture from the internet
# # url name is long, so split it
# url1 = "http://freeflowerpictures.net/image/flowers/petunia/"
# url2 = "petunia-flower.jpg"
# url = url1 + url2
# image_bytes = urlopen(url).read()
# # internal data file
# data_stream = io.BytesIO(image_bytes)
# # open as a PIL image object
# pil_image = Image.open(data_stream)
# # get the size of the image
# w, h = pil_image.size
# # resize the image so it retains its aspect ration
# # but fits into the specified display box
# pil_image_resized = resize(pil_image, w_box, h_box)
# # optionally show resized image info ...
# # get the size of the resized image
# wr, hr = pil_image_resized.size
# # split off image file name
# fname = url.split('/')[-1]
# sf = "resized {} ({}x{})".format(fname, wr, hr)
# root.title(sf)
# # convert PIL image object to Tkinter PhotoImage object
# tk_image = ImageTk.PhotoImage(pil_image_resized)
# # put the image on a widget the size of the specified display box
# label = tk.Label(root, image=tk_image, width=w_box, height=h_box)
# label.pack(padx=5, pady=5)
# root.mainloop()