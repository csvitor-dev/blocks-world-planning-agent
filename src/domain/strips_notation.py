class StripsNotation:
    def __init__(self, actions: list[str], initial_state: str, goal_state: str) -> None:
        self.__propositions: set[str] = set()
        self.__actions = self.__create_actions(actions)
        self.__initial_state = self.__resolve_steps_group(initial_state)
        self.__goal_state = self.__resolve_steps_group(goal_state)
    
    def __create_actions(self, raw_actions: list[str]) -> dict[str,dict[str,list[str]]]:
        hook: dict[str,dict[str,list[str]]] = {}
        for i in range(0, len(raw_actions), 3):
            preconditions, post_conditions = self.__resolve_steps_group(raw_actions[i+1]), self.__resolve_steps_group(raw_actions[i+2])
            self.__add_proposition_group(preconditions + post_conditions)

            hook[raw_actions[i]] = {
                'pre': preconditions,
                'post': post_conditions
            }
        return hook

    def __resolve_steps_group(self, raw_state: str) -> list[str]:
        return raw_state.split(';')

    def __add_proposition_group(self, steps: list[str]) -> None:
        for step in steps:
            self.__propositions.add(step)

    def get_actions(self) -> dict[str,dict[str,list[str]]]:
        return self.__actions

    def get_states(self) -> dict[str, list[str]]:
        return {
            'initial': self.__initial_state,
            'goal': self.__goal_state,
        }

    def get_all_propositions(self) -> list[str]:
        return list(self.__propositions)