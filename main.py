""" 
TRABALHO DE INTELIGÊNCIA ARTIFICIAL

Equipe:
    - Agnaldo Erick Maia de Oliveira (539650) [ES]
    - Francisco Rodrigo de Santiago Pinheiro (554394) [ES]
    - Vitor Costa de Sousa (536678) [ES]
"""

from src.parser.domain_mapper import DomainMapper

def app() -> None:
    instance = DomainMapper.get_instance('4-0')
    print(instance.get_states())

if __name__ == "__main__":
    app()
