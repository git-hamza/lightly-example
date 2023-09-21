# lightly-example

---

This repository is the extension of [lightly](https://github.com/lightly-ai/lightly/tree/master). It currently has
preprocessing script for yolo format dataset and notebooks for training and inference of two architechtures `BYOL` 
and `SimCLR`. For more details please visit [lightly](https://github.com/lightly-ai/lightly/tree/master).

## Implementation Details:
Notebooks for the respective architechtures are self-explanatory and easier to execute. 

The script inside data directory is helpful for preprocessing of yolo format annotations.

- `class-based-statistics.py : ` class based statistics will be provided for the yolo format annotations.
- `visualize_annotations.py : ` visualize the yolo format annotations.
- `save_roi_from_yolo_annotations.py : ` This script will take yolo format annotaitons and
convert the data into the lightly training format i.e., have each label image into its respective directory.
- `split_data.py : ` to split the lightly model format data. 

