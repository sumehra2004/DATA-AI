import csv

ip_address = []

with open("sample_logs.log", "r") as log:
    lines = log.readlines()

    for line in lines:
        if "reverse mapping" in line:
            words = line.split('[')
            ip_addr = words[2].split(']')
            ip_address.append(ip_addr[0])

with open("ip_addresses.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["IP_Address"]) 

    for ip in ip_address:
        writer.writerow([ip])

print("IP addresses extracted and saved to CSV successfully.")