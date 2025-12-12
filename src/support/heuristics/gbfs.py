from typing import Set
from src.domain.blocks_world_state import BlocksWorldState


def h(current_state: BlocksWorldState, goal: Set[int]) -> int:
    score = 0

    for fact in current_state.current:
        if current_state.parent is not None and fact not in current_state.parent.current and fact in goal:
            score += 2
        elif fact in goal:
            score += 1
        elif current_state.parent is not None and fact in current_state.parent.current and fact not in goal:
            score -= 2
        elif fact not in goal:
            score -= 1
    return score
