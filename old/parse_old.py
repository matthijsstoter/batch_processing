import os
import pathlib
from dataclasses import dataclass, field

import pandas as pd


DIR = pathlib.Path(os.getcwd())
SOURCE_DATA_DIR = DIR / "Data/Source"
PROCESSED_DATA_DIR = DIR / "Data/Processed"

file = SOURCE_DATA_DIR / "Generic Markerless 2.c3d.txt"






# Reading txt file
df = pd.read_csv(file, sep="\t", header=0, index_col=0, skiprows=1)

# Handling index and lines to skip
df = df[df.index.notnull()]
df.drop("ITEM", inplace=True)
df.index.astype(int, copy=False)
df.index.name = "Item"

# Converting all columns to float, rather than str
df = df.astype(float)

# Exporting to txt file
txt_file = PROCESSED_DATA_DIR / "Data.txt"
with open(txt_file, mode="w") as f:
    string = df.to_string()
    f.write(string)

# Exporting to csv file
df.to_csv(PROCESSED_DATA_DIR / "Data.csv", sep='\t', mode='a')

# %% Exporting to Excel file
# Resetting index for processing
df.reset_index(inplace=True)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(PROCESSED_DATA_DIR / "Data.xlsx")  #, engine='xlsxwriter')

# Sheet name to use for writing
sheet_name = "Source"

# Convert the dataframe to an XlsxWriter Excel object. Turn off the default
# header and index and skip one row to allow us to insert a user defined
# header.

df.to_excel(writer, sheet_name=sheet_name, startrow=1, header=False, index=False)

# Get the xlsxwriter workbook and worksheet objects.
workbook = writer.book
worksheet = writer.sheets[sheet_name]

# Get the dimensions of the dataframe.
(max_row, max_col) = df.shape

# Create a list of column headers, to use in add_table().
column_settings = []
for header in df.columns:
    column_settings.append({'header': header})

# Add the table.
worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

# Make the columns wider for clarity.
worksheet.set_column(0, max_col - 1, 12)

# Close the Pandas Excel writer and output the Excel file.
# writer.save()
# writer.book.save()
writer.close()