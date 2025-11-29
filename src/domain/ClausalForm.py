class ClausalForm:
    def __init__(self, planning):
        self.planning = planning
        self.conversao = self._criar_mapa()
        self.estado_inicial = self._cod(planning.initial_state)
        self.estado_final = self._cod(planning.goal_state)

    def _criar_mapa(self):
        props = set()

        for acao in self.planning.actions:
            for p in acao.precond_pos:
                props.add(p)
            for p in acao.precond_neg:
                props.add("~" + p)
            for p in acao.effect_pos:
                props.add(p)
            for p in acao.effect_neg:
                props.add("~" + p)

        for p in self.planning.initial_state:
            props.add(p)

        for p in self.planning.goal_state:
            props.add(p)

        props = sorted(list(props))
        mapa = {}
        n = 1

        for p in props:
            if p.startswith("~"):
                base = p[1:]
                mapa[p] = -n
                mapa[base] = n
            else:
                if p not in mapa:
                    mapa[p] = n
            n += 1

        return mapa

    def _cod(self, lista):
        return [self.conversao[p] for p in lista]
