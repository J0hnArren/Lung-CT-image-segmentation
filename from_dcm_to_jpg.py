import os
import glob
import pydicom
from PIL import Image
import pandas as pd

# Set paths for input and output folders
input_folders = ['ABDULAZIZOVA-ROMANA-ROMANOVNA', 'KHALDEEVA-OL`GA-ALEKSANDROVNA', 'KORYAKIN-YURIY-ALEKSEEVICH', 'PLUTALOVA-LARISA-ALEKSEEVNA', 'ROGACHEV-VITALIY-EGOROVICH', 'TRUSHIN-ALEKSEY-ANATOL`EVICH', 'ZROYCHIKOVA-ZOYA-VYACHESLAVOVNA']

output_folder = "C:\\Users\\Rauf\\Desktop\\2_dataset\\"

# Create empty dataframe to store processed image filenames and paths
df = pd.DataFrame(columns=["filename", "filepath"])

for input_folder in input_folders:

    newpath = output_folder+input_folder
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # Get list of DICOM files in input folder
    dcm_files = glob.glob(os.path.join(input_folder, "*.dcm"))

    # Loop through DICOM files and convert to JPEG
    for dcm_file in dcm_files:
        try:
            # Read DICOM file
            ds = pydicom.dcmread(dcm_file)

            pixel_array = ds.pixel_array.astype('int16')  # Convert 3D array to 2D array
            image = Image.fromarray(pixel_array)

            # Convert image mode to RGB
            image = image.convert("RGB")

            # Save image as JPEG in output folder
            output_filename = os.path.basename(dcm_file).replace(".dcm", ".jpg")
            output_path = os.path.join(output_folder+input_folder, output_filename)
            image.save(output_path)

            # Add filename and filepath to dataframe
            new_row = {"filepath": output_path, "filename": output_filename}
            df = pd.concat([df, pd.DataFrame(new_row, index=[0])], ignore_index=True)

        except Exception as e:
            # Skip broken images and log filename to file
            with open(output_folder+"skipped_images.txt", "a") as f:
                f.write(f"{dcm_file}\n")
            continue

# Save dataframe to CSV file
df.to_csv(output_folder+"processed_images.csv", index=False)
