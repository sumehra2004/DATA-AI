import shutil
import datetime

source = "C:\\Users\\User\\OneDrive\\Desktop\\Capg\\python\\data.txt"
backup=f"C:\\Users\\User\\OneDrive\\Desktop\\Capg\\python\\data_backup_{datetime.date.today()}.txt"
shutil.copy(source,backup)

print(f"Backup of {source} created at {backup}")