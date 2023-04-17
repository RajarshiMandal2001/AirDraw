from tkinter import *
from PIL import ImageTk, Image
import cv2
import imutils
import numpy as np
#..............................All variables here........................
points_queue = []   #coordinates are stored in it
figNo = 1           #assigns figure number to distinct figures drawn
justStarted = 0
shift_queue = []    #overrider line points stored in it
permission=0        #permission to start drawing
newFig=0
activate_white_background = 0
R,G,B = 0,0,255     #default blue pen
colorDic = dict()   #colour mapper according to figNo
# ........................All function definations here................... 
def callStart():  
    global permission
    global newFig
    print("start pressed")
    permission=1
    newFig=0
def callStop():  
    global permission
    global newFig
    global figNo
    print("stop pressed")
    permission=0
    newFig=1
    figNo += 1
    print("figno incremented,new val=",figNo)
def callClear():
    global points_queue
    global shift_queue
    global figNo
    global colorDic
    print("clear pressed")
    points_queue.clear()
    shift_queue.clear()
    colorDic.clear()
    figNo=1
def callWhiteBackground():
    global activate_white_background
    activate_white_background = 1
def callClearFig():
    global shift_queue
    global points_queue
    print("clear fig pressed")
    f=None
    if shift_queue:
        minco,maxco = min(shift_queue[0:-1]),max(shift_queue[0:-1])  #last coordinates should not be counted since it is the point to where the fig is to be shifted
        for co in points_queue:
            if maxco[0]>=co[0] and minco[0]<=co[0] and minco[1]<=co[1] and maxco[1]>=co[1]:
                f=points_queue.index(co)
                print(co,"found at index:",points_queue.index(co))
                break

    try:
        temp_points_queue = []
        for i in range(len(points_queue)):  
            if points_queue[i][2] != points_queue[f][2]:
                    temp_points_queue.append(points_queue[i])
        points_queue = temp_points_queue
        shift_queue.clear()
    except TypeError:
        print("overlapping not found")

def callShift():
    global points_queue
    global shift_queue
    global colorDic
    print("shift pressed")
    try:
        f=None
        for i in range(len(points_queue)):    #convert tuple to list else it cant be modified
            points_queue[i] = list(points_queue[i])
        print("queue= ",points_queue)
        print("\nshift_queue= ",shift_queue)

        f999 = shift_queue.index((-999,-999))

        minco,maxco = min(shift_queue[0:f999]),max(shift_queue[0:f999])  #last coordinates should not be counted since it is the point to where the fig is to be shifted
        print(min(shift_queue[0:f999]),max(shift_queue[0:f999]))
        for co in points_queue:
            if maxco[0]>=co[0] and minco[0]<=co[0] and minco[1]<=co[1] and maxco[1]>=co[1]:
                f=points_queue.index(co)
                print(co,"found at index:",points_queue.index(co))
                break
        try:
            print("last shift queue value= ",shift_queue[-2],",at f queue value = ",points_queue[f])
            temp = points_queue[f]
            shift_x = shift_queue[-2][0]-temp[0] #  -2 because in -1 -999 is present
            shift_y = shift_queue[-2][1]-temp[1]
            print("temp[0]=",temp[0],"temp[1]=",temp[1])
            print("shift_x=",shift_x,"shift_y=",shift_y)
            for i in range(len(points_queue)):   
                if (points_queue[i][2] == temp[2]):
                    print(points_queue[i],points_queue[i][0])
                    points_queue[i][0] += shift_x   
                    points_queue[i][1] +=  shift_y 
            shift_queue.clear()
        except TypeError:
            print("overlapping not found")
    except ValueError:
        pass
def callPinkColor():
    global R,B
    global G
    R,G,B = 255,102,255
def callYellowColor():
    global R,B,G
    R,G,B = 255,255,0
def callBlackColor():
    global R,B,G
    R,G,B = 0,0,0
def callWhiteColor():
    global R,B,G
    R,G,B = 255,255,255
def callBlueColor():
    global R,B,G
    R,G,B = 0,0,255
def callGreenColor():
    global R,B,G
    R,G,B = 0,255,0
# ........ ...............................................................
#............................Window configurations........................
root = Tk()
root.geometry("1400x700")
root.title("Air Drawing")

videoFrame = Frame(root)
videoFrame.place(x=50,y=5)
lmain = Label(videoFrame)
lmain.pack()

secondaryFrame = Frame(root)
secondaryFrame.place(x=980,y=5)
secondarylmain = Label(secondaryFrame)
secondarylmain.pack()

#.............................All Buttons here............................
startBtn = Button(root,text="Start",command=callStart).place(x=10,y=650)
cleartBtn = Button(root,text="Clear Screen",command=callClear).place(x=60,y=650)
stopBtn = Button(root,text="Stop",command=callStop).place(x=150,y=650)
shiftBtn = Button(root,text="Shift Figure",command=callShift).place(x=220,y=650)
clearFigBtn = Button(root,text="Remove selected figure",command=callClearFig).place(x=300,y=650)
whiteBackgroundBtn = Button(root,text="White BackGround",command=callWhiteBackground).place(x=420,y=650)
changeColorLabel = Label(root,text="Change Pen Colour").place(x=900,y=300)
yellowImg = ImageTk.PhotoImage(Image.open("yellow.png"))
yellowColorBtn = Button(root,image=yellowImg,command=callYellowColor).place(x=900,y=340) 
pinkImg = ImageTk.PhotoImage(Image.open("pink.png"))
pinkColorBtn = Button(root,image=pinkImg,command=callPinkColor).place(x=950,y=340) 
whiteImg = ImageTk.PhotoImage(Image.open("white.png"))
whiteColorBtn = Button(root,image=whiteImg,command=callWhiteColor).place(x=1000,y=340) 
blackImg = ImageTk.PhotoImage(Image.open("black.png"))
blackColorBtn = Button(root,image=blackImg,command=callBlackColor).place(x=1050,y=340) 
greenImg = ImageTk.PhotoImage(Image.open("green.png"))
greenColorBtn = Button(root,image=greenImg,command=callGreenColor).place(x=1100,y=340) 
blueImg = ImageTk.PhotoImage(Image.open("blue.png"))
blueColorBtn = Button(root,image=blueImg,command=callBlueColor).place(x=1150,y=340) 
#.........................................................................

#.............................Capture from webcam.........................
# URL = "http://10.237.101.66:8080/video"
# cap = cv2.VideoCapture(URL)
cap = cv2.VideoCapture(0)

#........................Image/Video processing Function..................
def video_stream():
    global justStarted
    global newFig
    _, frame = cap.read()
    sframe = imutils.resize(frame,width=300,height=200)
    sframe = cv2.flip(sframe,1)
    sframe = cv2.cvtColor(sframe, cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=800,height=600)
    frame = cv2.flip(frame,1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    if permission:
        # finding green object...............................................
        lower_green = np.array([36, 25, 25])
        upper_green = np.array([70, 255,255])
        green_mask = cv2.inRange(hsv,lower_green,upper_green)
        contours,_ = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        x,y=0,0
        for c in contours:
            area = cv2.contourArea(c)
            if area>100:
                x,y,_,_ = cv2.boundingRect(c)
        if not(x==0 and y==0):
            points_queue.append((x,y,figNo))
            colorDic[figNo] = (R,G,B)
        # finding redish object...............................................
        sx,sy=0,0
        lower_red = np.array([136, 87, 111])  #pink colour
        upper_red = np.array([179, 255,255])
        red_mask = cv2.inRange(hsv,lower_red,upper_red)
        contours,_ = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area = cv2.contourArea(c)
            if area>100:
                sx,sy,_,_ = cv2.boundingRect(c)
        if not(sx==0 and sy==0):
            shift_queue.append((sx,sy))
    if activate_white_background:
        cv2.rectangle(cv2image,(0,0),(800,600),(255,0,0),800)

    for co in points_queue:
        cv2.circle(cv2image,tuple(co[0:-1]),1,colorDic[co[2]],2)

    if justStarted:
        for co in range(len(points_queue)-2):
            if (points_queue[co][2] != points_queue[co+1][2]): 
                continue
            cv2.line(cv2image,tuple(points_queue[co][0:-1]),tuple(points_queue[co+1][0:-1]),colorDic[points_queue[co][2]],2)
    justStarted=1
    
    
    if newFig:
        if shift_queue:   #if shidt queue is empty then we will not insert -999 into it
            print("-999 inserted in shift_queue")
            shift_queue.append((-999,-999))  
        else:
            print("-999 cant be inserted since shift queue is empty")
        newFig = 0
    for co in shift_queue:
        cv2.circle(cv2image,co,1,(255,0,0),2)
    
    
    # dont touch the below codes ,they are constant
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)

    simg = Image.fromarray(sframe)
    simgtk = ImageTk.PhotoImage(image=simg)
    secondarylmain.simgtk = simgtk
    secondarylmain.configure(image=simgtk)

    lmain.after(1, video_stream) 
    
#.............................Welcome Frame........................................
welcomeFrame = Frame()
welcomeFrame.place(x=0,y=0,width=1400,height=700)
welcomeImg = ImageTk.PhotoImage(Image.open("AirPic1.png"))
welcomeLabel = Label(welcomeFrame, image = welcomeImg)
welcomeLabel.pack(side = "bottom", fill = "both", expand = "yes")
# welcomeLabel = Label(welcomeFrame,text="welcome")
# welcomeLabel.place(x=0,y=9)
welcomeFrame.after(5000,welcomeFrame.destroy)

video_stream()
root.mainloop()
print(colorDic)


# # ................................................................................
# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.uix.button import Button
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.image import Image
# from kivy.clock import Clock
# from kivy.graphics.texture import Texture
# from kivy.uix.camera import Camera

# # from kivy.config import Config
# # Config.set("AirDraw","width","500")
# # Config.set("AirDraw","height","500")

# # from android.permissions import request_permissions, Permission

# import cv2
# import numpy as np

# class CamApp(App):
#     queue=[]
#     justStarted=0
#     permission=0
#     newFig=0

#     def build(self):

#         # request_permissions([
#         # Permission.CAMERA,
#         # Permission.WRITE_EXTERNAL_STORAGE,
#         # Permission.READ_EXTERNAL_STORAGE
#         # ])

#         layout = BoxLayout(orientation="vertical")
#         self.img1=Image(size_hint=(1.0,1.0),pos_hint={"center_x":0.5,"center_y":0.5})  #pos_hint={"center_x":0.5,"center_y":0.5}

#         # layout.add_widget(self.img1)
#         innerLayout = BoxLayout()
#         startBtn = Button(text="Start",on_press=self.callStart,font_size="20sp",background_color=(1,1,1,1),color=(1,1,1,1),size_hint=(.2,.2))
#         stopBtn = Button(text="Stop",on_press=self.callStop,font_size="20sp",background_color=(1,1,1,1),color=(1,1,1,1),size_hint=(.2,.2))
#         clearBtn = Button(text="Clear",on_press=self.callClear,font_size="20sp",background_color=(1,1,1,1),color=(1,1,1,1),size_hint=(.2,.2))
        
#         innerLayout.add_widget(startBtn)
#         innerLayout.add_widget(stopBtn)
#         innerLayout.add_widget(clearBtn)
#         layout.add_widget(self.img1)
#         layout.add_widget(innerLayout)

#         # URL = "http://10.23.174.5:8080/video"
#         # self.capture = cv2.VideoCapture(URL)

#         # self.cam = Camera()
#         # self.cam.resolution = (640,480)

#         self.capture = cv2.VideoCapture(0)
#         Clock.schedule_interval(self.update, 1.0/33.0)
#         return layout

#     def callStart(self,obj):  #why obj we dont know,if not given it will give error
#         print("start pressed")
#         CamApp.permission=1
#         CamApp.newFig=0
#     def callStop(self,obj):  #why obj we dont know,if not given it will give error
#         print("stop pressed")
#         CamApp.permission=0
#         CamApp.newFig=1
#     def callClear(self,obj):
#         print("clear pressed")
#         CamApp.queue.clear()

#     def update(self, dt):
#         # display image from cam in opencv window
#         ret, frame = self.capture.read()
#         frame = cv2.flip(frame,0)
#         frame = cv2.flip(frame,1)
#         cv2.circle(frame,(10,10),5,(255,0,0),2)
#         # cv2.imshow("CV2 Image", frame)
#         #....................from here opencv code...........................
#         if CamApp.permission:
#             hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#             lower_green = np.array([36, 25, 25])
#             upper_green = np.array([70, 255,255])
#             mask = cv2.inRange(hsv,lower_green,upper_green)

#             contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#             x,y=0,0
#             for c in contours:
#                 area = cv2.contourArea(c)
#                 if area>100:
#                     x,y,w,hi = cv2.boundingRect(c)

#             if not(x==0 and y==0):
#                 CamApp.queue.append((x,y))
#                 print(CamApp.queue)
#         if CamApp.newFig:
#             CamApp.queue.append((-999,-999))  #break point for new figure
#             CamApp.newFig = 0

#         for co in CamApp.queue:
#             cv2.circle(frame,co,1,(255,0,0),2)

#         if CamApp.justStarted:
#             for co in range(len(CamApp.queue)-2):
#                 if CamApp.queue[co] == (-999,-999) or CamApp.queue[co+1] == (-999,-999):
#                     continue
#                 cv2.line(frame,CamApp.queue[co],CamApp.queue[co+1],(255,0,0),2)

#         CamApp.justStarted=1
#         #....................................................................

#         # convert it to texture
#         buf1 = frame
#         buf = buf1.tostring()
#         texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
#         texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
#         # display image from the texture
#         self.img1.texture = texture1
# if __name__ == '__main__':
#     CamApp().run()
#     cv2.destroyAllWindows()




