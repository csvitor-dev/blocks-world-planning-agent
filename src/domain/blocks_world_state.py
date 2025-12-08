import numpy as np
from typing import Generator, Set


class BlocksWorldState:
    def __init__(self, current_state: Set[int],
                 actions: dict[str, dict[str, Set[int]]],
                 name: str = 'root',
                 parent: 'BlocksWorldState | None' = None) -> None:

        self.n_props = max(abs(x) for x in current_state) + 1
        self.state_vec = np.zeros(self.n_props, dtype=np.bool_)
        for fact in current_state:
            if fact > 0:
                self.state_vec[fact] = True   

        self.key = self.state_vec.tobytes()
        self.actions_masks = self.__convert_actions(actions)

        self.identifier = name
        self.parent = parent

    def successors(self, actions: dict[str, dict[str, Set[int]]]) \
            -> Generator['BlocksWorldState', None, None]:

        for name, masks in self.actions_masks.items():
            pre_mask, add_mask, del_mask = masks
            if np.all(self.state_vec[pre_mask]):
                yield self.__expand(name, add_mask, del_mask, actions)

    def __expand(self, action_name: str,
                 add_mask: np.ndarray,
                 del_mask: np.ndarray,
                 actions: dict[str, dict[str, Set[int]]]) -> 'BlocksWorldState':

        new_vec = self.state_vec.copy()
        new_vec[del_mask] = False
        new_vec[add_mask] = True
        new_state_set = {i for i in range(len(new_vec)) if new_vec[i]}

        return BlocksWorldState(new_state_set, actions,
                                action_name, parent=self)

    def __convert_actions(self, actions: dict[str, dict[str, Set[int]]]):

        converted = {}

        for name, cond in actions.items():

            pre = cond['pre']
            post = cond['post']

            max_index = self.n_props

            pre_mask = np.zeros(max_index, dtype=np.bool_)
            add_mask = np.zeros(max_index, dtype=np.bool_)
            del_mask = np.zeros(max_index, dtype=np.bool_)

            for p in pre:
                if p > 0:
                    pre_mask[p] = True

            for p in post:
                if p > 0:
                    add_mask[p] = True
                else:
                    del_mask[abs(p)] = True

            converted[name] = (pre_mask, add_mask, del_mask)

        return converted

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BlocksWorldState) and self.key == other.key

    def __repr__(self) -> str:
        true_indices = [i for i in range(len(self.state_vec)) if self.state_vec[i]]
        return f"State({true_indices})"
