import os
import pandas as pd
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''

from google.cloud import storage

client = storage.Client()

bucket = client.get_bucket('nela_llm_data')

blobs = bucket.list_blobs()

for blob in blobs:
    print(blob.name)

url = "gs://nela_llm_data/nela-gt-2017.csv"
df = pd.read_csv(url)
print(df.head())