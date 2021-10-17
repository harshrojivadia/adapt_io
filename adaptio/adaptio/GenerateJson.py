import pymongo
import json

def exportlink():
    conn = pymongo.MongoClient('mongodb://localhost:27017/')
    db = conn.adaptio

    cursor = db['LinkData'].find()

    data_list = list()
    for value in cursor:
        value.pop('_id')
        data_list.append(value)

    with open('company_index.json', 'w') as f:
        json.dump(data_list, f)

def export_data():
    conn = pymongo.MongoClient('mongodb://localhost:27017/')
    db = conn.adaptio

    cursor = db['DataTable'].find()

    data_list = list()
    for value in cursor:
        value.pop('_id')
        data_list.append(value)

    with open('company_profiles.json', 'w') as f:
        json.dump(data_list, f)


if __name__ == '__main__':
    exportlink()
    # export_data()

# company_profiles