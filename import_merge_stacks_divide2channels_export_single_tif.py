from ij import IJ
from ij.plugin import ZProjector, ChannelSplitter, Duplicator
from ij.io import OpenDialog
from ij.gui import GenericDialog
import os

desktop_path = "/Users/grosshans-lab/Desktop"

# Step 1: Select the image file
opener = OpenDialog("Select your image (.tif or .czi)")
file_path = opener.getPath()
if file_path is None:
    IJ.error("No file selected.")
    exit()

# Step 2: Open the image explicitly
if file_path.lower().endswith(".czi"):
    IJ.run("Bio-Formats Importer", "open=[" + file_path + "] autoscale color_mode=Default view=Hyperstack stack_order=XYCZT")
    imp = IJ.getImage()
else:
    imp = IJ.openImage(file_path)
    if imp is None:
        IJ.error("Could not open image.")
        exit()
    imp.show()

# Confirm dimensions explicitly
n_channels, n_slices, n_frames = imp.getNChannels(), imp.getNSlices(), imp.getNFrames()
IJ.log("Image dimensions (C,Z,T): (%d,%d,%d)" % (n_channels, n_slices, n_frames))

# Step 3: Create output folders explicitly
gd = GenericDialog("Output Folder")
gd.addStringField("New folder name (Desktop):", "Processed_Images")
gd.showDialog()
if gd.wasCanceled():
    IJ.error("Cancelled by user.")
    exit()

folder_name = gd.getNextString()
output_dir = os.path.join(desktop_path, folder_name)
channel_names = ['mkate', 'gfp']

# Create directories explicitly
for ch_name in channel_names:
    ch_path = os.path.join(output_dir, ch_name)
    if not os.path.exists(ch_path):
        os.makedirs(ch_path)

# Step 4: Process each channel explicitly and independently
duplicator = Duplicator()

for idx, ch_name in enumerate(channel_names, start=1):
    IJ.log("Processing channel: " + ch_name)
    
    # Extract single channel stack explicitly
    single_ch_stack = duplicator.run(imp, idx, idx, 1, n_slices, 1, n_frames)
    
    # Process each frame explicitly
    for t in range(1, n_frames + 1):
        # Extract the current timepoint substack explicitly
        frame_stack = duplicator.run(single_ch_stack, 1, 1, 1, n_slices, t, t)
        
        # Explicitly perform Z-Projection
        zp = ZProjector(frame_stack)
        zp.setMethod(ZProjector.MAX_METHOD)
        zp.doProjection()
        mip_imp = zp.getProjection()
        
        # Explicitly save the projected image
        filename = "wt3_%s_t%d.tif" % (ch_name, t - 1)
        save_path = os.path.join(output_dir, ch_name, filename)
        IJ.saveAsTiff(mip_imp, save_path)
        IJ.log("Explicitly saved: " + save_path)

IJ.showMessage("✅ Finished!", "Both channels processed and saved explicitly!")


