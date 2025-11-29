""" 
TRABALHO DE INTELIGÊNCIA ARTIFICIAL

Equipe:
    - Agnaldo Erick Maia de Oliveira (539650) [ES]
    - Francisco Rodrigo de Santiago Pinheiro (554394) [ES]
    - Vitor Costa de Sousa (536678) [ES]
"""

from src.parser.domain_mapper import DomainMapper
from src.domain.clausal_form import ClausalForm
from lib.utils import cmd

def app() -> None:
    instance_id = cmd.pluck_instance_from_cmd_args()
    
    instance = DomainMapper.get_instance(instance_id)
    expression = ClausalForm(instance)
    print(expression.get_actions())

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print('Errors:', e.args)
