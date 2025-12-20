""" 
TRABALHO DE INTELIGÊNCIA ARTIFICIAL

Equipe:
    - Agnaldo Erick Maia de Oliveira (539650) [ES]
    - Francisco Rodrigo de Santiago Pinheiro (554394) [ES]
    - Vitor Costa de Sousa (536678) [ES]
"""

import time
from lib.utils import cmd
from src.parser.domain_mapper import DomainMapper
from src.domain.planning import Planning


def execute(id: str, alg: str, dont_show_output: bool) -> None:
    instance = DomainMapper.get_instance(id)
    planning = Planning(instance)

    if dont_show_output:
        planning.off_report()
    planning.set_algorithm(alg)
    planning.execute()


def app() -> None:
    flags = cmd.pluck_flags_from_cmd_args(search_for=['instance', 'algorithm', 'only-execute'])

    if len(flags['instance']) == 1:
        execute(flags['instance'][0], flags['algorithm'], dont_show_output=flags['only-execute'])
        return
    for instance_id in flags['instance']:
        execute(instance_id, flags['algorithm'], dont_show_output=flags['only-execute'])
        time.sleep(5)


if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print('Errors:', e.args)
