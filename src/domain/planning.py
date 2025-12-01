from domain.strips_notation import StripsNotation

class Planning:
    def __init__(self, strips: StripsNotation):
        self.__map = self.__map_clauses(strips)

        actions = strips.get_actions()
        self.__actions = self.__resolve_actions(actions)

        states = strips.get_states()
        self.__initial_state = self.__resolve_propositions(states['initial'])
        self.__goal_state = self.__resolve_propositions(states['goal'])

    def __map_clauses(self, strips: StripsNotation) -> dict[str,int]:
        action_hook: dict[str,int] = {}
        
        for proposition in strips.get_all_propositions():
            if proposition not in action_hook.keys():
                action_hook[proposition] = abs(action_hook.get(f'~{proposition}', len(action_hook) + 1)) if proposition.startswith('~') is False else -action_hook.get(proposition[1:], len(action_hook) + 1)
        return action_hook

    def __resolve_propositions(self, target: list[str]) -> list[int]:
        return [self.__map[prop] for prop in target]
    
    def __resolve_actions(self, actions: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, list[int]]]:
        hook: dict[str, dict[str,list[int]]] = {}

        for action, conditions in actions.items():
            hook[action] = {
                'pre': self.__resolve_propositions(conditions['pre']),
                'post': self.__resolve_propositions(conditions['post']),
            }
        return hook
    
    def get_map(self) -> dict[str, int]:
        return self.__map
    
    def get_states(self) -> dict[str, list[int]]:
        return {
            'initial': self.__initial_state,
            'goal': self.__goal_state,
        }
    
    def get_actions(self) -> dict[str, dict[str, list[int]]]:
        return self.__actions
