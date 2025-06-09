import xml.etree.ElementTree as ET
import sys, os
from collections import defaultdict

def extract_class_name_pairs():
    ui_path = os.path.join(os.path.dirname(__file__), "Achse.ui")
    try:
        tree = ET.parse(ui_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error reading UI file: {e}")
        return

    exclude_classes = {"QWidget", "QGroupBox", "QComboBox", "QLabel"}
    class_groups = defaultdict(list)

    for widget in root.iter("widget"):
        class_name = widget.attrib.get("class")
        object_name = widget.attrib.get("name")
        if class_name and object_name and class_name not in exclude_classes:
            class_groups[class_name].append(object_name)

    for cls in sorted(class_groups):
        for name in sorted(class_groups[cls]):
            print(name)

if __name__ == "__main__":
    extract_class_name_pairs()
