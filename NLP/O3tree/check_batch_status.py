from openai import OpenAI
client = OpenAI()

batch = client.batches.retrieve("batch_67ac87d414488190bc3b67568b344ac3")
print("\n\n\ncurrent batch info:", batch)
print("\n\n\n\ncurrent batch status:", batch.status)

batch_list = client.batches.list()
print("\n\n\n\n\ncurrent batches running:", batch_list)
