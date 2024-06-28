from deepface import DeepFace
from PIL import Image, ImageDraw
from transformers import BlipProcessor, BlipForConditionalGeneration
import numpy as np
import os

def faceAnalysis(imagePath):
    image = Image.open(imagePath)
    return DeepFace.analyze(img_path=imagePath, detector_backend='retinaface')

def faceVerification(imagePath, imagePath2):
    result = DeepFace.verify(img1_path=imagePath, img2_path=imagePath2, detector_backend='retinaface')
    return result['verified']

def imageCaptioning(imagePath):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    rawImage = Image.open(imagePath)
    inputs = processor(rawImage, return_tensors="pt")
    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

def cutFace(imagePath, outputPath, analysis):
    image = Image.open(imagePath)
    region = analysis['region']
    x, y, w, h = region['x'], region['y'], region['w'], region['h']

    img_np = np.array(image)
    
    x1, y1 = max(x, 0), max(y, 0)
    x2, y2 = min(x + w, img_np.shape[1]), min(y + h, img_np.shape[0])

    faceImg = img_np[y1:y2, x1:x2]

    facePil = Image.fromarray(faceImg)

    facePil.save(outputPath)