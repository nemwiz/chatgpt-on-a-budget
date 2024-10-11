import csv
import json

import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


CATEGORIES_PROMPT = '''
You are an expert assistant that specializes in categorizing items based on their description.
You will be provided with an item description and your job is to assign it to one of the predefined categories.

The category name is listed between ** ** and below the name you will find a few example items that you should use for categorization.

Here are the categories:

**Groceries**
- Albert Heijn
- Lidl
- Supermarkt
- Markt
- Jumbo

**Shopping**
- Zara
- Primark

**Eating out**
- McDonalds
- Kebab

Answer in JSON in the specified format.
---------

Categorize the following item
'''

class CategorizedItem(BaseModel):
    item: str
    category: str


def extract_items() -> list[str]:
    with open('dummy-transactions.csv') as csv_file:
        items = csv.DictReader(csv_file)
        return [ item['Name / Description'] for item in items]


def create_batch_transactions(items: list[str]) -> list[str]:

    transactions = []

    for index, item in enumerate(items, start=1):
        batch_transaction = {
            'custom_id': f'category-{index}',
            'method': 'POST',
            'url': '/v1/chat/completions',
            'body': {
                'model': os.environ.get('CHAT_COMPLETION_MODEL'),
                'messages': [
                    {'role': 'system', 'content': CATEGORIES_PROMPT},
                    {'role': 'user', 'content': item}
                ],
                'response_format': {
                    'type': 'json_schema',
                    'json_schema': {
                        'description': 'Categorized item JSON schema',
                        'name': 'CategorizedItem',
                        'schema': CategorizedItem.model_json_schema()
                    }
                }
            }
        }

        transactions.append(json.dumps(batch_transaction))

    return transactions



items = extract_items()
batch_transactions = create_batch_transactions(items)

with open('my-batch.jsonl', 'w') as batch_file:
    for transaction in batch_transactions:
        batch_file.write(transaction)
        batch_file.write('\n')
