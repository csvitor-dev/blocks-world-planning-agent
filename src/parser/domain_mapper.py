from src.domain.strips_planning import StripsPlanning
from src.parser.file_manager import FileManager

class DomainMapper:
    @staticmethod
    def get_instance(ref: str) -> StripsPlanning:
        file = FileManager.resolve_path('./planningsat', f'blocks-{ref}.strips')
        raw = FileManager.read(file)

        separation_line =  len(raw) - 3
        actions_set, states = raw[:separation_line], raw[separation_line+1:]

        return StripsPlanning(actions_set, states[0], states[1])