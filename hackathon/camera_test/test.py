from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import picamera

camera = picamera.PiCamera()
camera.capture('image1.jpg')
print("1")
block_blob_service = BlockBlobService(account_name='ccblobstorage', account_key='RSU4i/ssYCWnz7z8JSKJbm3RQGaJfuGj3/nYPGQtTOFJ/KOOx26mVxoEUnYHVsHTHAcKBe1+LG23e+k3iOvL8w==')
print("2")
block_blob_service.create_blob_from_path(
    'ccblobcontainer',
    'firstblood.jpg',
    'image1.jpg',
    content_settings=ContentSettings(content_type='image/jpeg'))

print("3")
