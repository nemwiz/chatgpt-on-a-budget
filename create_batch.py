import csv
import json
import uuid

with open('dummy-transactions.csv') as csv_file:

    categories = csv.DictReader(csv_file)

    for index, category in enumerate(categories, start=1):

        print(category['Name / Description'])

        batch_transaction = {"method": "POST",
                          "url": "/v1/chat/completions",
                          "body":
                            {"model": "gpt-3.5-turbo-0125",
                             "messages": []
                         }}


        print(json.dumps(batch_transaction))





