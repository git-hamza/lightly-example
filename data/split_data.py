import os
import shutil

# Function to split a directory into train and test based on a percentage
def split_directory(input_dir, output_train_dir, output_test_dir, split_percentage):
    # Create train and test directories if they don't exist
    os.makedirs(output_train_dir, exist_ok=True)
    os.makedirs(output_test_dir, exist_ok=True)
    
    # List subdirectories (classes)
    classes = os.listdir(input_dir)
    
    for class_dir in classes:
        class_path = os.path.join(input_dir, class_dir)
        
        # Create class-specific train and test directories
        train_class_dir = os.path.join(output_train_dir, class_dir)
        test_class_dir = os.path.join(output_test_dir, class_dir)
        os.makedirs(train_class_dir, exist_ok=True)
        os.makedirs(test_class_dir, exist_ok=True)
        
        # List images in the class directory
        images = os.listdir(class_path)
        num_images = len(images)
        
        # Calculate the number of images for the train and test sets
        num_train = int(num_images * split_percentage)
        num_test = num_images - num_train
        
        # Split images into train and test sets
        train_images = images[:num_train]
        test_images = images[num_train:]
        
        # Copy images to train and test directories
        for image in train_images:
            src = os.path.join(class_path, image)
            dst = os.path.join(train_class_dir, image)
            shutil.copy(src, dst)
        
        for image in test_images:
            src = os.path.join(class_path, image)
            dst = os.path.join(test_class_dir, image)
            shutil.copy(src, dst)

# Input directory containing subdirectories with images
input_directory = "dataset"

# Output directories for train and test sets
output_train_directory = "dataset_train"
output_test_directory = "dataset_test"

# Specify the split percentage (e.g., 0.8 for 80% train, 20% test)
split_percentage = 0.8

if split_percentage < 0 or split_percentage > 1:
    print("Invalid split percentage. provide value between 0 and 1.")
else:
    split_directory(input_directory, output_train_directory, output_test_directory, split_percentage)
    print(f"Dataset split into train and test with {split_percentage*100}% for train and {(1-split_percentage)*100}% for test.")
