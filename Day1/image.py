import os
import shutil

source_folder = r"C:\Users\User\OneDrive\Desktop\Capg\python\src_image"

backup_folder = os.path.join(os.path.dirname(source_folder), "backup_photos")

if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)
    print(f"Backup folder created: {backup_folder}")
else:
    print(f"Backup folder already exists: {backup_folder}")

image_extensions = ('.jpg')

for file_name in os.listdir(source_folder):
    if file_name.lower().endswith(image_extensions):
        source_file = os.path.join(source_folder, file_name)
        dest_file = os.path.join(backup_folder, file_name)
        shutil.copy(source_file, dest_file)
        print(f"Copied: {file_name}")

print("All photos have been backed up successfully!")
