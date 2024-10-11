import json

from create_batch import CategorizedItem
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_api = OpenAI()

def check_batch_status_and_retrieve_output_file_id() -> str | None:

    with open('uploaded-batch.json', 'r') as uploaded_batch:
        uploaded_batch_information = json.load(uploaded_batch)
        batch = openai_api.batches.retrieve(uploaded_batch_information['id'])

        if batch.status == 'completed':
            return batch.output_file_id
        else:
            print('The batch is still being processed, it might take up to 24 hours. Check back later.')
            return None

def convert_to_categorized_item(transaction: str) -> CategorizedItem:
    content = json.loads(transaction)['response']['body']['choices'][0]['message']['content']
    return CategorizedItem(**json.loads(content))

output_file_id = check_batch_status_and_retrieve_output_file_id()

if output_file_id:
    processed_batch = openai_api.files.content(output_file_id)
    for transaction in processed_batch.text.split('\n'):
        if transaction != '':
            print(convert_to_categorized_item(transaction))
