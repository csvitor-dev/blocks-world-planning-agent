from pathlib import Path
from os import path

class FileManager:
    @staticmethod
    def read(path: Path) -> list[str]:
        with open(path, 'r') as file:
            return file.readlines()
    
    @staticmethod
    def load():
        ...

    @staticmethod
    def resolve_path(base_path: str, fileName: str) -> Path:
        abs_path = path.abspath(f'{base_path}/{fileName}')
        target_path = Path(abs_path)

        if target_path.exists() is False:
            raise FileExistsError()
        return target_path
