class ClausalForm:
    conversao = {
        "clear_a": 1,
        "clear_b": 2,
        "clear_c": 3,
        "clear_d": 4,
        "handempty": 5,
        "holding_a": 6,
        "holding_b": 7,
        "holding_c": 8,
        "holding_d": 9,
        "on_a_b": 10,
        "on_a_c": 11,
        "on_a_d": 12,
        "on_b_a": 13,
        "on_b_c": 14,
        "on_b_d": 15,
        "on_c_a": 16,
        "on_c_b": 17,
        "on_c_d": 18,
        "on_d_a": 19,
        "on_d_b": 20,
        "on_d_c": 21,
        "ontable_a": 22,
        "ontable_b": 23,
        "ontable_c": 24,
        "ontable_d": 25
    }

    def encode(sentenca):
        itens = sentenca.split(";")
        resultado = []
        for item in itens:
            item = item.strip()
            if item.startswith("~"):
                proposicao = item[1:]
                resultado.append(-ClausalForm.conversao[proposicao])
            else:
                resultado.append(ClausalForm.conversao[item])
        return resultado
