#!/bin/bash

set -e

echo "📥 Installing jpp..."

INSTALL_PATH="/usr/local/bin/jpp"

curl -fsSL https://raw.githubusercontent.com/fabfawufawd/jpp/main/jpp.py -o /tmp/jpp

chmod +x /tmp/jpp
sudo mv /tmp/jpp "$INSTALL_PATH"

echo
echo "✅ Installation complete!"
echo "You can now use jpp in your terminal:"
echo
echo "    cat data.json | jpp"