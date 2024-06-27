from deepface import DeepFace
from PIL import Image, ImageDraw
from IPython.display import display

def faceAnalysis():
    imagePath = "RDJ.jpg"
    image = Image.open(imagePath)
    display(image)
    print(DeepFace.analyze(img_path=imagePath, detector_backend='retinaface'))

def faceBox():
    imagePath = "RDJ.jpg"
    image = Image.open(imagePath)
    analysis = DeepFace.analyze(img_path=imagePath, detector_backend='retinaface')

    region = analysis[0]['region']
    draw = ImageDraw.Draw(image)
    draw.rectangle([(region['x'], region['y']), (region['x'] + region['w'], region['y'] + region['h'])], outline="green", width=3)
    modifiedImagePath = "RDJ_Modified.jpg"
    image.save(modifiedImagePath)

    image = Image.open(modifiedImagePath)
    display(image)

def verifySamePerson():
    print(DeepFace.verify(img1_path="RDJ.jpg", img2_path="RDJ2.jpg", detector_backend='retinaface'))

verifySamePerson()