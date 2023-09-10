from ultralytics import YOLO
import os
import cv2
import gdown
import cvzone
import supervision as sv
import numpy as np
from itertools import combinations 
# from fire_detect import PARAMS_FILE_PATH
CONFIG_FILE_PATH = "config/config.yaml"
PARAMS_FILE_PATH = "config/params.yaml"
import utils
" =  +"

class FireDetector:

    def __init__(self)->None:
        
        self.config_content = utils.read_yaml(CONFIG_FILE_PATH).get("fire_detect")
        self.params_content = utils.read_yaml(PARAMS_FILE_PATH).get("text_params")

    def load_model(self,model_path:str)->YOLO:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"{model_path} not found")
        
        self.model = YOLO(model_path)

    @staticmethod
    def download_model(model_drive_id:str,yolo_model_path:str)->None:
        if os.path.exists(yolo_model_path):
            gdown.download(id = model_drive_id,output=yolo_model_path)
            return
        else:
            print("Model Already Exist")


    def combine_all(self):
        FIRE_DETECT_DIR_NAME = "fire_detect"
        input_video_path = os.path.join(FIRE_DETECT_DIR_NAME,self.config_content.get("input_video_path"))
        output_video_path =  os.path.join(FIRE_DETECT_DIR_NAME,self.config_content.get("output_video_path"))
        model_drive_id =  self.config_content.get("model_drive_id")
        yolo_model_path =  os.path.join(FIRE_DETECT_DIR_NAME,self.config_content.get("yolo_model_path"))
        self.download_model(model_drive_id,yolo_model_path)
        self.load_model(yolo_model_path)
        sv.process_video(input_video_path,output_video_path,self.process)
        print(f"PROCESS VIDEO DONE OUT VIDEO PATH {output_video_path} ")

    def process(self,im:np.ndarray,_)->np.ndarray:

        font = self.params_content.get("font")
        danger_txt= self.params_content.get("danger_txt")
        fine_txt= self.params_content.get("fine_txt")
        danger_thick= self.params_content.get("danger_thick")
        danger_fontface= self.params_content.get("danger_fontface")
        normal_thick= self.params_content.get("normal_thick")
        normal_fontface= self.params_content.get("normal_fontface")

        result = self.model.predict(im,verbose  = False )
        combi=list(combinations([i for i in result[0].boxes.data],2))
        temp = False
        for p1,p2 in combi:
            p1=np.array(p1,dtype=int)

            p2=np.array(p2,dtype=int)
            lab = [p1[-1] , p2[-1]]
            if p1[-1] != p2[-1] and abs(p2[0]-p1[0])<300 and (0 in lab) and (1 in lab):
                for p in [p1,p2]:
                    temp=True
                    x,y = (p[0],p[1])
                    x2,y2 = (p[2],p[3])
                    w,h = x2-x,y2-y
                    cvzone.cornerRect(im,(x,y,w,h),colorR=[50,59,237],colorC=[0,0,255])
                p1,p2 = (p2,p1) if p1[1]>p2[1] else (p1,p2)
            

            # cv2.rectangle(im,(p1[0]-10,p1[1]-10),(max(p1[2:4],p2[2:4],key=lambda a:a[0])[0]+10,p2[3]+10),(0,0,255),thickness=4)
            # cv2.putText(im,"Danger Zone",(p1[0]-10,p1[1]-15),cv2.FONT_HERSHEY_COMPLEX,1.5,(0,0,255),3)
            
                x,y = (p1[0]-10,p1[1]-10)
                x2,y2 = (max(p1[2:4],p2[2:4],key=lambda a:a[0])[0]+10,p2[3]+10)
                w,h = x2-x,y2-y
                cvzone.cornerRect(im,(x,y,w,h),colorR=[50,59,237],colorC=[0,0,255])
                cvzone.putTextRect(im,"Stove on and no fire detected",( p1[0],p1[1]-45 ),colorT=(0,0,255),scale=2,thickness=2,offset=5)
                cvzone.putTextRect(im,"Danger Zone",(p1[0],p1[1]-20),colorT=(0,0,255),scale=2,thickness=2,offset=5)

            if not temp and len(set(lab))>1 and abs(p2[0]-p1[0])<300:
                for p in [p1,p2]:
                    # cv2.rectangle(im,(p[0],p[1]),(p[2],p[3]),[106, 237, 40][::-1],thickness=4)
                    cvzone.cornerRect(im,(p[0],p[1],p[2] - p[0],p[3] - p[1]),colorR=[40,237,106],colorC=[0,255,0])
                p1,p2 = (p2,p1) if p1[1]>p2[1] else (p1,p2)

                x,y = (p1[0]-10,p1[1]-10)
                x2,y2 = (max(p1[2:4],p2[2:4],key=lambda a:a[0])[0]+10,p2[3]+10)
                w,h = x2-x,y2-y
                cvzone.cornerRect(im,(x,y,w,h),colorR=[40,237,106],colorC=[0,255,0])
                on_off = "on" if 3 in lab else "off"
                fire_or_not = "fire detected" if on_off=="on" else "no fire detected"
                cvzone.putTextRect(im,f"Stove {on_off} and {fire_or_not}",( p1[0],p1[1]-45 ),colorT=(0,255,0),scale=2,thickness=2,offset=5)
                cvzone.putTextRect(im,"Every Thing Fine",(p1[0],p1[1]-20),colorT=(0,255,0),scale=2,thickness=2,offset=5)
        return im