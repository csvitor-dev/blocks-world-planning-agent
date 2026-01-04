""" 
TRABALHO DE INTELIGÊNCIA ARTIFICIAL

Equipe:
    - Agnaldo Erick Maia de Oliveira (539650) [ES]
    - Francisco Rodrigo de Santiago Pinheiro (554394) [ES]
    - Vitor Costa de Sousa (536678) [ES]
"""
from src.parser.domain_mapper import DomainMapper
from src.domain.planning import Planning


def execute(instance_id: str, alg: str) -> None:
    instance = DomainMapper.get_instance(instance_id)
    planning = Planning(instance, instance_id=instance_id)
    planning.set_algorithm(alg)
    planning.execute(enable_csv=True)


def app() -> None:
    instances = [
        '4-0',
        '4-1',
        '4-2',
        '5-0',
        '7-0',
        # '8-0',
        # '9-0',
        # '9-1',
        # '9-2',
        # '10-0',
        # '12-0',
        # '12-1',
        # '12-2',
        # '13-0',
        # '13-1',
        # '14-0',
        # '15-0',
        # '17-0',
    ]
    algorithms = ['BFS', 'DLS', 'IDS', 'A*', 'BiA*']

    for instance_id in instances:
        for alg in algorithms:
            execute(instance_id, alg)


if __name__ == "__main__":
    print("Batch execution started...")
    app()
