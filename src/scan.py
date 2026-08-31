import argparse
import cv2
import imutils
import pytesseract
from skimage.filters import threshold_local
from google.colab.patches import cv2_imshow # For Colab display

from transform import four_point_transform
from ocr_parser import parse_receipt_data

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="Path to the image to be scanned")
    args = vars(ap.parse_args())

    # Load the image and resize it
    image = cv2.imread(args["image"])
    if image is None:
        print(f"Error: Could not load image at {args['image']}")
        return

    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    # Convert the image to grayscale, blur it, and find edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    print("STEP 1: Edge Detection")
    cv2_imshow(edged) # Use cv2_imshow for Colab

    # Find contours in the edged image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    screenCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        raise ValueError("Could not find a 4-point contour for the document.")

    print("STEP 2: Find contours of paper")
    contour_img = image.copy()
    cv2.drawContours(contour_img, [screenCnt], -1, (0, 255, 0), 2)
    cv2_imshow(contour_img) # Use cv2_imshow for Colab

    # Apply four-point transform and adaptive thresholding
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset=10, method="gaussian")
    scanned = (warped > T).astype("uint8") * 255

    print("STEP 3: Apply perspective transform & scan effect")
    cv2_imshow(imutils.resize(scanned, height=650)) # Use cv2_imshow for Colab

    # Perform OCR and parse data
    text_data = pytesseract.image_to_string(scanned, lang='eng')
    print("
--- Extracted Raw Text ---")
    print(text_data)

    receipt_info = parse_receipt_data(text_data)
    print("
--- Parsed Receipt Information ---")
    for key, value in receipt_info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    # For execution in Colab, you might need to mock argparse or provide default args
    # Example: sys.argv = ['scan.py', '--image', 'sample_data/raw/receipt.jpg']
    # Then call main()
    # For direct execution, remove/comment out the Colab specific display and args mocking
    main()