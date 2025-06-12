#!/bin/bash

echo "=== STARTING FIX SCRIPT ==="


UI_FILE="Achse_Linux.ui"

if [[ ! -f "$UI_FILE" ]]; then
    echo "Error: File '$UI_FILE' not found."
    exit 1
fi

echo "Sanitizing $UI_FILE..."

# Orientation
sed -i 's|Qt::Orientation::Horizontal|Horizontal|g' "$UI_FILE"
sed -i 's|Qt::Orientation::Vertical|Vertical|g' "$UI_FILE"
sed -i 's|Qt.Orientation.Horizontal|Horizontal|g' "$UI_FILE"
sed -i 's|Qt.Orientation.Vertical|Vertical|g' "$UI_FILE"

# EchoMode
sed -i 's|QLineEdit::EchoMode::Normal|Normal|g' "$UI_FILE"
sed -i 's|QLineEdit::EchoMode::Password|Password|g' "$UI_FILE"
sed -i 's|QLineEdit::EchoMode::NoEcho|NoEcho|g' "$UI_FILE"
sed -i 's|QLineEdit::EchoMode::PasswordEchoOnEdit|PasswordEchoOnEdit|g' "$UI_FILE"
sed -i 's|QLineEdit.Normal|Normal|g' "$UI_FILE"

# Alignment (C++ to valid Qt .ui syntax)
sed -i 's|<enum>Qt::AlignmentFlag::AlignCenter</enum>|<set>AlignCenter</set>|g' "$UI_FILE"
sed -i 's|<enum>Qt::AlignmentFlag::AlignLeft</enum>|<set>AlignLeft</set>|g' "$UI_FILE"
sed -i 's|<enum>Qt::AlignmentFlag::AlignRight</enum>|<set>AlignRight</set>|g' "$UI_FILE"
sed -i 's|<enum>Qt::AlignmentFlag::AlignHCenter</enum>|<set>AlignHCenter</set>|g' "$UI_FILE"
sed -i 's|<enum>Qt::AlignmentFlag::AlignVCenter</enum>|<set>AlignVCenter</set>|g' "$UI_FILE"

# Replace <set> flag entries (Qt::AlignmentFlag::...) with clean values
sed -i 's|<set>Qt::AlignmentFlag::AlignCenter</set>|<set>AlignCenter</set>|g' "$UI_FILE"
sed -i 's|<set>Qt::AlignmentFlag::AlignLeft</set>|<set>AlignLeft</set>|g' "$UI_FILE"
sed -i 's|<set>Qt::AlignmentFlag::AlignRight</set>|<set>AlignRight</set>|g' "$UI_FILE"
sed -i 's|<set>Qt::AlignmentFlag::AlignHCenter</set>|<set>AlignHCenter</set>|g' "$UI_FILE"
sed -i 's|<set>Qt::AlignmentFlag::AlignVCenter</set>|<set>AlignVCenter</set>|g' "$UI_FILE"

sed -i 's|<enum>Qt::AlignmentFlag::AlignCenter</enum>|<set>AlignCenter</set>|g' "$UI_FILE"

# Strip C++ enum prefixes from alignment flags
sed -i 's|Qt::AlignmentFlag::||g' "$UI_FILE"



echo "✅ Enum cleanup done for $UI_FILE"
