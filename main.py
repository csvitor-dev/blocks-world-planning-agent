""" 
TRABALHO DE INTELIGÊNCIA ARTIFICIAL

Equipe:
    - Agnaldo Erick Maia de Oliveira (539650) [ES]
    - Francisco Rodrigo de Santiago Pinheiro (554394) [ES]
    - Vitor Costa de Sousa (536678) [ES]
"""

from lib.utils import cmd
from src.parser.domain_mapper import DomainMapper
from src.domain.planning import Planning


def app() -> None:
    instance_id = cmd.pluck_instance_from_cmd_args()

    instance = DomainMapper.get_instance(instance_id)
    planning = Planning(instance)

    planning.set_algoritm('A*')
    planning.execute()
    planning.set_algoritm('BFS')
    planning.execute()
    planning.set_algoritm('DLS')
    planning.execute()
    planning.set_algoritm('IDS')
    planning.execute()


if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print('Errors:', e.args)
