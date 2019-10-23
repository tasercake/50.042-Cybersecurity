#!/usr/bin/env python3
"""
50.042 FCS Lab 5 Modular Arithmetics
Year 2019

Krishna Penukonda - 1001781
"""
from itertools import zip_longest


class Polynomial2:
    def __init__(self, coeffs=None):
        self.coeffs = [] or coeffs  # Polynomial defaults to 0
        while self.coeffs and self.coeffs[-1] == 0:
            del self.coeffs[-1]  # Remove trailing zeros
        if not self.coeffs:
            self.coeffs.append(0)
        super(Polynomial2, self)

    def add(self, p2):
        return self.xor(p2)

    def sub(self, p2):
        return self.xor(p2)

    def mul(self, p2, modp=None):
        partials = [p2]
        for i in range(self.degree):
            partial = partials[-1].left_shifted()
            if modp and modp.degree == partial.degree:
                partial = partial.drop_msb() + modp.drop_msb()
            partials.append(partial)
        return sum([p for i, p in enumerate(partials) if self.coeffs[i]] or [self.__class__([0])])

    def div(self, p2):
        quotient = self.__class__([0])
        remainder = self.__class__(self.coeffs)
        degree = p2.degree
        while remainder.degree >= degree:
            coeffs = [0 for _ in range(remainder.degree - degree + 1)]
            coeffs[-1] = 1
            s = self.__class__(coeffs)
            quotient = quotient + s
            remainder = remainder - s * p2
        return quotient, remainder

    def getInt(self):
        return sum([bit << i for i, bit in enumerate(self.coeffs)])

    def xor(self, p2):
        new_coeffs = [c1 ^ c2 for c1, c2 in zip_longest(
            self.coeffs, p2.coeffs, fillvalue=0)]
        return self.__class__(new_coeffs)

    def left_shifted(self, n=1):
        assert n >= 0
        return self.__class__([0 for _ in range(n)] + self.coeffs)

    def drop_msb(self, n=1):
        assert n >= 0
        return self.__class__(self.coeffs[:-n])

    @property
    def degree(self):
        if len(self.coeffs) == 1 and not self.coeffs[0]:
            return -1
        return len(self.coeffs) - 1

    def __str__(self):
        terms = [(f'x^{i}' if i else '1') for i, c in enumerate(self.coeffs) if c] or ['0']
        return ' + '.join(reversed(terms))

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        if isinstance(other, (float, int)):
            return self
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mul(other)

    def __truediv__(self, other):
        return self.div(other)

    def __int__(self):
        return self.getInt()


class GF2N:
    affinemat = [[1, 0, 0, 0, 1, 1, 1, 1],
                 [1, 1, 0, 0, 0, 1, 1, 1],
                 [1, 1, 1, 0, 0, 0, 1, 1],
                 [1, 1, 1, 1, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 0, 0],
                 [0, 0, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1]]

    def __init__(self, x, n=8, ip=Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])):
        self.poly = Polynomial2([int(b) for b in bin(x)[:1:-1]][:n])
        self.n = n
        self.ip = ip

    def add(self, g2):
        return self.__class__(int(self.poly + g2.poly), n=self.n, ip=self.ip)

    def sub(self, g2):
        return self.__class__(int(self.poly - g2.poly), n=self.n, ip=self.ip)

    def mul(self, g2):
        return self.__class__(int(self.poly.mul(g2.poly, modp=self.ip)), n=self.n, ip=self.ip)

    def div(self, g2):
        q, r = self.poly / g2.poly
        q = self.__class__(int(q), n=self.n, ip=self.ip)
        r = self.__class__(int(r), n=self.n, ip=self.ip)
        return q, r

    def getPolynomial2(self):
        return self.poly

    def __str__(self):
        return str(self.getInt())

    def getInt(self):
        return self.poly.getInt()

    def mulInv(self):
        r1 = self.ip
        r2 = self.poly
        t1 = Polynomial2([0])
        t2 = Polynomial2([1])
        while r2.getInt() > 0:
            q = r1.div(r2)[0]

            r = r1.sub(q.mul(r2))
            r1 = r2
            r2 = r

            t = t1 - q.mul(t2)
            t1 = t2
            t2 = t
        if r1.getInt() == 1:
            return self.__class__(t1.getInt(), n=self.n, ip=self.ip)

    def affineMap(self):
        pass


if __name__ == "__main__":
    print('\nTest 1')
    print('======')
    p1 = Polynomial2([0, 1, 1, 0, 0, 1])
    p2 = Polynomial2([1, 0, 1, 1])
    print(f'p1 = {p1}')
    print(f'p2 = {p2}')
    p3 = p1.add(p2)
    print(f'p3 = p1 + p2 = {p3}')

    print('\nTest 2')
    print('======')
    p4 = Polynomial2([0, 1, 1, 1, 1, 0, 0, 1])
    # modp = Polynomial2([1,1,0,1,1,0,0,0,1])
    modp = Polynomial2([1, 0, 0, 0, 1, 1, 0, 1, 1])
    print(f'p1 = {p1}')
    print(f'p4 = {p4}')
    print(f'modp = {modp}')
    p5 = p1.mul(p4, modp)
    print(f'p5 = p1 * p4 mod (modp) = {p5}')

    print('\nTest 3')
    print('======')
    p6 = Polynomial2([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    p7 = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
    print(f'p6={p6}')
    print(f'p7={p7}')
    p8q, p8r = p6.div(p7)
    print(f'q for p6/p7 ={p8q}')
    print(f'r for p6/p7 = {p8r}')
    print(f'Division sanity check: ({p7})({p8q}) + {p8r} = {(p7 * p8q) + p8r}')

    ####
    print('\nTest 4')
    print('======')
    g1 = GF2N(100)
    g2 = GF2N(5)
    print(f'g1 = {g1.getPolynomial2()}')
    print(f'g2 = {g2.getPolynomial2()}')
    g3 = g1.add(g2)
    print(f'g1 + g2 = {g3}')

    print('\nTest 5')
    print('======')
    ip = Polynomial2([1, 1, 0, 0, 1])
    print('irreducible polynomial', ip)
    g4 = GF2N(0b1101, 4, ip)
    g5 = GF2N(0b110, 4, ip)
    print('g4 = ', g4.getPolynomial2())
    print('g5 = ', g5.getPolynomial2())
    g6 = g4.mul(g5)
    print(f'g4 x g5 = {g6.getPolynomial2()}')

    print('\nTest 6')
    print('======')
    g7 = GF2N(0b1000010000100, 13, None)
    g8 = GF2N(0b100011011, 13, None)
    print('g7 = ', g7.getPolynomial2())
    print('g8 = ', g8.getPolynomial2())
    q, r = g7.div(g8)
    print('g7 / g8 =')
    print('q = ', q.getPolynomial2())
    print('r = ', r.getPolynomial2())

    print('\nTest 7')
    print('======')
    ip = Polynomial2([1, 1, 0, 0, 1])
    print('irreducible polynomial', ip)
    g9 = GF2N(0b101, 4, ip)
    print('g9 = ', g9.getPolynomial2())
    print('inverse of g9 =', g9.mulInv().getPolynomial2())

    print('\nTest 8')
    print('======')
    print("# NOT ATTEMPTED")
    # ip = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
    # print('irreducible polynomial', ip)
    # g10 = GF2N(0xc2, 8, ip)
    # print('g10 = 0xc2')
    # g11 = g10.mulInv()
    # print('inverse of g10 = g11 =', hex(g11.getInt()))
    # g12 = g11.affineMap()
    # print('affine map of g11 =', hex(g12.getInt()))
