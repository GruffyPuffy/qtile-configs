#!/usr/bin/env bash

virtualenv -p python3 qtile-venv

source ./qtile-venv/bin/activate
pip3 install qtile
pip3 install dbus-next
pip3 install psutil

# Create session file
cat << EOF > qtile-venv.desktop
[Desktop Entry]
Name=Qtile(venv)
Comment=Qtile Session
Exec=/opt/venv/qtile-wrap start
Type=Application
Keywords=wm;tiling
EOF

sudo cp qtile-venv.desktop /usr/share/xsessions

# Create qtile-wrapper
cat << 'EOF' > qtile-wrap
#!/usr/bin/env bash
source /opt/venv/qtile-venv/bin/activate
qtile "$@"
EOF

sudo chmod +x qtile-wrap
