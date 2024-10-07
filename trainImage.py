import os
import cv2
import numpy as np
from PIL import Image

def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)

    faces, Ids = getImagesAndLabels(trainimage_path)
    print(f"Number of faces: {len(faces)}, Number of IDs: {len(Ids)}")

    # Ensure the directory exists for saving the model
    trainimagelabel_dir = os.path.dirname(trainimagelabel_path)
    if not os.path.exists(trainimagelabel_dir):
        os.makedirs(trainimagelabel_dir)

    # Check if faces and IDs have been extracted
    if not faces or not Ids:
        message.configure(text="No faces found. Please check your image paths and filenames.")
        return

    try:
        recognizer.train(faces, np.array(Ids))
        recognizer.save(trainimagelabel_path)
        res = "Image Trained successfully"
    except cv2.error as e:
        res = f"OpenCV error: {e}"
    except Exception as e:
        res = f"An error occurred: {e}"

    message.configure(text=res)
    text_to_speech(res)

def getImagesAndLabels(path):
    newdir = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    imagePath = [
        os.path.join(newdir[i], f)
        for i in range(len(newdir))
        for f in os.listdir(newdir[i]) if f.endswith(('png', 'jpg', 'jpeg'))
    ]
    faces = []
    Ids = []

    for imagePath in imagePath:
        print(f"Processing image: {imagePath}")
        if not os.path.exists(imagePath):
            print(f"Image not found: {imagePath}")
            continue
        
        pilImage = Image.open(imagePath).convert("L")
        imageNp = np.array(pilImage, "uint8")
        Id = int(os.path.split(imagePath)[-1].split("_")[1])
        faces.append(imageNp)
        Ids.append(Id)

    return faces, Ids
