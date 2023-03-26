import csv
from datetime import date, datetime
from typing import Any, Dict, List, Union


class CSVLoader:
    def __init__(
        self,
        file_path: str,
        column_types: Dict[str, Any] = None,
        skip_broken: bool = True,
    ):
        self.file_path = file_path
        self.column_types = column_types
        self.skip_broken = skip_broken

    def _convert_value(
        self, value: str, target_type: Any
    ) -> Union[str, int, float, bool]:
        if isinstance(target_type, tuple):
            if tuple[0] == date and isinstance(tuple[1], str):
                return datetime.strptime(value, tuple[1]).date()

        elif target_type == int:
            try:
                return int(value)
            except ValueError:
                return int(float(value))
        elif target_type == float:
            return float(value)
        elif target_type == bool:
            return value.lower() in ["true", "1", "yes", "y", "verified"]
        else:
            return value

    def load(self) -> List[Dict[str, Any]]:
        data = []

        with open(self.file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not self.column_types:
                    data.append(row)
                else:
                    try:
                        converted_row = {
                            key: self._convert_value(
                                value, self.column_types.get(key, str)
                            )
                            for key, value in row.items()
                        }
                        data.append(converted_row)
                    except ValueError as e:
                        if self.skip_broken:
                            continue
                        else:
                            raise e

        return data
