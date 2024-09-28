from datasets import load_dataset
import pandas as pd


dataset = load_dataset('imdb', split='train')

dataframe = pd.DataFrame(dataset)

dataframe.to_csv('imdb_dataset_train.csv', index=False)