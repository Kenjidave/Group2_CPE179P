import cv2
import numpy as np

def preprocess_receipt(image_path):
    print(f"Loading image: {image_path}")
    img = cv2.imread(image_path)

    if img is None:
        print("Error: Image not found.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    adjusted = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    normalized = adjusted.astype('float32') / 255.0

    print("Preprocessing complete. Image shape:", normalized.shape)

    # Save the output to verify it works without a UI
    cv2.imwrite("preprocessed_output.jpg", adjusted)
    print("Saved preprocessed image as 'preprocessed_output.jpg'")

# Run the test
preprocess_receipt("sample_receipt.jpg") # Ensure you have a sample_receipt.jpg in your folder

