import sympy as sym
import xlsxwriter
import time
from sympy.matrices import hessian, zeros
sym.init_printing(use_latex="mathjax")


def gradient(f, varls):
    """ Calcula el gradiente de una función f(x1,x2,...)"""
    n = len(varls)
    G = zeros(n,1)
    for i in range(n):
        G[i] = f.diff(varls[i])
    return G


def dk(f, variables):
    df = gradient(f, variables)

    df1 = df[0]
    df2 = df[1]

    ddf1 = gradient(df1, variables)
    ddf2 = gradient(df2, variables)

    matriz = ddf1.row_join(ddf2)
    matriz_invertida = matriz.inv()
    return matriz_invertida, df


def newton(dk, x0, tol, maxIt):
    x = sym.Matrix(([x0[0]], [x0[1]]))
    i = 0
    error = []
    expenses = []
    for n in range(maxIt):
        i = n
        x = x - sym.sympify(dk[0]*dk[1]).subs({"x1": x[0], "x2": x[1]})
        error.append((float((sym.Matrix([1, 1]) - x).norm()/sym.Matrix([1,
                                                                   1]).norm()),
                          i + 1))
        expenses.append([i + 1, str((float(x[0]), float(x[1]))),
                         sym.sympify(f).subs({"x1": x[0], "x2": x[1]}),
                         sym.sympify(dk[1]).subs(
                             {"x1": x[0], "x2": x[1]}).norm()])

        if sym.sympify(dk[1]).subs({"x1": x[0], "x2": x[1]}).norm() < tol:
            break

    row = 1
    col = 0
    for iteracion, x_val, fx, parada in expenses:
        experimento3.write(row, col, iteracion)
        experimento3.write(row, col + 1, x_val)
        experimento3.write(row, col + 2, fx)
        experimento3.write(row, col + 3, parada)
        row += 1
    print(error)
    return x, i+1, error


inicio3 = time.time()
x1, x2 = sym.symbols("x1 x2")
f = 100*(x2 - x1**2)**2 + (1 - x1)**2
variables = (x1, x2)
dk = dk(f, variables)

x0 = [-2, 2]
maxIt = 10
tol = 1e-16

workbook = xlsxwriter.Workbook('Experimento_Newton.xlsx')
experimento3 = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
experimento3.write('A1', 'iteracion', bold)
experimento3.write('B1', 'x', bold)
experimento3.write('C1', 'fx', bold)
experimento3.write('D1', 'criterio parada', bold)

resultado = newton(dk, x0, tol, maxIt)

# print([float(resultado[0][0]), float(resultado[0][1])], resultado[1])
print("termino exp. 3: {}".format(time.time() - inicio3))
workbook.close()
