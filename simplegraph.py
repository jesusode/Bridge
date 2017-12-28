# Israel Fermín Montilla <ferminster@gmail.com>

class SimpleGraph():
    def __init__(self):
        self._spo = {}
        self._pos = {}
        self._osp = {}

    def _addToIndex(self, index, a, b, c):
        if a not in index: index[a] = {b: set([c])}
        else:
            if b not in index[a]: index[a][b] = set([c])
            else: index[a][b].add(c)

    def add(self, (sub, pred, obj)):
        self._addToIndex(self._spo, sub, pred, obj)
        self._addToIndex(self._pos, pred, obj, sub)
        self._addToIndex(self._osp, obj, sub, pred)

    def _removeFromIndex(self, index, a, b, c):
        try:
            bs = index[a]
            cset = bs[b]
            cset.remove(c)
            if len(cset) == 0: del bs[b]
            if len(bs) == 0: del index[a]
            # Pueden ocurrir errores si falta un DictKey
        except KeyError:
            pass

    def value(self, sub=None, pred=None, obj=None):
        for retSub, retPred, retObj in self.triples((sub, pred, obj)):
            if sub is None: return retSub
            if pred is None: return retPred
            if obj is None: return retObj
        return None

    def triples(self, (sub, pred, obj)):
    # Revisamos qué términos están para usar el íldice correcto
        try:
            if sub != None:
                if pred != None:
                    # sub pred obj
                    if obj != None:
                        if obj in self._spo[sub][pred]:
                            yield(sub, pred, obj)
                    # sub pred None
                    else:
                        for retObj in self._spo[sub][pred]:
                            yield(sub, pred, retObj)
                else:
                    # sub None obj
                    if obj != None:
                        for retPred in self._osp[obj][sub]:
                            yield(sub, retPred, obj)
                    else:
                    # sub None None
                        for retPred, objSet in self._spo[sub].itemp():
                            for retObj in objSet:
                                yield(sub, retPred, retObj)
            else:
                if pred != None:
                    if obj != None:
                        for retSub in self._pos[pred][obj]:
                            yield(retSub, pred, obj)
                    #None pred None
                    else:
                        for retObj, subSet in self._pos[pred].items():
                            for retSub in subSet:
                                yield(retSub, pred, retObj)
                else:
                    # None None obj
                    if obj != None:
                        for retSub, predSet in self._osp[obj].items():
                            for retPred in predSet:
                                yield(retSub, retPred, obj)
                    # None None None
                    else:
                        for retSub, predSet in self._spo.items():
                            for retPred, objSet in predSet.items():
                                for retObj in objSet:
                                    yield(retSub, retPred, retObj)
        except:
            pass



    def remove(self, (sub, pred, obj)):
        triples = list(self.triples((sub, pred, obj)))
        for (delSub, delPred, delObj) in triples:
            self._removeFromIndex(self._spo, delSub, delPred, delObj)
            self._removeFromIndex(self._pos, delPred, delObj, delSub)
            self._removeFromIndex(self._osp, delObj, delSub, delPred)

    def load(self, filename):
        f = open(filename, "rb")
        reader = csv.reader(f)
        for sub, pred, obj in reader:
            sub = unicode(sub, "UTF-8")
            pred = unicode(pred, "UTF-8")
            obj = unicode(obj, "UTF-8")
            self.add((sub, pred, obj))
        f.close()

    def save(self, filename):
        f = open(filename, "wb")
        writer = csv.writer(f)
        for sub, pred, obj in self.triples((None, None, None)):
            writer.writerow([sub.encode("UTF-8"), pred.encode("UTF-8"), onj.encode("UTF-8")])
        f.close()

    def query(self, clauses):
        bindings = None
        for clause in clauses:
            bpos = {}
            qc = []       # for query clause
            for pos, elem in enumerate(clause):
                if elem.startswith('?'):
                    qc.append(None)
                    bpos[elem] = pos
                else:
                    qc.append(elem)
            pre_results = list(self.triples((qc[0], qc[1], qc[2])))
            if bindings == None:
            # A la primera siempre pasa, los demás si tienen algo
                bindings = []
                for pre_result in pre_results:
                    binding = {}
                    for var, pos in bpos.items():
                        binding[var] = pre_result[pos]
                    bindings.append(binding)
            else:
                # Eliminar vínculos que no aplican
                newb = []
                for binding in bindings:
                    for result in pre_results:
                        valid_match = True
                        temp_binding = binding.copy()
                        for var, pos in bpos.items():
                            if var in temp_binding:
                                if temp_binding[var] != result[pos]:
                                    valid_match = False
                            else:
                                temp_binding[var] = result[pos]
                        if valid_match: newb.append(temp_binding)
                    bindings = newb
            return bindings