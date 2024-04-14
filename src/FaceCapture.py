import cv2
import os

# Inicializar la captura de video desde la cámara
cap = cv2.VideoCapture(1)  # 0 para la cámara predeterminada

# Carpeta donde se guardarán las fotos (fuera de la carpeta src)
folder_name = "faces/"
os.makedirs(folder_name, exist_ok=True)  # Crear la carpeta si no existe

carnet = input("Ingrese el carnet ('q' para salir): ")

if  not carnet.lower() == 'q':
    while True:
        # Capturar un frame desde la cámara
        ret, frame = cap.read()
        if not ret:
            print("Error: no se pudo capturar el fotograma desde la cámara.")
            break

        # Mostrar el frame en una ventana
        cv2.imshow("Registro de rostro", frame)

        # Esperar a que se presione una tecla
        key = cv2.waitKey(1)

        if key == 27:
            print("Procesando captura...")
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            # Realizar la detección de rostros en la imagen en escala de grises
            faces = face_cascade.detectMultiScale(frame, 1.1, 5)

            if len(faces) > 0:
                print("Se detectaron rostros en la imagen. Guardando captura...")
                # Guardar solo el primer rostro detectado
                x, y, w, h = faces[0]
                face = frame[y:y+h, x:x+w]
                face = cv2.resize(face, (150, 150))  # Redimensionar el rostro a 150x150
                file_name = os.path.join(folder_name, f"{carnet}.jpg")
                cv2.imwrite(file_name, face)
                print(f"Captura guardada como '{file_name}'")
            else:
                print("No se detectaron rostros en la imagen.")

            print("Proceso de captura finalizado.")
            break
        elif key == "s":  # Si se presiona la tecla 'Esc', salir del bucle
            print("Se presionó la tecla 's'. Saliendo...")
            break

    # Liberar la captura de video y cerrar todas las ventanas abiertas
    
else:
    print("Cerrando...")
cap.release()
cv2.destroyAllWindows()    
