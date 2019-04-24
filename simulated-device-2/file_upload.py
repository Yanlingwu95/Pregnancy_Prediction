from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import picamera

# camera = picamera.PiCamera()
# camera.capture('image1.jpg')
print("1")
block_blob_service = BlockBlobService(account_name='cs2743a315b9ea3x49fdxb30', account_key='fiGff9v/aulWyb6T3eUupbS4hS2ygfwmTmAQ55+xA+q+enpqIJfaPRfqSQ9paP2idEoj+FYaU7wX+FWWHfSkPQ==')
print("2")
block_blob_service.create_blob_from_path(
    'mydata',
    'firstdata.json',
    'row_data.json',
    content_settings=ContentSettings(content_type='json'))

print("3")
