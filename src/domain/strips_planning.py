class StripsPlanning:
    def __init__(self, actions: list[str], initial_state: str, goal_state: str) -> None:
        self.__actions = self.__create_actions(actions)
        self.__initial_state = initial_state
        self.__goal_state = goal_state
    
    def __create_actions(self, raw_actions: list[str]) -> dict[str,tuple[str,str]]:
        hook: dict[str,tuple[str,str]] = {}
        for i in range(0, len(raw_actions), 3):
            hook[raw_actions[i]] = (raw_actions[i+1], raw_actions[i+2])
        return hook

    def get_actions(self) -> dict[str,tuple[str,str]]:
        return self.__actions

    def get_states(self) -> dict[str, str]:
        return {
            'initial': self.__initial_state,
            'goal': self.__goal_state
        }
