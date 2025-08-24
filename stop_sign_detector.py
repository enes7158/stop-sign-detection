import cv2
import numpy as np
import os


def detect_red_regions(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
    red_mask = mask1 + mask2
    
    return red_mask


def detect_stop_sign(image_path, output_dir):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image {image_path}")
        return
    
    red_mask = detect_red_regions(image)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    result_image = image.copy()
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 500:
            continue
            
        x, y, w, h = cv2.boundingRect(contour)
        
        aspect_ratio = float(w) / h
        if 0.7 <= aspect_ratio <= 1.3:
            cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            center_x = x + w // 2
            center_y = y + h // 2
            
            cv2.circle(result_image, (center_x, center_y), 5, (255, 0, 0), -1)
            
            print(f"STOP sign detected - Center coordinates: ({center_x}, {center_y})")
    
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(output_dir, f"{name}_detected{ext}")
    cv2.imwrite(output_path, result_image)
    print(f"Result saved to: {output_path}")


def process_dataset():
    dataset_dir = "stop_sign_dataset"
    output_dir = "detection_results"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    
    for file in os.listdir(dataset_dir):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(file)
    
    print(f"Found {len(image_files)} images to process")
    
    for image_file in image_files:
        image_path = os.path.join(dataset_dir, image_file)
        print(f"\nProcessing: {image_file}")
        detect_stop_sign(image_path, output_dir)


if __name__ == "__main__":
    process_dataset()