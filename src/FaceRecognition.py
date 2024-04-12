import os
import cv2

def orb_sim(img1, img2):
    """
    Calcula la similitud entre dos imágenes utilizando el algoritmo ORB para detectar y describir características.
    
    Args:
    - img1: La primera imagen (en escala de grises) representada como un arreglo numpy.
    - img2: La segunda imagen (en escala de grises) representada como un arreglo numpy.
    
    Returns:
    - El porcentaje de similitud entre las dos imágenes.
    """
    # Crea un objeto ORB (Oriented FAST and Rotated BRIEF).
    orb = cv2.ORB_create()
    
    # Detecta y calcula los descriptores de las características en ambas imágenes.
    kpa, descr_a = orb.detectAndCompute(img1, None)
    kpb, descr_b = orb.detectAndCompute(img2, None)
    
    # Crea un objeto BFMatcher (Brute-Force Matcher) para hacer coincidir descriptores.
    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    # Encuentra las coincidencias entre los descriptores de ambas imágenes.
    matches = comp.match(descr_a, descr_b)
    
    # Filtra las coincidencias para obtener las regiones similares.
    regiones_similares = [i for i in matches if i.distance < 70]
    
    # Calcula el porcentaje de similitud entre las dos imágenes.
    if len(matches) == 0:
        return 0
    return len(regiones_similares) / len(matches)



def reconocimiento_cara(cara, carpeta):
    cantidad_imagenes = 0
    """
    Realiza el reconocimiento facial comparando una cara con imágenes almacenadas en una carpeta.
    
    Args:
    - cara: La imagen de la cara a reconocer (en escala de grises) representada como un arreglo numpy.
    - carpeta: La ruta de la carpeta que contiene las subcarpetas con imágenes de referencia.
    
    Returns:
    - Un diccionario donde las claves son los nombres de las subcarpetas y los valores son la cantidad de coincidencias encontradas.
    """
    # Inicializa el diccionario para almacenar el resultado por carpeta.
    resultado_por_carpeta = {}
    # Itera sobre cada subdirectorio en la carpeta especificada.
    for subdirectorio in os.listdir(carpeta):
        ruta_subdirectorio = os.path.join(carpeta, subdirectorio)
        
        # Verifica si el elemento en la ruta es una carpeta.
        if os.path.isdir(ruta_subdirectorio):
            # Inicializa el contador de coincidencias para este subdirectorio.
            cantidad_coincidencias = 0
            
            # Itera sobre cada imagen en el subdirectorio.
            for imagen_nombre in os.listdir(ruta_subdirectorio):
                ruta_imagen = os.path.join(ruta_subdirectorio, imagen_nombre)
                
                # Lee la imagen y la convierte a escala de grises.
                imagen = cv2.imread(ruta_imagen, 0)
                
                # Calcula la similitud entre la cara y la imagen actual.
                similitud = orb_sim(cara, imagen)
                
                # Si la similitud es mayor o igual a 0.98, se considera una coincidencia.
                if similitud >= 0.95:
                    cantidad_coincidencias += 1

                cantidad_imagenes += 1
            
            # Almacena la cantidad de coincidencias encontradas para este subdirectorio.
            resultado_por_carpeta[subdirectorio] = cantidad_coincidencias
    
    print("Cantidad de imagenes: " , cantidad_imagenes)
    # Devuelve el diccionario con el resultado del reconocimiento facial por carpeta.
    return resultado_por_carpeta

# Ejemplo de uso:
cara = cv2.imread("cara.jpg", 0)  # Supongamos que tienes una imagen de la cara a reconocer
carpeta = "captured_photos"
resultado = reconocimiento_cara(cara, carpeta)
print(resultado)
