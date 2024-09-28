from datasets import load_dataset
import pandas as pd

dataset = load_dataset('amazon_us_reviews', name='Apparel_v1_00')

print(dataset.keys())
