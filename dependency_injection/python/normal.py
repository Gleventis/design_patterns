import json
from typing import Any, Protocol

type Data = list[dict[str, Any]]

class Loader(Protocol):
    """
    protocol class for loaders
    """
    def load(self) -> Data:
        """
        loads the data
        """

class Transformer(Protocol):
    """
    protocol class for transformers
    """
    def transform(self, data: Data) -> Data:
        """
        transforms the given data
        """

class Exporter(Protocol):
    """
    protocol class for exporters
    """
    def export(self, data: Data) -> None:
        """
        exports the given data
        """

class InMemoryLoader:
    """
    concrete implementation of the Loader protocol for loading in memory objects
    """
    def load(self) -> Data:
        """
        returns the loaded data

        Returns:
            Data: the loaded data
        """

        return [
            {"name": "subject1", "age": 31},
            {"name": "subject2", "age": None},
            {"name": "subject3", "age": 39},
            {"name": "subject4", "age": 40}
        ]

class CleanMissingFields:
    """
    concrete implementation of the Transformer protocol for cleaning data with missing fields
    """

    def transform(self, data: Data) -> Data:
        """
        transforms the given data by cleaning it and dropping fields that have None as value

        Args:
            data (Data): given data

        Returns:
            Data: cleaned data
        """
        return [item for item in data if item.get("age") is not None]

class JSONExpoerter:
    """
    concrete implementation of the Exporter protocol for exporting the data in json
    """
    def __init__(self, filename: str):
        """
        Constructor of the class

        Args:
            filename (str): the filename
        """
        self.filename = filename

    def export(self, data: Data) -> None:
        """
        exports the given data to json

        Args:
            data (Data): given data
        """
        with open(self.filename, "w") as file_handler:
            json.dump(data, file_handler)


class DataPipeline:
    """
    example data pipeline that we will inject our dependencies in
    """
    def __init__(self, loader: Loader, transformer: Transformer, exporter: Exporter):
        self.loader = loader
        self.transformer = transformer
        self.exporter = exporter

    def run(self) -> None:
        """
        runs the pipeline
        """
        data = self.loader.load()

        cleaned_data = self.transformer.transform(data=data)

        self.exporter.export(data=cleaned_data)


if __name__ == "__main__":

    loader = InMemoryLoader()

    transformer = CleanMissingFields()

    exporter = JSONExpoerter("output.json")

    pipeline = DataPipeline(loader=loader, transformer=transformer, exporter=exporter)

    pipeline.run()

