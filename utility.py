import pandas as pd
import sqlite3
import sqlalchemy 
import logging
import io,os
import base64
import pandas as pd
import sqlite3
import sqlalchemy 
from PIL import  Image, ImageDraw, ImageFont
import cv2
import numpy as np
import PySimpleGUI as sg


logger = logging.getLogger()

def SELECT_FILE(filename, show=False):
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    add=os.path.join(here,filename)
    if(show):print(add)
    return add
    

Clases=['post','trunk']
Side=['left','Right']
All_image=[]
Right_image=[]
Left_image=[]
Folder=None


class Analyzer(object):

    def __init__(self, **kwargs):
        self.height=0 #self.__dict__.update(kwargs)
        self.width=0
        for key, value in kwargs.items():   #for key in kwargs:
                setattr(self, key, value)     #setattr(self, key, kwargs[key])
   
    def convert_to_bytes(self,file_or_bytes, resize=None):
        if isinstance(file_or_bytes, str):
            img = Image.open(file_or_bytes)
        else:
            try:
                img = Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
            except Exception as e:
                dataBytesIO = io.BytesIO(file_or_bytes)
                img = Image.open(dataBytesIO)
        ######################
        cur_width, cur_height = img.size
        if resize:
            new_width, new_height = resize
            scale = min(new_height/cur_height, new_width/cur_width)
            img = img.resize((int(cur_width*scale), int(cur_height*scale)), Image.ANTIALIAS)
            cur_width, cur_height = img.size
        ######################
        
        with io.BytesIO() as bio:
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()   
        
    def NonBlackPer(self,img,pre):
        self.height, self.width = img.shape
        n_total = self.height * self.width
        n_black = cv2.countNonZero(img)
        st=(n_black / n_total * 100)
        #pre=round(pre/100,2)
        st=round(st,2)
        if st>pre:
            detect=1
        else:
            detect=0
        return st,detect

    def dilate(self,img,tr):
        blurred = cv2.GaussianBlur(img, (3, 3), 0)
        edged = cv2.Canny(blurred, 10, 100)

        # define a (3, 3) structuring element
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        # apply the dilation operation to the edged image
        dilate = cv2.dilate(edged, kernel, iterations=1)

        # find the contours in the dilated image
        contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        image_copy = img.copy()
        # draw the contours on a copy of the original image
        cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 2)
        return img

    def contour_aprx_non(self,img,tr):  #int(values['-THRESH SLIDER-'] )
        ret ,         thrash = cv2.threshold(img, tr , 255, cv2.CHAIN_APPROX_NONE)
        contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
            cv2.drawContours(img, [approx], 0, (0, 255, 0), 5)

        return img  

    def contour_multi_shape(self,img,tr):
        ret,thresh = cv2.threshold(img,tr,255,1)  
        contours,h = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
         
        for cnt in contours: 
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True) 
            #print len(approx) 
            if len(approx)==5: 
                #print "pentagon" 
                cv2.drawContours(img,[cnt],0,255,-1) 
            elif len(approx)==3: 
                #print "triangle" 
                cv2.drawContours(img,[cnt],0,(0,255,0),-1) 
            elif len(approx)==4: 
                #print "square" 
                cv2.drawContours(img,[cnt],0,(0,0,255),-1) 
            elif len(approx) == 9: 
                #print "half-circle" 
                cv2.drawContours(img,[cnt],0,(255,255,0),-1) 
            elif len(approx) > 15: 
                #print "circle" 
                cv2.drawContours(img,[cnt],0,(0,255,255),-1) 
        return img

    def contour(self,img,tr):
        threshold = 90
        canny_output = cv2.Canny(img, threshold, threshold * 2)

        contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find the rotated rectangles and ellipses for each contour
        minRect     = [None]*len(contours)
        minEllipse  = [None]*len(contours)
        for i, c in    enumerate(contours):
            minRect[i] = cv2.minAreaRect(c)
            if c.shape[0] > 5:
                minEllipse[i] = cv2.fitEllipse(c)
        # Draw contours + rotated rects + ellipses
        
        drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
        
        for i, c in enumerate(contours):
            color = (0, 255, 0)#rng.randint(0,256)
            # contour
            cv2.drawContours(drawing, contours, i, color)
            # ellipse
            if c.shape[0] > 10:
                cv2.ellipse(drawing, minEllipse[i], color, 2)
            # rotated rectangle
            box = cv2.boxPoints(minRect[i])
            box = np.intp(box) #np.intp: Integer used for indexing (same as C ssize_t; normally either int32 or int64)
            cv2.drawContours(drawing, [box], 0, color)
        
        return drawing

    def analyze(self,Folder,w,h,ca,cb,prec):
        # layout the form
        if w and h:
                new_size = w,h
        else:
                new_size = None

        layoutr = [[sg.Text('Analysing.....')],
                  [sg.ProgressBar(1, orientation='h', size=(40, 20), key='progress')],
                  [sg.Cancel()]]
        window = sg.Window('Analysing Right images', layoutr)
        progress_bar = window['progress']

        p,v,i=0,0,0
        s_r=[]
        for img in Right_image:            
            event, values = window.read(timeout=0)
            if event == 'Cancel' or event == None:
                break            
            filename    = os.path.join(Folder,img)
            frame = cv2.imread(filename)
            frame = cv2.resize(frame,new_size) 
            frame = cv2.imread(filename,0)
            frame = cv2.resize(frame,new_size) 
            img   = cv2.Canny(frame,ca,cb)    #,apertureSize = 3
            pre,det   =self.NonBlackPer(img,prec)
            
            if det:
                s_r.append(f'Vine{v}')
                v=v+1
            else:
                s_r.append(f'Post{p}')
                p=p+1
            print('Right',pre,det)#1662251276864
            i+=1
            progress_bar.update_bar(i, len(Right_image))
        window.close()  
        
        layoutl = [[sg.Text('Analysing.....')],
                  [sg.ProgressBar(1, orientation='h', size=(40, 20), key='progress')],
                  [sg.Cancel()]]
        window = sg.Window('Analysing Left images', layoutl)
        progress_bar = window['progress']
        p,v,i=0,0,0
        s_l=[]
        for img in Left_image:            
            event, values = window.read(timeout=0)
            if event == 'Cancel' or event == None:
                break            
            filename    = os.path.join(Folder,img)
            frame = cv2.imread(filename)
            frame = cv2.resize(frame,new_size) 
            frame = cv2.imread(filename,0)
            frame = cv2.resize(frame,new_size) 
            img   = cv2.Canny(frame,ca,cb)    #,apertureSize = 3
            pre,det   =self.NonBlackPer(img,prec)
            
            if det:
                s_l.append(f'Vine{v}')
                v=v+1
            else:
                s_l.append(f'Post{p}')
                p=p+1
            print('Left',pre,det)#1662251276864
            i+=1
            progress_bar.update_bar(i, len(Right_image))
        window.close() 
        return  s_l,s_r      

class DB_Data(object):
    
    def __init__(self,db_file):
        self.clas=None
        self.lef=None
        self.top=None
        self.w=None
        self.h=None
        self.Lat=None
        self.Lon=None
        self.Hei=None
        self.conn=None
        self.detect=False
        self.db_file=db_file
        self.isConnected=False
        self.d_detec=None
        self.d_img=None
        self.ini_conection()

    def ini_conection(self):
        logger.info('ini_conection')
        try:
            self.conn = sqlite3.connect(SELECT_FILE(self.db_file))    #"RAW1648120355.db"
            self.isConnected=True
            self.d_detec=pd.read_sql_query('SELECT * FROM Detections', self.conn) #ImageId  ClassId  Left   Top  Width  Height
            self.d_img  =pd.read_sql_query('SELECT * FROM Images'    , self.conn) # CameraId  ImageId       Lat       Lon         Hei
            print(self.d_detec)
            print(self.d_img)
            self.conn.close()
        except Exception as e:
            self.isConnected=False
            logger.info(e)

    def is_image_side(self,fileName):
        j=0
        for row in self.d_img["ImageId"]:
            if row==fileName:
               if(self.d_img['CameraId'][j]==0):
                  return 'R'
               else:
                  return 'L'
            j+=1
        return 'N' 

    def find_image_info(self,id):
        
        j=0
        det,image=0,0
        for row in self.d_detec["ImageId"]:
            if row==id:
               det=1;
               #print('got n')
               self.clas,self.lef,self.top,self.wi,self.hi=self.d_detec['ClassId'][j],self.d_detec['Left'][j],self.d_detec['Top'][j],self.d_detec['Width'][j],self.d_detec['Height'][j]
               break
            j+=1
        
        j=0
        for row in self.d_img["ImageId"]:
            if row==id:
               image=1
               #print('got nnn')
               self.cam,self.lat,self.lon,self.hei=self.d_img['CameraId'][j],self.d_img['Lat'][j],self.d_img['Lon'][j],self.d_img['Hei'][j]
               break
            j+=1
        if (image+det)>1:
            self.detect=True
        else: 
            self.detect=False
        #print('info ',id,' =',clas,lef,top,w,h,cam,lat,lon,hei)
        
        #s= f'{id}=[img{image}detect{det}?{detect}]{Clases[self.clas]},{self.lef},{self.top},{self.wi},{self.hi},{Side[self.cam]},{self.lat},{self.lon},{self.hei}'
        #print(s)
        return 's'
        
   
    def sort_images(self,fol):
        global Folder
        Folder=fol
        logger.info("sort_images",fol )
       
        try:
            file_list = os.listdir(fol)         # get list of files in folder  
            #print('all files\n',file_list)
        except:
            file_list = []
        #print('file_list',file_list)   
        for f in file_list:
            if os.path.isfile(os.path.join(fol, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp")):
                try:
                    f=int(f[:-5] )
                    #print(f,type(f))
                    if   self.is_image_side(f)=='R':
                                            Right_image.append(str(f)+'.jpeg')
                    elif self.is_image_side(f)=='L':
                                            Left_image.append(str(f)+'.jpeg')   
                except:
                    pass
            All_image.append(str(f)+'.jpeg')   
      
        print(len(All_image),len(Right_image),len(Left_image))    














