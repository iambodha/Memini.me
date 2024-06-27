from deepface import DeepFace
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def faceAnalysis(imagePath):
    image = Image.open(imagePath)
    return DeepFace.analyze(img_path=imagePath, detector_backend='retinaface')

def faceVerification(imagePath, imagePath2):
    return DeepFace.verify(img1_path= imagePath, img2_path= imagePath2, detector_backend='retinaface')

def imageCaptioning(imagePath):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    rawImage = Image.open(imagePath)
    inputs = processor(rawImage, return_tensors="pt")
    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)