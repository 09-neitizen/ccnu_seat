import json

# 指定要打开的JSON文件的文件路径
file_path = "./seat.json"  # 替换为实际的文件路径

# 读取seat.json
with open(file_path, "r",encoding="utf-8") as input_file:
    data = json.load(input_file)

# 提取devName和devId并存储在字典中
output_data = {}
for item in data["data"]:
    dev_name = item["devName"]
    dev_id = item["devId"]
    output_data[dev_name] = dev_id

# 将结果存储为JSON文件
with open("output.json", "w") as output_file:
    json.dump(output_data, output_file, indent=4)

print("已提取并存储devName和devId到output.json文件。")
