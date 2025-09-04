#!/bin/bash

# Install Python and dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Create a simple static HTML file for the root URL
mkdir -p build
cat > build/index.html << 'EOL'
<!DOCTYPE html>
<html>
<head>
    <title>Cash Flow Forecaster</title>
    <meta http-equiv="refresh" content="0; url='/app'" />
</head>
<body>
    <p>Redirecting to the application...</p>
</body>
</html>
EOL

# Make the build script executable
chmod +x build.sh
