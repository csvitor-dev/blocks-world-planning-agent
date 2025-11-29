from src.domain.strips_planning import StripsPlanning

class ClausalForm:
    def __init__(self, strips: StripsPlanning):
        self.__map = self.__map_clauses(strips)
        
        states = strips.get_states()
        self.__initial_state = self.__resolve_state(states['initial'])
        self.__goal_state = self.__resolve_state(states['goal'])

    def __map_clauses(self, strips: StripsPlanning) -> dict[str,int]:
        action_hook: dict[str,int] = {}
        counter = 1
        
        for proposition in strips.get_all_propositions():
            if proposition not in action_hook.keys():
                if proposition.startswith('~'):
                    action_hook[proposition] = -action_hook.get(proposition[1:], counter)
                else:
                    action_hook[proposition] = abs(action_hook.get(f'~{proposition}', counter))
                counter += 1
        return action_hook

    def __resolve_state(self, target: list[str]) -> list[int]:
        return [self.__map[prop] for prop in target]
    
    def get_map(self) -> dict[str, int]:
        return self.__map
    
    def get_states(self) -> dict[str, list[int]]:
        return {
            'initial': self.__initial_state,
            'goal': self.__goal_state,
        }
