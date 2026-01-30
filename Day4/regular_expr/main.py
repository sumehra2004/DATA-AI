# import re
# text="python is powerful "
# res=re.match("python",text)
# if res:
#     print("Match found:",res.group())

# import re   
# text = "python is powerful"
# res = re.search("powerful", text)
# if res:
#     print("Search found:", res.group())

import re
# text="my number is 1234567890 and 8908767656"
# num=re.findall("\d{10}",text)
# print(num)

# for match in re.finditer("\d{10}",text):
    # print("Match found:",match.group(),"at position",match.start(),"-",match.end())

text="my phone number is 1234567890"
masked=re.sub("\d{6}","******",text)
print(masked)