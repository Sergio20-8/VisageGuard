import cv2
from FaceCapture import FaceCapture


if __name__ == "__main__":
    fc = FaceCapture()

    print("Presiona:")
    print("'r' para registrar un rostro")
    print("'c' para cancelar")

    tecla = input(">>> ")
 
    fc.capture_photos(tecla) 

 
    
 