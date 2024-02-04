import multiprocessing as multi
import mediapipe as mp
import cv2
import numpy as np
import time
import cv2 as cv
import time
import AiPhile

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

mp_drawing1 = mp.solutions.drawing_utils
mp_drawing_styles1 = mp.solutions.drawing_styles
mp_pose1 = mp.solutions.pose

angle1 = 0.
angle2 = 0.

KNOWN_DISTANCE = 76.2  # centimeter
# width of face in the real world or Object Plane
KNOWN_WIDTH = 14.3  # centimeter
# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 200, 255)
fonts = cv.FONT_HERSHEY_COMPLEX

# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


# focal length finder function
def focal_length(measured_distance, real_width, width_in_rf_image):

    focal_length_value = (width_in_rf_image * measured_distance) / real_width
    return focal_length_value


# distance estimation function
def distance_finder(focal_length, real_face_width, face_width_in_frame):

    distance = (real_face_width * focal_length) / face_width_in_frame
    return distance


# face detector function
def face_data(image):

    face_width = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    for (x, y, h, w) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), WHITE, 1)
        face_width = w

    return face_width


def compare_angle(a1, a2):
    return abs(a1-a2) < 50

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 


def video():
    cap = cv2.VideoCapture('D:/python/9.mp4')
    cap2 = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0 
    stage = None

    # Curl counter variables
    counter2 = 0 
    stage2 = None
    # Curl counter variables
    counter3 = 0 
    stage3 = None
    stage4 = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        with mp_pose1.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose2:
            while cap.isOpened():
                ret, frame = cap.read()
                
                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
            
                # Make detection
                results = pose.process(image)
            
                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                ret, frame = cap2.read()

                # Recolor image to RGB
                image2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image2.flags.writeable = False
            
                # Make detection
                results2 = pose2.process(image2)
                
                # Recolor back to BGR
                image2.flags.writeable = True
                image2 = cv2.cvtColor(image2, cv2.COLOR_RGB2BGR)
                
                ref_image = cv2.imread("Ref_image.png")

                ref_image_face_width = face_data(ref_image)
                focal_length_found = focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, ref_image_face_width)
                # starting time here
                starting_time = time.time()
                frame_counter = 0
                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark
                    
                    # Get coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    
                    # Calculate angle
                    angle1 = calculate_angle(shoulder, elbow, wrist)
                    
                    # Visualize angle
                    cv2.putText(image, str(angle1), 
                                tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    
                    # Curl counter logic
                    if angle1 > 160:
                        stage = "down"
                    if angle1 < 30 and stage =='down':
                        stage="up"
                        counter +=1
                        print(counter)
                    if compare_angle(angle1,angle2):
                        #print(angle1)
                        #print(angle2)
                        print("Same")
                    else:
                        print("Different")
                except:
                    pass
                


                try:
                    landmarks = results2.pose_landmarks.landmark
                    
                    # Get coordinates
                    shoulder = [landmarks[mp_pose1.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose1.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose1.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose1.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose1.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose1.PoseLandmark.LEFT_WRIST.value].y]
                    
                    # Calculate angle
                    angle2 = calculate_angle(shoulder, elbow, wrist)
                    
                    # Visualize angle
                    cv2.putText(image2, str(angle2), 
                                tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    
                    # Curl counter logic
                    if angle2 > 160:
                        stage2 = "down"
                    if angle2 < 30 and stage2 =='down':
                        stage2="up"
                        counter2 +=1
                        print(counter2)
                    if compare_angle(angle1,angle2):
                        stage3="same"
                        print("Same")
                    else:
                        stage3="different"
                        print("Different")
                    frame_counter += 1
                    _, image2 = cap2.read()

                        # calling face_data function
                    face_width_in_frame = face_data(image2)
                        # finding the distance by calling function Distance
                    if face_width_in_frame != 0:
                        Distance = distance_finder(focal_length_found, KNOWN_WIDTH, face_width_in_frame)
                            # Drwaing Text on the screen
                            # cv.putText(
                            #     frame, f"Distance = {round(Distance,2)} CM", (50, 50), fonts, 1, (WHITE), 2)
                        AiPhile.textBGoutline(
                            image2,
                            f"Distance = {round(Distance,2)} CM",
                            (30, 100),
                            scaling=0.5,
                            text_color=AiPhile.GREEN,
                        )
                    if Distance > 80:
                        print("too far")
                        stage4="too far"
                    if Distance < 60:
                        print("too close")
                        stage4="too close"

                except:
                    pass   
                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
                            
                   # Rep data
                cv2.putText(image, 'reps', (15,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, str(counter), 
                            (10,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                            
                            # Stage data
                cv2.putText(image, 'STAGE', (65,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, stage, 
                            (60,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                            
                            
                            # Render curl counter
                            # Setup status box
                cv2.rectangle(image2, (0,0), (225,73), (245,117,16), -1)
                
                cv2.rectangle(image2, (0,400), (225,500), (100,50,204), -1)             

                            # Rep data
                cv2.putText(image2, 'reps2', (15,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image2, str(counter2), 
                            (10,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                            
                            # Stage data
                cv2.putText(image2, 'STAGE2', (65,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image2, stage2, 
                            (60,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

                cv2.putText(image2, stage3, 
                            (12,450), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.6, (255,255,255), 3, cv2.LINE_AA)            
                
                cv2.putText(image2, stage4, 
                            (12,385), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (205,133,63), 2, cv2.LINE_AA)            
                

                            # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                        )               
                            
                cv2.imshow('coach detection', image)

                        

                            # Render detections
                mp_drawing1.draw_landmarks(image2, results2.pose_landmarks, mp_pose1.POSE_CONNECTIONS,
                                        mp_drawing1.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing1.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                        )               
                            #!/usr/bin/python
                            #-*- coding: utf-8 -*-
                            

                            

                cv2.namedWindow("your body detection", 0)  # 0可調大小，注意：視窗名必須imshow裡面的一視窗名一直
                cv2.resizeWindow("your body detection", 850,650 )    # 設定長和寬
                cv2.imshow('your body detection', image2)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            cap.release()
            cap2.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    video()