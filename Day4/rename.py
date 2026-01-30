import os

folder = "temp"

for i, file in enumerate(os.listdir(folder), start=1):
    os.rename(
        os.path.join(folder, file),
        os.path.join(folder, f"file_{i}.txt")
    )

print("Files renamed")
