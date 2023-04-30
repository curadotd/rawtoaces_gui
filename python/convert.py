"""
@package rawtoaces_gui.convert
@brief This module contains the functions to convert the images, rename and stor in a exr subfolder.

@author Marco Curado
@email mjbacurado@gmail.com
"""

import multiprocessing
import os
import sys
import subprocess
import shutil
import time


convert_key = sys.argv[0]

commands = ["rawtoaces"]

#Here we get the arguments from the command line
for args in sys.argv:
    commands.append(args)

#Here we extract the new name of the image
if "--change-output-image-name" in commands:
    get_new_name = commands.pop()

def flush_then_wait():
    """function to flush the stdout and stderr and wait 0.5 seconds
    """
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(0.1)

def changeImageName(commands):
    """function to change the name of the image
    We also add a number padding .####. to the end of the name to avoid overwriting the images.
    """
    #Here we create a count variable to add to the end of the name
    count = 1001
    
    #Here we check if the user wants to convert a sequence of images
    if "--sequence" in commands:
        sequence = True
    #Here we remove the arguments that we don't need, and get the path of the image.

    commands = [x for x in commands if "--sequence" not in x and "--create-exr-subfolder" not in x and "--change-output-image-name" not in x and convert_key not in x]
    full_path = commands.pop()
    path = os.path.dirname(full_path)

    #Here we get all the images in the folder and sort them
    images = [f for f in os.listdir(path) if '.exr' in f and not f.startswith('.')]
    images.sort()

    #Here we rename the images
    for image in images:
        new_name = "{0}.".format(get_new_name) + str(count) + ".exr"
        count += 1
        sys.stdout.write("start_moving: {0} to {1}\n".format(os.path.join(path, image), os.path.join(path, new_name)))
        os.rename(os.path.join(path, image), os.path.join(path, new_name))
        sys.stdout.write("end_moving: Finished\n")
        sys.stderr.write("Total complete: 90%\n")
        flush_then_wait()

def convertComand(commands, sequence=False, percent=False):
    """function to convert the images
    """

    #Here we create a percet variable to show the progress of the conversion
    if percent == False:
        percent = 80

    #Here we remove the arguments that we don't need
    commands = [x for x in commands if "--sequence" not in x and "--create-exr-subfolder" not in x and "--change-output-image-name" not in x and convert_key not in x]

    #Here we add the path of the images if we wish to convert a sequence
    if sequence:
        commands.append(sequence)
    
    #Here set process to run the subprocess, and we capture the output
    process = subprocess.run( commands, capture_output=True )

    #Here we print the output of the subprocess, to use in the GUI
    sys.stdout.write( "exit status: {0}\n".format(process.returncode))
    sys.stdout.write( "stdout: {0}\n".format(process.stdout.decode()))
    sys.stderr.write("Total complete: {0}%\n".format(int(percent)))

def createSubFolder(commands):
    """function to create a exr subfolder
    """
    #Here we remove the arguments that we don't need
    commands = [x for x in commands if "--sequence" not in x and "--create-exr-subfolder" not in x and "--change-output-image-name" not in x and convert_key not in x]
    
    #Here we get the path of the images
    directory = os.path.dirname(commands.pop())
    exr_path = os.path.join(directory, "exr")

    #Here we check and or create the exr subfolder
    if not os.path.exists(exr_path):
        os.makedirs(exr_path)
    
    #Here we get all the images in the folder and sort them
    images = [f for f in os.listdir(directory) if '.exr' in f.lower()]
    images.sort()

    #Here we move the images to the exr subfolder
    for image in images:
        sys.stdout.write("star_moving: {0} to {1}\n".format(image, exr_path))
        shutil.move(os.path.join(directory, image), exr_path)
        sys.stdout.write("end_moving: Finished\n")
        sys.stderr.write("Total complete: 100%\n")
        flush_then_wait()

def sequenceComand(commands):
    """function to convert a sequence of images
    """
    #Here we remove the arguments that we don't need
    commands = [x for x in commands if "--sequence" not in x and "--create-exr-subfolder" not in x and "--change-output-image-name" not in x and convert_key not in x]
    
    #Here we get the path of the images
    input_file = commands.pop()
    directory = os.path.dirname(input_file)
    all_files = os.listdir(directory)
    #Here we get all the images in the folder and sort them
    all_files = [f for f in all_files if not f.startswith('.')]
    all_files.sort()

    #Here we create a count variable to show the progress of the conversion
    count = 0

    #Here we parse the images to the convertComand function.
    for file in all_files:
        count += 80 / len(all_files)
        converte_files = os.path.join(directory, file)
        convertComand(commands, sequence=converte_files, percent=count)

#Here we check if the user wants to convert a single image and convert it
if "--sequence" not in commands:
    convertComand(commands)

#Here we check if the user wants to convert a sequence of images and convert it
if "--sequence" in commands:
    sequenceComand(commands)

#Here we check if the user wants to change the name of the image and change it
if "--change-output-image-name" in commands and not "--sequence" in commands:
    commands = [x for x in commands if "--change-output-image-name" not in x]
    changeImageName(commands)

#Here we check if the user wants to change the name of the sequence and change it
if "--change-output-image-name" in commands and "--sequence" in commands:
    commands = [x for x in commands if "--change-output-image-name" not in x]
    changeImageName(commands)

#Here we check if the user wants to create a exr subfolder and create it
if "--create-exr-subfolder" in commands and not "--sequence" in commands:
    commands = [x for x in commands if "--create-exr-subfolder" not in x]
    createSubFolder(commands)

#Here we check if the user wants to create a exr subfolder for the sequence and create it
if "--create-exr-subfolder" in commands and "--sequence" in commands:
    commands = [x for x in commands if "--sequence" not in x and "--create-exr-subfolder" not in x]
    createSubFolder(commands)
