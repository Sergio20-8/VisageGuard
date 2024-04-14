import cv2
import os 

if __name__ == "__main__":
    
    if not os.path.exists("faces"):
        os.makedirs("faces")
        print("Nueva carpeta creada: faces")

    if not os.path.exists("photos"):
        os.makedirs("photos")
        print("Nueva carpeta creada: photos")

 