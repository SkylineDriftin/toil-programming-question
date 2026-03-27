import json, distribution_network

def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


data = load_json(r'C:\Users\David\Content\code\genomics_lab_coding_question\tests\simple_input.json')
#print(data)

network = distribution_network.DistributionNetwork.from_json(data)
print("facilities")
for facility in network.facilities.values():
    print(facility)
print('max consumption: ')
print(network.max_consumption())