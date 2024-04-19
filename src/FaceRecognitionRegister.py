import cv2
import os
import face_recognition
from ExcelWriter import escribir_en_excel
import datetime

imageFacesPath = "C:/Users/hidal/OneDrive/Desktop/VisageGuard/faces"

# Llenar el diccionario con los carnets de los alumnos y False para indicar que no han sido reconocidos
faces_Encodings = {}
for file_name in os.listdir(imageFacesPath):
    image = cv2.imread(os.path.join(imageFacesPath, file_name))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    face_encoding = face_recognition.face_encodings(image, known_face_locations=[(0, 150, 150, 0)])[0]
    carnet = file_name.replace("_", " ").split(".")[0]  # Reemplazar guiones bajos por espacios y eliminar la extensión del archivo
    # Extracting the part before the underscore
    faces_Encodings[carnet] = {"encoding": face_encoding, "reconocido": False, "hora_llegada": None, "detecciones": 0}

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True: 
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    orig = frame.copy()


    faces = faceClassif.detectMultiScale(frame, 1.1, 20)

    for (x, y, w, h) in faces:
        face = orig[y:y + h, x:x + w]
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        actual_face_encoding = face_recognition.face_encodings(face, known_face_locations=[(0, w, h, 0)])
        
        

        if len(actual_face_encoding) > 0:
            actual_face_encoding = actual_face_encoding[0]
            # Comparar la codificación facial con las codificaciones de los alumnos
            for carnet, info in faces_Encodings.items():
                if not info["reconocido"]:
                    result = face_recognition.compare_faces([info["encoding"]], actual_face_encoding)[0]
                    if result:
                        print(f"¡ Reconocido: {carnet}!")
                        info["detecciones"] += 1
                        if info["detecciones"] > 6:
                            info["reconocido"] = True
                            info["hora_llegada"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            print(f"¡El alumno con carnet {carnet} ha sido reconocido a las {info['hora_llegada']}!")

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

# Llamar a la función para escribir en el archivo Excel
nombre_archivo_excel = "Asistencia.xlsx"
escribir_en_excel(faces_Encodings, nombre_archivo_excel)
