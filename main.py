import time
import os
from itertools import product, combinations

start_time = time.time()

def relacoes(A):
    n = len(A)
    with open('relations.txt', 'w') as file:
        for subset in product([0, 1], repeat=n*n):
            relacao = set()
            for i, j in combinations(range(n), 2):
                if subset[i*n+j]:
                    relacao.add((A[i], A[j]))
                    relacao.add((A[j], A[i]))
            
            if len(relacao) == 0:
                file.write('{} ' + classificar(relacao, A) + '\n')
            else:
                file.write(str(relacao) + ' ' + classificar(relacao, A) + '\n')


def classificar(relacao, A):

    simetrica = all((y, x) in relacao for x, y in relacao)
    transitiva = all((x, w) in relacao for x, y in relacao for z, w in relacao if y == z)
    reflexiva = all((a, a) in relacao for a in A)
    irreflexiva = all((a, a) not in relacao for a in A)

    equivalence = reflexiva and simetrica and transitiva

    classification = ''
    if equivalence:
        classification += "STRE"
    else:
        if simetrica:
            classification = "S"
        if transitiva:
            classification += "T"
        if reflexiva:
            classification += "R"
    if irreflexiva:
        classification += "I"
    
    # verifica se é função
    if len(relacao) < 2:
        return classification
    else:
        function_bij = True
        function_surj = True
        function_inj = True

        range_values = set([y for x, y in relacao])
        if len(range_values) != len(A):
            function_bij = False
        else:
            for a in A:
                count = sum(y == a for x, y in relacao)
                if count != 1:
                    function_bij = False
                    break
        if range_values != set(A):
            function_surj = False

        domain_values = set([x for x, y in relacao])
        if len(domain_values) != len(A):
            function_inj = False
        else:
            for y in set([y for x, y in relacao]):
                count = sum(y == a for a, z in relacao if z == y)
                if count != 1:
                    function_inj = False
                    break

        classification += "Fu"
        if function_bij:
            classification += "Fb"
        if function_surj:
            classification += "Fs"
        if function_inj:
            classification += "Fi"
    
    return classification

A = (1, 2, 3, 4)
relacoes(A)

end_time = time.time()
total_time = end_time - start_time
print(f"Tempo total de execução: {total_time} segundos")

size = os.path.getsize("relations.txt")
print(f"Tamanho do arquivo: {size} bytes")