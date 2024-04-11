import cv2
from FaceCapture import FaceCapture
from FaceRecognition import FaceRecognition

if __name__ == "__main__":
    fc = FaceCapture()

    print("Presiona:")
    print("'r' para registrar un rostro")
    print("'c' para cancelar")

    tecla = input(">>> ")
 
    fc.capture_photos(tecla) 
           
            


        

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
    
 