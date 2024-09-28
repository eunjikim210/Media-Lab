import pandas as pd

file_paths = [
    'source 2017.csv',
    'source 2018.csv',
    'source 2019.csv',
    'source 2020.csv',
    'source 2021.csv',
    'source 2022.csv'
]

sets = [set(pd.read_csv(path).iloc[:, 0]) for path in file_paths]

all_files = set.intersection(*sets)
five_files = (set.union(*[set.intersection(*[s for j, s in enumerate(sets) if j != i]) for i in range(6)]) - all_files)
four_files = (set.union(*[set.intersection(*[s for j, s in enumerate(sets) if j not in [i, k]]) for i in range(6) for k in range(i+1, 6)]) - all_files - five_files)
three_files = (set.union(*[set.intersection(*[s for j, s in enumerate(sets) if j not in [i, k, l]]) for i in range(6) for k in range(i+1, 6) for l in range(k+1, 6)]) - all_files - five_files - four_files)
two_files = (set.union(*[set.intersection(*[s for j, s in enumerate(sets) if j not in [i, k, l, m]]) for i in range(6) for k in range(i+1, 6) for l in range(k+1, 6) for m in range(l+1, 6)]) - all_files - five_files - four_files - three_files)
one_file = (set.union(*sets) - all_files - five_files - four_files - three_files - two_files)

with pd.ExcelWriter('distinct list.xlsx') as writer:
    pd.DataFrame(list(all_files), columns=['Element']).to_excel(writer, sheet_name='All Files', index=False)
    pd.DataFrame(list(five_files), columns=['Element']).to_excel(writer, sheet_name='Five Files', index=False)
    pd.DataFrame(list(four_files), columns=['Element']).to_excel(writer, sheet_name='Four Files', index=False)
    pd.DataFrame(list(three_files), columns=['Element']).to_excel(writer, sheet_name='Three Files', index=False)
    pd.DataFrame(list(two_files), columns=['Element']).to_excel(writer, sheet_name='Two Files', index=False)
    pd.DataFrame(list(one_file), columns=['Element']).to_excel(writer, sheet_name='One File', index=False)