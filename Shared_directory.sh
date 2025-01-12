#!/bin/bash

#Variables
DEV_GROUP_NAME="developers"


# Check if the developers group exists, if not create it
if ! getent group $DEV_GROUP_NAME > /dev/null; then
    sudo groupadd $DEV_GROUP_NAME
    echo "Successfully created group for developers"
fi


# Check if at least one path is provided
if [ "$#" -lt 1 ]; then
    echo "Please pass atleast 1 argument to run this script"
    exit 1
fi


# Function to create shared directoriy with nested permissions for sub folders and files
shared_directory() {
    local dir_path=$1
    cd /opt/
    
    # Create the directory if it doesn't exist
    if [ ! -d "$dir_path" ]; then
        sudo mkdir -p "$dir_path"
        echo "Directory created: $dir_path"
    fi
    
    # Changing group ownership to developers
    echo "changing group ownership"
    sudo chgrp -R $DEV_GROUP_NAME "$dir_path"
    
    # Setting permissions to allow read/write by group members
    echo "Setting permissions"
    sudo chmod -R 2775 "$dir_path"
    
    # setting newly created files and directories inherit the group ownership
    echo "Setting default group ownership for new files"
    sudo chmod g+s "$dir_path"
}




# Iterate over shared paths
for arg in "$@"; do
    shared_directory "$arg"
done



#####Assumptions#####
#1. All Developers are added to group "developers" after the creation.
#2. Shared_directory.sh Script has execute permissions
#3. Relative path shared directories are created under /opt
#4. Script can be tested with following command.
#$ ./Shared_directory.sh /home/sanjay/shared1  shared2




