# from multiprocessing import Pool
# import time

# def simulate_region(region):
#     print(f"Calculating weather for {region}...")
#     time.sleep(1)
#     result = f"region {region} complete"
#     return result

# if __name__ == "__main__":
#     regions = ['North', 'South', 'East', 'West']

#     with Pool(processes=4) as p:
#         result=p.map(simulate_region, regions)

#     print("Results:", result )


from multiprocessing import Pool
import time
def analyze_log(chunk):
    print(f"Analyzing log chunk {chunk}...")
    time.sleep(1)
    result = f"log chunk {chunk} analyzed"
    return result
if __name__ == "__main__":
    log_chunks = [1, 2, 3, 4]

    with Pool(4) as p:
        result = p.map(analyze_log, log_chunks)

    print("Analysis Results:", result)
