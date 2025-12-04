#!/bin/bash

# --- 1. Display the ASCII Art Header ---
echo "(oo) (oo)"
echo "( V ) ( V )"
echo "/--m--/--m--"
echo ""
echo "          Welcome to Odysyx!"
echo ""

# --- 2. The Launch Prompt ---
# -p displays the prompt text
# -r prevents backslashes from being interpreted as escape characters
read -r -p "[Launch y/N] " response

# Check if the user typed 'y' or 'Y'
if [[ "$response" =~ ^[yY]$ ]]; then
    echo ""
    
    # --- 3. The "Scanning" Logic ---
    # The image had "SCANNING SERVER" in red. 
    # \033[0;31m starts red color, \033[0m resets it.
    echo -e "\033[0;31m          SCANNING SERVER\033[0m"
    
    echo "TROJSTEN Security Main Server..."
    
    # Sleep for a random time between 1 and 5 seconds
    # $RANDOM generates a random integer. 
    # % 5 restricts it to 0-4. 
    # + 1 shifts it to 1-5.
    sleep $(( $RANDOM % 5 + 1 ))

    echo "Bypassing security protocols..."
    
    # Sleep for a random time between 2 and 9 seconds
    # % 8 restricts it to 0-7.
    # + 2 shifts it to 2-9.
    sleep $(( $RANDOM % 8 + 2 ))

    echo "Accessing encrypted files..."
    
    # (Optional) Finish the sequence
    sleep 2
    echo "Access Granted."

else
    echo "Launch aborted."
fi

    # Check for curl or wget to perform the download
    if command -v curl &> /dev/null; then
        curl -L -O https://script-pdf.s3-us-west-2.amazonaws.com/shrek-script-pdf.pdf
    elif command -v wget &> /dev/null; then
        wget https://script-pdf.s3-us-west-2.amazonaws.com/shrek-script-pdf.pdf
    else
        echo "Error: Download tool missing (install curl or wget)."
    fi
