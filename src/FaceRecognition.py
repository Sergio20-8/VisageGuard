import cv2
import os
import face_recognition

imageFacesPath = "C:/Users/hidal/OneDrive/Desktop/VisageGuard/faces"

faces_Encodings = []
faces_Names = []

for file_name in os.listdir(imageFacesPath):
    image = cv2.imread(os.path.join(imageFacesPath, file_name))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    face_encodings = face_recognition.face_encodings(image, known_face_locations=[(0, 150, 150, 0)])[0]
 
    faces_Encodings.append(face_encodings)
    name = file_name.replace("_", " ").split(".")[0]  # Reemplazar guiones bajos por espacios y eliminar la extensión del archivo
   
    faces_Names.append(name) 

# Leyendo el video
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Detector facial
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True: 
    ret, frame = cap.read()
    if ret == False:
        break
    frame = cv2.flip(frame, 1)
    orig = frame.copy()

    faces = faceClassif.detectMultiScale(frame, 1.1, 5)

    for(x, y, w, h) in faces:
        face = orig[y:y + h, x:x + w]

        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        actual_face_encodign = face_recognition.face_encodings(face, known_face_locations=[(0, w, h, 0)])[0]
        result = face_recognition.compare_faces(faces_Encodings, actual_face_encodign)
        print(result)

        if True in result:
            index = result.index(True)
            name = faces_Names[index]
            color = (125, 220, 0)
        else:
            name = "Desconocido"
            color = (60,50,255)
        
        cv2.rectangle(frame, (x,y+h), (x + w, y + h + 30), color, -1)
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)
        cv2.putText(frame, name, (x, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_4)

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
