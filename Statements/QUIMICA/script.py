import sys
import os

def rename(ruta_completa, carpeta_actual, nombre_archivo):
    new_name = "r"+nombre_archivo
    os.rename(ruta_completa,new_name)

#python script.py carpeta_libros
# se almacena en la carpeta png

if __name__ == "__main__":
    
    #ruta de la carpeta como argumento
    carpeta = sys.argv[1]

    # Recorrer el carpeta y sus subcarpetas para obtener el nombre de cada archivo
    for carpeta_actual, subcarpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            # Imprimir la ruta completa del archivo (nombre completo incluyendo la ruta)
            ruta_completa = os.path.join(carpeta_actual, archivo)
            #print(carpeta_actual)
            #print(subcarpetas)
            print(ruta_completa)
            #print(subcarpetas)
            
            nombre_archivo = archivo
            rename(ruta_completa, carpeta_actual, nombre_archivo)        



print("Proceso de conversión finalizado")