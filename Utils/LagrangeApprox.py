from numpy.polynomial.polynomial import  *


def basisPolynomial(_nodes: list, _pivot: int) -> Polynomial:
    product = Polynomial([1])
    for i in range(len(_nodes)):
        if i == _pivot:
            continue
        basisFactor = Polynomial([-1 * _nodes[i], 1])
        product *= basisFactor / basisFactor(_nodes[_pivot])
    return product

def lagrangeInterpolation(_Xnodes: list, _Ynodes: list):
    summation = Polynomial([0])
    for k in range(len(_Xnodes)):
        summation += _Ynodes[k] * basisPolynomial(_Xnodes, k)
    return summation

if __name__ == '__main__':
    print(lagrangeInterpolation([0, 0.25, 0.5, 0.75, 1], [0, 0.75, 0.5, 0.25, 1]))