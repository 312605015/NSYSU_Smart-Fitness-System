import multiprocessing as multi
import mediapipe as mp
import cv2
import numpy as np
import time 
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

mp_drawing1 = mp.solutions.drawing_utils
mp_drawing_styles1 = mp.solutions.drawing_styles
mp_pose1 = mp.solutions.pose

angle1 = 0.
angle2 = 0.

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
    cap = cv2.VideoCapture('D:/python/66.mp4')
    cap2 = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0 
    stage = None

    # Curl counter variables
    counter2 = 0 
    stage2 = None

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
            

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark
                    
                    # Get coordinates
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    
                    # Calculate angle
                    angle1 = calculate_angle(hip, knee, ankle)
                    
                    # Visualize angle
                    cv2.putText(image, str(angle1), 
                                tuple(np.multiply(knee, [600,900]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    
                    # Curl counter logic
                    if angle1 < 60:
                        stage = "down"
                    if angle1 > 160 and stage =='down':
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
                    hip = [landmarks[mp_pose1.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose1.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose1.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose1.PoseLandmark.LEFT_KNEE.value].y]
                    ankle = [landmarks[mp_pose1.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose1.PoseLandmark.LEFT_ANKLE.value].y]
                    
                    # Calculate angle
                    angle2 = calculate_angle(hip, knee, ankle)
                    
                    # Visualize angle
                    cv2.putText(image2, str(angle2), 
                                tuple(np.multiply(knee, [640, 480]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    
                    # Curl counter logic
                    if angle2 > 160:
                        stage2 = "down"
                    if angle2 < 30 and stage2 =='down':
                        stage2="up"
                        counter2 +=1
                        print(counter2)
                            
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
                
                cv2.namedWindow("your body detection", 0)  # 0可調大小，注意：視窗名必須imshow裡面的一視窗名一直
                cv2.resizeWindow("your body detection", 1000,800 )    # 設定長和寬
                cv2.imshow('your body detection', image2)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            cap.release()
            cap2.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    video()