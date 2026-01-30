import shutil
import datetime

source = "data.txt"
backup = f"backup_{datetime.date.today()}.txt"

shutil.copy(source, backup)
print("Backup created")
