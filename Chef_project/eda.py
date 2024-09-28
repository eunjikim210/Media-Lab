import pandas as pd

# file_path = 'postdat_10percent.csv'
# # data = pd.read_csv(file_path)

# # print(data.head())

# import pandas as pd

# data = pd.read_csv(file_path)

# output_file = 'postdat_10percent.xlsx'
# writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

# workbook = writer.book

# # Set strings_to_urls=False to prevent URLs from automatically converting to hyperlinks
# workbook.strings_to_urls = False

# data.to_excel(writer, index=False)

# writer.close()
# print(f"The file has been successfully saved as {output_file}")

# file_path = 'postdat_10percent.xlsx'
# data_first_40_rows = pd.read_excel(file_path, nrows=40)

# output_file = 'postdat_40rows.xlsx'
# writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

# workbook = writer.book
# workbook.strings_to_urls = False
# data_first_40_rows.to_excel(writer, index=False)
# writer.close()

# print(f"The first 40 rows have been successfully saved as {output_file}")

file_path = 'postdat_10percent.csv'
data_first_40_rows = pd.read_csv(file_path, nrows=40)

output_file = 'postdat_5rows_astest.csv'

data_first_40_rows.to_csv(output_file, index=False)
print(f"The first 40 rows have been successfully saved as {output_file}")
