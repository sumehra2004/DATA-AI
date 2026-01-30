# # TUPLE
# trip_summary=("uber","pondicherry","Chennai",3456.90,"completed")
# # # print(trip_summary)
# # # print(trip_summary[2])

# # for i in trip_summary:
# #     print(i)
# # print(len(trip_summary))

# print(trip_summary[-2])


# -----------------------------------------------------------------
# Dictionary
# mydic={"key1":"Value1","key2":"Value2","key3":"Value3"}
# print(mydic)

# trip_summary={"cab":"uber","City":"pondicherry","fare":3456.90}
# print(trip_summary.keys())
# print(trip_summary.values())
# print(trip_summary.get("cab"))
# print(trip_summary["City"])
# for key,values in trip_summary.items():
#     print(f"Key:{key},Value:{values}")

# trip_summary.update({"status":"completed"})
# print(trip_summary)
# trip_summary.pop("status")
# print(trip_summary)
# for i in trip_summary:
#     print(i, "->",trip_summary[i])

# -----------------------------------------------------------------
# SET
# myset={1,2,3,4,5,6}
# print(myset)

# uber={"Hyd","Mumbai","Bangalore","pondicherry","pune","delhi"}
# uber.add("gurgaon")
# print(uber)
# list_uber=list(uber)
# print(list_uber)

uber1={"Hyd","Mumbai","Bangalore","pune","delhi"}
uber2={"Calcutta","Hyd","delhi"}
print(uber1.union(uber2))
print(uber1.intersection(uber2))
print(uber1.difference(uber2))

uber1.add("gurugram")
print(uber1)
uber1.remove("gurugram")
print(uber1)