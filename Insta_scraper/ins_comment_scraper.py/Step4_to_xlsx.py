import json

import pandas

for count in [10,11,12,13]:
    with open(f"temp{count}.txt", 'r', encoding='utf-8') as f:
        lines = [json.loads(i.strip()) for i in f.readlines()]
        df = pandas.DataFrame(lines)
        df.drop_duplicates(['post_id', 'Comment ID'], inplace=True)
        df.to_csv(f"comments{count}.csv")
