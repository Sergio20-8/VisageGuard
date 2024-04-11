import cv2
import os
from datetime import datetime
from mtcnn.mtcnn import MTCNN

class FaceCapture:

    def __init__(self):
        # Inicializar el detector de rostros MTCNN
        self.detector = MTCNN()
        # Inicializar el clasificador de rostros Haar
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Inicializar la cámara
        self.cap = cv2.VideoCapture(0)  # La cámara predeterminada
        # Establecer la resolución deseada para la cámara (aquí se establece a 640x480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def generate_folder_name(self):
        now = datetime.now()
        return now.strftime("%Y%m%d_%H%M%S")

    def capture_photos(self, nombre):

        while True:


            # Leer un frame de la cámara
            ret, frame = self.cap.read()
        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detectar rostros en el frame
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Dibujar un rectángulo alrededor de cada rostro detectado
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Mostrar el frame con los rectángulos dibujados en una ventana
            cv2.imshow('Camera', frame)

            # Esperar 1 milisegundo y verificar si se presiona la tecla 'q' para salir del bucle
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                FaceCapture.close_camera()
                break
            elif key & 0xFF == ord('s'):  # Si se presiona la tecla 's', tomar 30 capturas y guardarlas en una nueva carpeta
                cv2.putText(frame, 'Presionaste S - Capturando...', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                folder_name = self.generate_folder_name()
                folder_path = os.path.join('captured_photos', folder_name)
                os.makedirs(folder_path)

                capture_count = 0
                while capture_count < 5:
                    # Leer un frame de la cámara
                    ret, frame = self.cap.read()
                
                    # Detectar rostros en el frame usando MTCNN
                    faces = self.detector.detect_faces(frame)

                    for result in faces:
                        # Recortar la región de la cara del frame
                        x, y, w, h = result['box'] 

                        face_region_grey = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)

                        # Guardar la región de la cara en la carpeta
                        photo_path = os.path.join(folder_path, f'{nombre}_{capture_count}.jpg')
                        cv2.imwrite(photo_path, face_region_grey)
                        print(f"Fotografía {capture_count+1} (cara) guardada como '{photo_path}'.")
                        capture_count += 1
                        cv2.waitKey(10)  # Pequeño retardo para permitir un tiempo de procesamiento mínimo

                        # Dibujar un rectángulo alrededor de cada rostro detectado en el frame original (para mostrar en pantalla)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    # Mostrar el frame con el rectángulo dibujado en una ventana
                    cv2.imshow('Camera', frame)

                    # Esperar 1 milisegundo y verificar si se presiona la tecla 'q' para salir del bucle
                    key = cv2.waitKey(1)
                    if key & 0xFF == ord('q'):
                        FaceCapture.close_camera()
                        break
                
                print("Todas las fotografías fueron tomadas y guardadas en la carpeta:", folder_path)
                break    

    def close_camera(self):
        # Liberar la cámara y cerrar todas las ventanas abiertas
        self.cap.release()
        cv2.destroyAllWindows() 
