# import needed modules
import cv2
from plate_detection import YoloInferenece
from Prediction import PlatesReader

# load plates detection model
plates_detector = YoloInferenece("car_plate_detector.pt", 512)

# get plates coordinates from car image;
# IMPORTANT NOTE: it takes an image FILE not a loaded images with cv2.imread
x,y,w,h = plates_detector.get_plate_xywh("./test.jpg")

# load original car pic as a matrix
car_img = cv2.imread("./test.jpg")

# crop plate from original car image -> plates matrix
plate = car_img[y:h,x:w]

# load ocr model
plate_reader = PlatesReader("ocr_model.hdf5")

# read the plate number from the cropped plate pic
# IMPORTANT NOTE: it takes an loaded image, not an image file
plate_num = plate_reader.read_plate(plate)
print(plate_num)
