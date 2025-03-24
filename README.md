
#These two files are Fiji Scripts in Python language (Jython) intended to facilitate the processing of big amounts of image data in .tif, .tiff or .czs format, 
#generated using imaging microscopy techniques, in particular Confocal microscopy with X,Y,Y and two C planes. 

#"import_merge_stacks_divide2channels_export_single_pgn_affinity.py": Helps by importing a selected file,
#automatically dividing the channels used, creating a maximal intensity projection of each of the Z-stacks for every time point,
#duplicating every time point into a new .png file, modifying their display options to Automatic Brightness and contrast, creating a folder for each channel,
#creating a folder to place the channel folders and saving each .png file independently into it's corresponding folder. 
#This Script is therefore intended to process images to be displayed only. Since the display modifications are saved into the new .png files.

#"import_merge_stacks_divide2channels_export_single_tif.py": Helps by importing a selected file, automatically dividing the channels used,
#creating a maximal intensity projection of each of the Z-stacks for every time point, duplicating every time point into a new .tif file,
#creating a folder for each Chanel to save the files independently and create a new folder to save the Chanel folders. 
#This Script is therefore intended to rapidly process images that can provide valuable statistical information.
#Fine tuning for particular purposes might be required.


# Created by prompting specifical requirements with the help of ai.
