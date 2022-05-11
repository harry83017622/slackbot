import json
import sys

import requests
from google.cloud import storage

from utils.logger_setting import log


def main():
    question_authors_map = crawl_notion_sorted()
    upload_gcloud_bucket(question_authors_map)
    with open("past_record.json", "w+") as fin:
        json.dump(question_authors_map, fin)
    print(len(question_authors_map))


def crawl_notion_sorted():
    with open("secret.json") as file:
        content = json.load(file)
        database_id = content["database_id"]
        secret_key = content["secret_key"]
        slack_token = content["slack_token"]
    question_authors_map = {}
    header = {"Authorization": secret_key, "Notion-Version": "2021-05-13"}
    query = {"sorts": [{"property": "題號", "direction": "ascending"}]}
    response = requests.post(
        "https://api.notion.com/v1/databases/" + database_id + "/query",
        headers=header,
        json=query,
    )

    push_results_to_map(response, question_authors_map)
    start_cursor = response.json()["next_cursor"]
    while start_cursor:
        query["start_cursor"] = start_cursor
        response = requests.post(
            "https://api.notion.com/v1/databases/" + database_id + "/query",
            headers=header,
            json=query,
        )
        push_results_to_map(response, question_authors_map)
        start_cursor = response.json()["next_cursor"]

    return question_authors_map


def push_results_to_map(response, mapper):
    
    for content in response.json()["results"]:
        article_prop = content["properties"]
        if "題號" not in article_prop:
            log.info(f"題號 not in {article_prop}")
            continue
        question_num = article_prop["題號"]["number"]
        authors_json = article_prop["Person"]["people"]
        if not article_prop["Person"]["people"]:
            log.info(f"people is empty in response for 題號 {question_num}")
            raise
        if question_num in mapper:
            log.info(f"duplicated artile with 題號 {question_num}")
            raise
        
        authors_list = []
        for author in authors_json:
            if "name" not in author:
                log.info(f"miss author name property {article_prop}")
                continue
            authors_list.append(author["name"])
        mapper[question_num] = authors_list

    return mapper


def upload_gcloud_bucket(data_results):
    bucket_name = "leetcode-notion-db"
    bucket = storage.Client().get_bucket(bucket_name)
    blob = bucket.blob("past_record.json")
    blob.upload_from_string(
        data=json.dumps(data_results, ensure_ascii=False),
        content_type="application/json",
    )
    return


if __name__ == "__main__":
    main()
