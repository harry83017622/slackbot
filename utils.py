from google.cloud import storage
import requests
import json

def upload_gcloud_bucket(data_results):
    bucket_name = 'leetcode-notion-db'
    bucket = storage.Client().get_bucket(bucket_name)

    # define a dummy dict
    # with open('notion_table.json', encoding='utf8') as jsonfile:
    #     data = json.load(jsonfile)
    # some_json_object = {'foo': list()}

    blob = bucket.blob('notion_table.json')
    # take the upload outside of the for-loop otherwise you keep overwriting the whole file
    # try:
    #     with open('notion_table.json', 'w', encoding='utf8') as jsonfile:
    #         json.dump({"object":"list","results":data_results}, jsonfile, indent=4, ensure_ascii=False)
    # except Exception as e:
    #     print(e)

    blob.upload_from_string(data=json.dumps({"object": "list", "results": data_results},
                            ensure_ascii=False), content_type='application/json')
    return

def get_gcloud_bucket():
    bucket_name = 'leetcode-notion-db'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob('notion_table.json')
    fileData = json.loads(blob.download_as_string())
    return fileData


def load_notion_db_from_gcp():
    # with open('notion_table.json', encoding='utf8') as jsonfile:
    #     data = json.load(jsonfile)
    data = get_gcloud_bucket()
    # print(data["results"][1])
    notion_table_set = {}
    for idx, i in enumerate(data["results"]):
        notion_table_set[i["題號"]] = idx
    return notion_table_set, data["results"]


# notion_table_set, table = load_nums()
# upload_gcloud_bucket(table)
# print(notion_table_set)
