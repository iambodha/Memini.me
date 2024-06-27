from deepface import DeepFace
from PIL import Image, ImageDraw
from IPython.display import display

def faceAnalysis():
    imagePath = "RDJ.jpg"
    image = Image.open(imagePath)
    display(image)
    print(DeepFace.analyze(img_path=imagePath, detector_backend='retinaface'))

def verifySamePerson():
    print(DeepFace.verify(img1_path="RDJ.jpg", img2_path="RDJ2.jpg"))

faceAnalysis()