import xml.etree.ElementTree as ET
import pdfplumber
from PIL import Image
import sys
import os
from tqdm import tqdm

from firebase_admin import auth

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials, storage

# Application Default credentials are automatically created.
cred = credentials.Certificate('./service-account-file.json')

app = firebase_admin.initialize_app(cred, {"storageBucket": "repository-exercises.appspot.com"})
db = firestore.client()

xml_string = '''
<data>
  <course>Raz. Mat.</course>
  <courseCode>10</courseCode>
  <topic>fechas y calendarios</topic>
  <topicCode>17</topicCode>
  <answer>1987</answer>
  <correctAlternative>E</correctAlternative>
</data>
'''



def uploadToStorage(current_directory,filename):
  #progress_bar = tqdm(total=len(array_images), desc="Procesando")
    try:
        path = os.path.join(current_directory,filename)
        bucket = storage.bucket()
        blob = bucket.blob("evaluation_question/"+path)
        blob.upload_from_filename(path)
        blob.make_public()
        uri_question = blob.public_url
        
        path_answer = os.path.join(current_directory,'r'+ filename)
        blob = bucket.blob("evaluation_answer/"+path_answer)
        blob.upload_from_filename(path_answer)
        blob.make_public()
        uri_answer = blob.public_url
        return (uri_question, uri_answer)
        
    except Exception as e:
        print("Error al subir el archivo png:", str(e))
    #progress_bar.update(1)
  #progress_bar.close()

def uploadToFirestore(filename, path, uri_question, uri_answer):
  # Parsear el string XML
  #root = ET.fromstring(xml_string)

  tree = ET.parse(path[:-4]+".xml")
  #tree = ET.parse(os.path.join())
  root = tree.getroot()

  # Imprimir los elementos del XML
  new_question = {}
  for child in root:
      new_question[child.tag] = child.text
      #print(f"{child.tag}: {child.text}")
  new_question['uri'] = uri_question

  # Agrega el nuevo registro a la colección "usuarios"
  update_time ,new_question_ref = db.collection("evaluation_question").add(new_question)
  new_question_ref = new_question_ref.id
  # Obtiene el ID del nuevo documento
  print(f"Added document with id {new_question_ref}")

  new_answer = {
     'uri': uri_answer
  }
  
  new_answer_ref = db.collection("evaluation_answer").document(new_question_ref)
  new_answer_ref.set(new_answer)

  """
  nuevo_registro = {
      'idQuestion': ,
      'uri': uri,
      'course': ,
      'courseCode':,
      'topic':,
      'topicCode':,
      'alternatives':[],
      'answer':
  }"""  
    

def main():
  for current_directory, subdirectory, files in os.walk(directory):
     ## recorremos solo enunciados, ignoramos xml y resoluciones
     _files = [f for f in os.listdir(current_directory) if (os.path.isfile(os.path.join(current_directory, f)) and (f[-4:] == ".png") and (f[0] != 'r'))]
     for file in _files:
        path_file = os.path.join(current_directory,file)
        if(os.path.isfile((path_file[:-4]+".xml"))):        ########### verificar que existe metadata   
          uri_question, uri_answer = uploadToStorage(current_directory,file)
          uploadToFirestore(file,path_file, uri_question, uri_answer)

if __name__ == '__main__':
    directory = sys.argv[1] 
    main()