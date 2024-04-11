import cv2
from FaceCapture import FaceCapture
from FaceRecognition import FaceRecognition

if __name__ == "__main__":
    face_capture = FaceCapture()

    while True:
        print("Presiona:")
        print("'r' para captura de video.")
        print("     'q' para liberar la camera")
        print("     's' para agregar un nuevo rostro")
        print("'t' para terminar la captura facial")
        nombre = input("Ingrese el nombre de la persona: ")
        face_capture.capture_photos(nombre)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('x'):
            FaceCapture.close_camera()
            break
        

    #recognizer = FaceRecognition()S
    #recognizer.recognize_faces()

'''
    recognizer = FaceRecognition()
    cap = cv2.VideoCapture(0)  # Inicializar la cámara
    while True:
        ret, frame = cap.read()  # Leer un frame de la cámara
        frame_with_recognition = recognizer.recognize_faces(frame)  # Reconocer caras en el frame
        cv2.imshow('Face Recognition', frame_with_recognition)  # Mostrar el frame con las caras reconocidas
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
'''
    
 