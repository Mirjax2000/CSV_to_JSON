"""CSV to JSON"""

from dataclasses import dataclass
from pathlib import Path
import sys
import json
from pandas import DataFrame, read_csv
from rich.console import Console


cons: Console = Console()


@dataclass
class Config:
    csv_folder: Path = Path("./CSVs").resolve()
    json_folder: Path = Path("./JSONs").resolve()
    codecs: tuple[str, ...] = (
        "utf-8",
        "utf-8-sig",
        "latin1",
        "cp1250",
        "cp1252",
    )


def input_file() -> str:
    file_name = input("Enter CSV file name (without .csv): ").strip()
    if not file_name.endswith(".csv"):
        file_name += ".csv"
    return file_name


class CsvToJson:
    """Csv to JSON main class"""

    def __init__(self, csv_file: str):
        self.config = Config()
        self.csv_file: str = csv_file
        self.csv_path: Path = self.config.csv_folder / self.csv_file
        self.dataset: DataFrame = self.get_dataset()
        self.columns: list[str] = self.get_dataset_columns(self.dataset)
        self.selected_columns: list[str] = []
        self.clean_dataset: DataFrame | None = None

    def get_dataset(self) -> DataFrame:
        """get whole dataset return raw Dataset"""
        config, csv_path, dataset, used_codec = self.config, self.csv_path, None, ""
        # --- solving csv encoding
        for codec in config.codecs:
            try:
                dataset = read_csv(
                    csv_path, encoding=codec, encoding_errors="strict", delimiter=";"
                )
                used_codec = codec
                break
            except UnicodeDecodeError:
                continue
        # ---
        if dataset is not None:
            cons.print(
                f"✅ Loaded successfully using encoding: {used_codec}", style="green"
            )
            cons.print(dataset.head())
        else:
            cons.print(
                "❌ Failed to load the CSV file with any known encoding.",
                style="red",
            )
            cons.print("Program ends.")
            sys.exit()
        # ---
        dataset.dropna(how="all", inplace=True)
        return dataset

    def get_dataset_columns(self, dataset) -> list[str]:
        """Get dataset columns: return list of columns name"""
        dataset.columns = [col.strip() for col in dataset.columns]
        columns: list[str] = list(dataset.columns)
        cons.print(f"seznam sloupcu: {columns}")
        return columns

    def get_selected_columns(self) -> None:
        selected_columns: list[str] = [
            col.strip()
            for col in input("Enter selected columns (or '__all__'): ").split(",")
        ]
        if selected_columns[0] == "__all__":
            self.selected_columns = self.columns
        else:
            self.selected_columns = selected_columns

    def filter_dataset(self) -> None:
        dataset, selected_columns = self.dataset, self.selected_columns
        missing_columns: list[str] = []
        # ---
        for col in selected_columns:
            if col not in self.columns:
                cons.print(f"⚠️ Column '{col}' not found in dataset.", style="yellow")
                missing_columns.append(col)
        # ---
        if not missing_columns:
            clean_dataset: DataFrame = DataFrame(dataset[selected_columns])
            self.dataset = clean_dataset
        else:
            cons.print(f"❌ Missing columns: {', '.join(missing_columns)}", style="red")
            cons.print("Program ends.", style="red")
            sys.exit()

    def convert_dataset_to_json(self) -> list[dict]:
        clean_dataset: DataFrame = DataFrame(self.dataset[self.selected_columns])
        return clean_dataset.to_dict(orient="records")

    def save_to_file(self, data: list[dict]) -> None:
        json_file: Path = self.config.json_folder / "result.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        cons.print(f"💾 Uloženo do {json_file}", style="cyan")

    def main(self) -> list[dict]:
        self.get_selected_columns()
        self.filter_dataset()
        result = self.convert_dataset_to_json()
        self.save_to_file(result)
        return result


if __name__ == "__main__":
    convert: CsvToJson = CsvToJson(input_file())
    result = convert.main()
