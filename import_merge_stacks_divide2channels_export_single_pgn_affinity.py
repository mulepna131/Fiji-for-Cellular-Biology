from ij import IJ
from ij.plugin import ZProjector, Duplicator, ContrastEnhancer, LutLoader
from ij.io import OpenDialog, DirectoryChooser
from ij.gui import GenericDialog
import os

desktop_path = "/Users/grosshans-lab/Desktop"

# Step 1: Select your file explicitly
opener = OpenDialog("Select your image (.tif or .czi)")
file_path = opener.getPath()
if file_path is None:
    IJ.error("No file selected.")
    exit()

# Step 2: Explicitly open image
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

# Step 3: Choose location explicitly for the output folder
dc = DirectoryChooser("Choose location for new folder")
chosen_dir = dc.getDirectory()
if chosen_dir is None:
    IJ.error("No directory selected.")
    exit()

# Step 4: Enter new folder name explicitly
gd = GenericDialog("Output Folder Name")
gd.addStringField("Enter new folder name:", "Processed_Images")
gd.showDialog()
if gd.wasCanceled():
    IJ.error("Cancelled by user.")
    exit()

folder_name = gd.getNextString()
output_dir = os.path.join(chosen_dir, folder_name)

channel_info = [
    {'name': 'mkate', 'lut': 'Red'},
    {'name': 'gfp', 'lut': 'Green'}
]

# Explicitly create directories
for ch in channel_info:
    ch_path = os.path.join(output_dir, ch['name'])
    if not os.path.exists(ch_path):
        os.makedirs(ch_path)

# Prepare explicitly duplicator and contrast enhancer
duplicator = Duplicator()
contrast_enhancer = ContrastEnhancer()

# Step 5: Process explicitly each channel independently
for idx, ch in enumerate(channel_info, start=1):
    IJ.log("Processing explicitly channel: " + ch['name'])

    # Explicitly extract single channel stack
    single_ch_stack = duplicator.run(imp, idx, idx, 1, n_slices, 1, n_frames)

    for t in range(1, n_frames + 1):
        frame_stack = duplicator.run(single_ch_stack, 1, 1, 1, n_slices, t, t)

        # Perform Z-projection explicitly
        zp = ZProjector(frame_stack)
        zp.setMethod(ZProjector.MAX_METHOD)
        zp.doProjection()
        mip_imp = zp.getProjection()

        # Explicitly adjust Auto-contrast
        contrast_enhancer.stretchHistogram(mip_imp, 0.35)

        # Explicitly apply LUT (Green for GFP, Red for mKate)
        IJ.run(mip_imp, ch['lut'], "")

        # Explicitly convert to RGB for display and save as PNG
        rgb_imp = mip_imp.flatten()

        # Save explicitly as PNG
        filename = "wt3_%s_t%d.png" % (ch['name'], t - 1)
        save_path = os.path.join(output_dir, ch['name'], filename)
        IJ.saveAs(rgb_imp, "PNG", save_path)
        IJ.log("Explicitly saved (LUT, PNG): " + save_path)

IJ.showMessage("✅ Visualization Ready!", "All images processed, LUT set, and saved explicitly as PNG!")
