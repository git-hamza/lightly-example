import os
import cv2

# Function to parse YOLO format annotations and save ROIs
def save_roi_from_annotations(annotations_dir, image_dir, output_dir, classes_file=None):
    labels = {}
    if classes_file:
        with open(classes_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                label_name = line.strip()
                labels[i] = label_name

    images_list = os.listdir(image_dir)

    for img_file in images_list:
        img = cv2.imread(os.path.join(image_dir, img_file))
        height, width = img.shape[:2]

        annotation_file = f"{os.path.splitext(img_file)[0]}.txt" 

        with open(os.path.join(annotations_dir, annotation_file), 'r') as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):
                parts = line.strip().split()
                label_id = int(parts[0])

                if classes_file:
                    label_dir = os.path.join(output_dir, labels.get(label_id, str(label_id)))
                else:
                    label_dir = os.path.join(output_dir, str(label_id))

                os.makedirs(label_dir, exist_ok=True)

                x, y, w, h = map(float, parts[1:])
                x1, y1 = int((x - w / 2) * width), int((y - h / 2) * height)
                x2, y2 = int((x + w / 2) * width), int((y + h / 2) * height)

                roi = img[y1:y2, x1:x2]
                filename = f"{os.path.splitext(img_file)[0]}_{idx}"
                save_path = os.path.join(label_dir, f'{filename}.jpg')

                cv2.imwrite(save_path, roi)

if __name__ == "__main__":
    annotations_file = "yolo_dataset/labels"  # Replace with your YOLO format annotations file
    image_dir = "yolo_dataset/images"  # Replace with the directory containing your images
    output_dir = "output_data"  # Replace with the directory where you want to save ROIs
    classes_file = "classes.txt"  # Replace with your classes.txt file if available, otherwise set to None

    save_roi_from_annotations(annotations_file, image_dir, output_dir, classes_file)
