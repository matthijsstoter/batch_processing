import pathlib

from parse import JointAngleFile


class FileProcessor():
    def __init__(self) -> None:
        pass

    def filter(self, filepaths: list[pathlib.Path]) -> list[pathlib.Path]:
        return [f for f in filepaths if ".DS" not in f.name ]

    def process(self, filepaths: list[pathlib.Path], target_path: pathlib.Path) -> None:

        for filepath in filepaths:
            jaf = JointAngleFile(file_path=filepath)
            export_name = f"{filepath.stem}.xlsx"
            export_path = target_path / export_name
            jaf.export_to_excel(export_path)
