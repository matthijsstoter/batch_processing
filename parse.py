import pathlib
from dataclasses import dataclass, field

import pandas as pd


@dataclass
class JointAngleFile:
    file_path: pathlib.Path
    data: pd.DataFrame = field(init=False)

    def __post_init__(self) -> None:
        self.data = self._read_file()
        self._process_data()
    
    def _read_file(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, sep="\t", header=0, index_col=0, skiprows=1)

    def _process_data(self) -> None:
        df = self.data.copy()

        # Handling index and lines to skip
        df = df[df.index.notnull()]
        df.drop("ITEM", inplace=True)
        df.index.astype(int, copy=False)
        df.index.name = "Item"

        # Converting all columns to float, rather than str
        df = df.astype(float)

        self.data = df
    
    def export_to_csv(self, filepath: pathlib.Path) -> None:
        self.data.to_csv(filepath, sep='\t', mode='a')
    
    def export_to_excel(self, filepath: pathlib.Path) -> None:
        df = self.data.copy().reset_index(inplace=False)
    
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(filepath)  #, engine='xlsxwriter')

        # Sheet name to use for writing
        sheet_name = "Data"

        # Convert the dataframe to an XlsxWriter Excel object. Turn off the default
        # header and index and skip one row to allow us to insert a user defined
        # header.
        df.to_excel(writer, sheet_name=sheet_name, startrow=1, header=False, index=False)

        # Get the xlsxwriter workbook and worksheet objects.
        worksheet = writer.sheets[sheet_name]

        # Get the dimensions of the dataframe.
        (max_row, max_col) = df.shape

        # Create a list of column headers, to use in add_table().
        column_settings = []
        for header in df.columns:
            column_settings.append({"header": header})

        # Add the table.
        worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings, "name": "JointAngles"})

        # Make the columns wider for clarity.
        worksheet.set_column(0, max_col - 1, 12)

        # Close the Pandas Excel writer and output the Excel file.
        writer.close()

    def export_to_txt(self, filepath: pathlib.Path) -> None:
        with open(filepath, mode="w") as f:
            string = self.data.to_string()
            f.write(string)
