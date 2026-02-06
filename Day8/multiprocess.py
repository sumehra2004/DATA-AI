# from multiprocessing import Process

# def worker_function():
#     print("Worker is running")

# if __name__ == "__main__":
#     p = Process(target=worker_function)
#     p.start()
#     p.join()

#     print("Main process is done")

# import time
# from multiprocessing import Pool
# def square(n):
#     return n * n
# if __name__ == "__main__":
#     numbers = [10**7,10**2,10**3,10**4,10**5]
#     start=time.time()
#     with Pool() as p:
#         result=p.map(square,numbers)
#     end=time.time()
#     print("Squares:",result)
#     print("Time taken with multiprocessing:",end-start)

import time
from multiprocessing import Pool, Process,Queue
def worker(q):
    q.put("hello")
if __name__ == "__main__":
    q=Queue()
    p=Process(target=worker,args=(q,))
    p.start()
    p.join()
    result=q.get()
    print("Message from worker:",result)
