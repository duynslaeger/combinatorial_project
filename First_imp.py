from math import exp
import numpy


def First_improvement(Mu, R):
    S=[]
    Denominator_S = 1
    delta = 1
    AP = R[0]
    
    # while jusqu'a ce que AP ne soit plus optimisé
    while delta > 0:

        # second while pour itéré sur n pour sélectionner
        for elem in range(len(R)):

            # Je prend un élément, est ce que cette élement à modifier positivement AP ?
            if elem in S:
                # non on continue
                pass
            else:
                # oui on prend
                new_denominator = Denominator_S + exp(Mu[elem])
                temp_S = S + [elem]
                new_AP = R[0]*(1/new_denominator)+ sum(R[elem]*(exp(Mu[elem])/new_denominator) for elem in temp_S)
                delta = new_AP - AP
                if (delta > 0):
                    S.append(elem)
                    break
        
        if (delta > 0):
            AP = new_AP
            Denominator_S = new_denominator

    return S, AP