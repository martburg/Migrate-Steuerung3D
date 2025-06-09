import xml.etree.ElementTree as ET
import os

def patch_ui_file(ui_filename="Achse.ui", out_filename="Achse_patched.ui"):
    ui_filename = os.path.join(os.path.dirname(__file__), "Achse.ui")
    print(f"🔍 Patching {ui_filename}...")
    try:
        tree = ET.parse(ui_filename)
        root = tree.getroot()
    except Exception as e:
        print(f"❌ Failed to load {ui_filename}: {e}")
        return

    count = 0

    for widget in root.iter("widget"):
        class_type = widget.attrib.get("class")
        name = widget.attrib.get("name")

        if class_type == "QRadioButton" and name and name.startswith("rb"):
            # Change to QCheckBox
            widget.attrib["class"] = "QCheckBox"
            new_name = "cb" + name[2:]
            widget.attrib["name"] = new_name
            print(f"🔁 {name} → {new_name}, QRadioButton → QCheckBox")
            count += 1

    if count == 0:
        print("ℹ️ No radio buttons matched the pattern.")
    else:
        tree.write(out_filename, encoding="utf-8", xml_declaration=True)
        print(f"\n✅ Patched {count} widgets. Saved to: {out_filename}")

if __name__ == "__main__":
    print
    patch_ui_file()
