import cv2
import os
from mtcnn.mtcnn import MTCNN

class FaceRecognition:
    
    def __init__(self):
        # Inicializar el detector de rostros MTCNN
        self.detector = MTCNN()
        # Inicializar el clasificador de rostros Haar
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Cargar las capturas almacenadas
        self.stored_faces = self.load_stored_faces()

    def load_stored_faces(self):
        stored_faces = []
        for root, dirs, files in os.walk('captured_photos'):
            for file in files:
                if file.endswith('.jpg'):
                    image_path = os.path.join(root, file)
                    stored_faces.append(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE))
        return stored_faces

    def recognize_faces(self):
        # Inicializar la cámara
        cap = cv2.VideoCapture(0)  # La cámara predeterminada
        # Establecer la resolución deseada para la cámara (aquí se establece a 640x480)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while True:
            # Leer un frame de la cámara
            ret, frame = cap.read()
        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detectar rostros en el frame
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Comparar cada rostro detectado con las capturas almacenadas
            for (x, y, w, h) in faces:
                face_region = gray[y:y+h, x:x+w]
                # Aquí puedes implementar tu algoritmo de comparación facial con las capturas almacenadas
                recognized = self.compare_with_stored_faces(face_region)
                if recognized:
                    cv2.putText(frame, 'Rostro Reconocido', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Mostrar el frame con los rectángulos dibujados en una ventana
            cv2.imshow('Reconocimiento Facial', frame)

            # Esperar 1 milisegundo y verificar si se presiona la tecla 'q' para salir del bucle
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break

        # Liberar la cámara y cerrar todas las ventanas abiertas
        cap.release()
        cv2.destroyAllWindows() 

    def compare_with_stored_faces(self, face_region):
        # Aquí puedes implementar tu algoritmo de comparación facial con las capturas almacenadas
        # Por ejemplo, puedes utilizar el reconocimiento facial de OpenCV (Eigenfaces, Fisherfaces, LBPH, etc.)
        # Devuelve True si el rostro es reconocido, False en caso contrario
        recognized = False
        for stored_face in self.stored_faces:
            # Aquí debes realizar la comparación entre el rostro almacenado y el rostro actual
            # Por ejemplo, puedes usar la función cv2.face.LBPHFaceRecognizer_create() de OpenCV para el reconocimiento facial
            pass
        return recognized

