import yaml
import os
import matplotlib.pyplot as plt

# Define paths to image and label directories, and class YAML file
data_dirs = ["data"]
class_yaml_path = "data.yaml"

# Load class names from YAML file
with open(class_yaml_path, 'r') as f:
    classes = yaml.safe_load(f)['names']
    if type(classes) != list:
        classes = list(classes.values())

print(classes)
# print(list(classes.values()))
# Initialize dictionary to store class-based statistics
class_stats = {c: {'num_labels': 0, 'num_images': 0} for c in classes}

# Loop through each data directory
for data_dir in data_dirs:
    # Define paths to image and label directories in current data directory
    image_dir = os.path.join(data_dir, 'images')
    label_dir = os.path.join(data_dir, 'labels')

    # Loop through images in image directory
    for filename in os.listdir(image_dir):
        if filename.endswith('.jpg'):
            # Read in corresponding YOLO format label file
            label_filename = os.path.splitext(filename)[0] + '.txt'
            label_filepath = os.path.join(label_dir, label_filename)
            with open(label_filepath, 'r') as f:
                labels = f.readlines()

            # Extract class labels from YOLO format label file
            class_labels = [classes[int(label.split()[0])] for label in labels]

            # Update class-based statistics
            for c in set(class_labels):
                class_stats[c]['num_labels'] += class_labels.count(c)
                class_stats[c]['num_images'] += 1

# Sort classes by number of labels in descending order
sorted_classes = sorted(classes, key=lambda c: class_stats[c]['num_labels'])

# Generate horizontal bar chart of class-based statistics
num_labels = [class_stats[c]['num_labels'] for c in sorted_classes]
num_images = [class_stats[c]['num_images'] for c in sorted_classes]


fig, ax = plt.subplots()
ax.barh(sorted_classes, num_labels)
ax.set_title('Number of Labels per Class')
ax.set_xlabel('Number of Labels')
ax.set_ylabel('Class')
plt.show()
fig.savefig('numeroflabels.jpg')

fig, ax = plt.subplots()
ax.barh(sorted_classes, num_images)
ax.set_title('Number of Images per Class')
ax.set_xlabel('Number of Images')
ax.set_ylabel('Class')
plt.show()
fig.savefig('numberofimages.jpg')

for i in range(len(sorted_classes)):
    print(sorted_classes[i], num_images[i])
