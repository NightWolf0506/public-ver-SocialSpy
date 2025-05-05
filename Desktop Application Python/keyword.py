import cv2
import pytesseract
from PIL import Image
import os

def extract_text(image_path):
    try:
        image = cv2.imread(image_path)
        TEXT_THRESHOLD = 10 
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, TEXT_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
        
        mask = cv2.bitwise_not(thresh)
        occlusion_mask = cv2.dilate(mask, None, iterations=2)
        occluded_image = cv2.bitwise_and(gray, gray, mask=occlusion_mask)
        text = pytesseract.image_to_string(Image.fromarray(occluded_image))
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""


def parse():
    a = input("Enter the Keyword : ").lower()
    folder_titles = [
            'IPostSS',
            'IMessSS'
            ]

    for folder in folder_titles:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_directory, folder)
        images = [img for img in os.listdir(folder_path) if img.endswith('.png')]

        def add_images_to_pdf(images):

            for i, image_file in enumerate(images):
                image_path = os.path.join(folder_path, image_file)
                t = extract_text(image_path).lower()
                #print(t)
                if a in t:
                    print("Found")
                else:
                    print("Not Found")
                    #os.remove(image_path)

        if images:
            add_images_to_pdf(images)
        else:
            print("Empty Folder")
parse()
