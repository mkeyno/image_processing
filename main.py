

from PIL import  Image, ImageDraw, ImageFont
 
from utility import *
from layout import *
 
import numpy as np
 


ImageId=None

db  =DB_Data("RAW1648120355.db")
ana =Analyzer()
  
def show_original(file_or_bytes, resize=None):
    
    if isinstance(file_or_bytes, str):
        img = Image.open(file_or_bytes)
    else:
        try:
            img = Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = Image.open(dataBytesIO)

    cur_width, cur_height = img.size

    if db.detect:
        draw = ImageDraw.Draw(img, "RGBA")
        #draw.rectangle(((lef,top), (lef-wi,top-hi)), outline="white", width=3)
        draw.rectangle(((db.lef,db.top), (db.lef+db.wi,db.top+db.hi)), outline="red", width=7)
        #draw.rectangle(((lef,top), ( wi, hi)), outline="blue", width=3)
    
    #draw.text((0, 0),ImageId,(255,255,255))
    font = ImageFont.truetype("arial", 35)
    ImageDraw.Draw( img).text( (5, 5),  f' Image: {ImageId}.jpeg \n latitiude:  {db.lat} \n longitiude:  {db.lon}\n height:  {db.hei}',  (0, 255, 0) ,font=font)
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), Image.ANTIALIAS)
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()


window=GUI()
frame=None

i=0
try:
    while True:
        event, values = window.read(timeout=20)
        if   event in (sg.WIN_CLOSED, 'Exit'):
            break
        if   event == sg.WIN_CLOSED or event == 'Exit':
            break
        if   event != sg.TIMEOUT_KEY:
            print( event)    

        if event == 'bside': 
            window['num_of_image'].update(len(All_image))
            window['-FILE LIST-'].update(All_image)
        elif event == 'Analyse':
            s_l,s_r=ana.analyze(values['-FOLDER-'],int(values['-W-']), int(values['-H-']),values['canny_slider_a'], values['canny_slider_b'],values['thresh_percent'])
            window['-MLINEL-'].update(s_l)
            window['-MLINER-'].update(s_r)
        elif event == 'lside': 
            window['num_of_image'].update(len(Left_image))
            window['-FILE LIST-'].update(Left_image)
        elif event == 'rside': 
            window['num_of_image'].update(len(Right_image))
            window['-FILE LIST-'].update(Right_image)
        elif event == '-FOLDER-':                        
 
            db.sort_images(values['-FOLDER-'])
            window['num_of_image'].update(len(All_image))
            window['-FILE LIST-'].update(All_image)
            window['bside'].update(True)
        elif event == '-FILE LIST-':   
            
            filename    = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            ImageId     =values['-FILE LIST-'][0]; ImageId=int(ImageId[:-5] )
            #print('new imge select',ImageId)
            #window['-MLINE-'].update(
            info=db.find_image_info(ImageId)
            #)          
            
            
            if values['-W-'] and values['-H-']:
                new_size = int(values['-W-']), int(values['-H-'])
            else:
                new_size = None
                
            window['-IMAGE-'].update(data=show_original(filename, resize=new_size)) 
            frame = cv2.imread(filename)
            frame = cv2.resize(frame,new_size) 

        elif values['canny'] :  #event.startswith
            img      = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            img      = cv2.Canny(frame, values['canny_slider_a'], values['canny_slider_b'])    #,apertureSize = 3
            per,det=ana.NonBlackPer(img,values['thresh_percent'])
            window['-MLINE-'].update(f'Percentage of white pixels:{per:.2f}% {det}'  )   
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['IMAGE_p'].update(data=imgbytes)          
            
        elif values['-BLUR-']:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.GaussianBlur(frame, (21, 21), values['-BLUR SLIDER-'])
            
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['IMAGE_p'].update(data=imgbytes)  
            
        elif values['-ENHANCE-']    :
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            kernel_size=int(values['-ENHANCE SLIDER-'])
            if kernel_size%2==0: kernel_size+=1
 
            blur_gray       = cv2.GaussianBlur(frame,(kernel_size, kernel_size),0)
            edges           = cv2.Canny(blur_gray,  values['canny_slider_a'], values['canny_slider_b'])
            rho             =1#int(values['-distance resolution-'])# 1  # distance resolution in pixels of the Hough grid
            theta           = np.pi /100# values['-angular resolution-']  # angular resolution in radians of the Hough grid
            threshold       = int(values['-THRESH SLIDER-'] ) # 180 minimum number of votes (intersections in Hough grid cell)
            min_line_length =int(values['-min line-'] )#50  # minimum number of pixels making up a line
            max_line_gap    = int(values['-max line-'] )#20  # maximum gap in pixels between connectable line segments
            line_image      = np.copy(frame) * 0  # creating a blank to draw lines on
            lines           = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
 
            try:
                for line in lines:
                    for x1,y1,x2,y2 in line:
                        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
                img      = cv2.addWeighted(frame, 0.8, line_image, 1, 0)    
                per,det=ana.NonBlackPer(img,values['thresh_percent'])
                window['-MLINE-'].update(f'Percentage of white pixels:{per:.2f}% {det}'  )   
                imgbytes = cv2.imencode('.png', img)[1].tobytes()
                window['IMAGE_p'].update(data=imgbytes)  
            except Exception as E:
                pass
 
        elif values['-THRESH-']  :

            img         = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img         = cv2.threshold(img, values['-THRESH SLIDER-'], 255, cv2.THRESH_BINARY)[1] 
            per,det=ana.NonBlackPer(img,values['thresh_percent'])
            window['-MLINE-'].update(f'Percentage of white pixels:{per:.2f}% {det}'  )    
            imgbytes    = cv2.imencode('.png', img)[1].tobytes()
            window['IMAGE_p'].update(data=imgbytes)            
  
        elif values['contour']  :
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)               
            if   values['type1']: 
                img=ana.contour_multi_shape(img,int(values['-THRESH SLIDER-'] ))
                per,det=ana.NonBlackPer(img,values['thresh_percent'])
                window['-MLINE-'].update(f'Percentage of white pixels:{per:.2f}% {det}'  )            
            elif values['type2']: 
                img=ana.contour(            img,int(values['-THRESH SLIDER-'] ))
                    
            elif values['type3']: 
                img=ana.dilate(             img,int(values['-THRESH SLIDER-'] ))
                per,det=ana.NonBlackPer(img,values['thresh_percent'])
                window['-MLINE-'].update(f'Percentage of white pixels:{per:.2f}% {det}'  )    
            elif values['type4']: 
                img=ana.contour_aprx_non(   img,int(values['-THRESH SLIDER-'] ))
                per,det=ana.NonBlackPer(img,values['thresh_percent'])
                window['-MLINE-'].update(f'Percentage of white pixels:{per:.2f}% {det}'  )    
                
            
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['IMAGE_p'].update(data=imgbytes)    
            
        elif values['detec']  :       
              
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['IMAGE_p'].update(data=imgbytes)      

except Exception as E:
    sg.PopupCancel(f' Make sure first select the image\n***{E} **')
    exit(0)
    window.close()
