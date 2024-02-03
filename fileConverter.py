from pillow_heif import register_heif_opener
from PIL import Image
# Open HEIF or HEIC file
register_heif_opener()
image1 = Image.open('IMG_0641.HEIC')
# image2 = Image.open('IMG_8543.HEIC')
# image3 = Image.open('IMG_8544.HEIC')
# image4 = Image.open('IMG_8545.HEIC')
# Convert to JPEG
image1.convert('RGB').save('siccwhip.jpg')
# image2.convert('RGB').save('image2.jpg')
# image3.convert('RGB').save('image3.jpg')
# image4.convert('RGB').save('image4.jpg')