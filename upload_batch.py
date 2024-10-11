from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

openai_api = OpenAI()

batch_input_file = openai_api.files.create(
  file=open("my-batch.jsonl", "rb"),
  purpose="batch"
)

batch = openai_api.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)

with open('uploaded-batch.json', 'w') as batch_file:
    batch_file.write(batch.model_dump_json())
