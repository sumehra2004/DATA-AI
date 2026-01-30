import shutil

total, used, free = shutil.disk_usage("/")

print("Total Storage:", total // (1024**3), "GB")
print("Used Storage :", used // (1024**3), "GB")
print("Free Storage :", free // (1024**3), "GB")