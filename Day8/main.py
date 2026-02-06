# import threading
# import time
# def say_hello():
#     print("hello world")

# t=threading.Thread(target=say_hello)
# t.start()

# print("Main Thread")
# import time
# def task():
#     print("Task started")
#     time.sleep(2)  # Simulate a task taking some time
#     print("Task completed")
# task()
# print("Main program continues...")
# why we need a threading
# one task is waiting(like downloading,sleeping,input/output) and for program to stay responsive
# ex: downloading a file,showing progress,accepting user input

# import threading
# def greet(name):
#     print(f"Hello, {name}!")
# t = threading.Thread(target=greet, args=("Alice",))
# t.start()

# Without threading
# import time

# def greet(name):
#     time.sleep(2)   
#     print(f"Hello, {name}!")

# greet("Alice")

# import threading
# import time


# def worker(num):
#     print(f"Worker{num} is running ")
#     time.sleep(1)
#     print(f"Worker{num} has finished")
# for i in range(5):
#     t=threading.Thread(target=worker,args=(i,))
#     t.start()
# import threading
# import urllib.request
# def download_file():
#     # url='http://localhost:8000/jk.txt'
#     url='https://files.eric.ed.gov/fulltext/EJ1172284.pdf'
#     filename='downloaded_test.pdf'
#     print("start download of file")
#     # time.sleep(2)
#     urllib.request.urlretrieve(url,'filename')
#     print("Download completed")

# t=threading.Thread(target=download_file)
# t.start()
# print("Main thread continues execution")

# with threading
# import urllib.request
# import threading
# import time
# import json
# import ssl

# def download_json():
#     try:
#         print("Connecting to API...")
#         time.sleep(2)

#         url = "https://fakestoreapi.com/products"
#         headers = {
#             "User-Agent": "Mozilla/5.0"
#         }

#         req = urllib.request.Request(url, headers=headers)
#         context = ssl._create_unverified_context()

#         with urllib.request.urlopen(req, context=context) as response:
#             data = response.read()

#         print("Data downloaded")

#         posts = json.loads(data)

#         with open("posts.json", "w") as f:
#             json.dump(posts, f, indent=4)

#         print("Download complete")

#     except Exception as e:
#         print("Error:", e)

# # Create and start thread
# t = threading.Thread(target=download_json)
# t.start()

# print("Main thread continues execution")

# # Optional: wait for thread to finish
# t.join()
# print("Program finished")

