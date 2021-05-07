from scipy import optimize
import sympy as sym
import xlsxwriter
import time
from sympy.matrices import zeros
sym.init_printing(use_latex="mathjax")


def paso(df_eval, x):
    # print("Line-search 1")
    f = lambda alpha: 100*(x[1]-alpha*df_eval[1] - (x[0]-alpha*df_eval[
    0])**2)**2 + (1 - (x[0]-alpha*df_eval[0]))**2
    alpha_min = optimize.fminbound(f, -2, 2)
    return alpha_min


def gradient(f, varls):
    """ Calcula el gradiente de una función f(x1,x2,...)"""
    n = len(varls)
    G = zeros(n, 1)
    for i in range(n):
        G[i] = f.diff(varls[i])
    return G


def cond_armijo(parametro, df_eval, x, xk, cond):
    fx = sym.sympify(f).subs({"x1": x[0], "x2": x[1]})
    fxk = sym.sympify(f).subs({"x1": xk[0], "x2": xk[1]})
    if cond == 1:
        return parametro * (df_eval.T * (x - xk))[0] <= fx - fxk
    else:
        return parametro * (df_eval.T * (x - xk))[0] >= fx - fxk


def gradiente(x0, f, df, tol, maxIt, opcion):
    x = sym.Matrix(([x0[0]], [x0[1]]))
    i = 0
    error = []
    expenses = []
    for n in range(maxIt):
        i = n
        df_eval = sym.sympify(df).subs({"x1": x[0], "x2": x[
            1]})
        if opcion == 1:
            x = x - paso(df_eval, x)*df_eval
            error.append(((sym.Matrix([1, 1]) - x).norm()/sym.Matrix([1, 1]).norm(),
                          i + 1))
            # ele = worksheet
        else:
            paso_2 = 1
            # print("Line-search 2")
            alpha = 0.1
            beta = 0.99
            # ele = experimento_2
            while True:
                xk = x - paso_2 * df_eval
                if cond_armijo(alpha, df_eval, x, xk, 1):
                    # print("primera si")
                    if cond_armijo(beta, df_eval, x, xk, 2):
                        # print("segunda si")
                        x = x - paso_2 * df_eval
                        error.append(((sym.Matrix([1, 1]) - x).norm(

                        )/sym.Matrix([1, 1]).norm(),
                                      i+1))
                        break
                    else:
                        print("segunda no")

                else:
                    paso_2 = paso_2*0.5
        # print(float(x[0]), float(x[1]), i+1)
        expenses.append([i+1, str((float(x[0]), float(x[1]))),
                         sym.sympify(f).subs({"x1": x[0], "x2": x[1]}),
                         df_eval.norm()])
        if df_eval.norm() < tol:
            break

    return x, i + 1, error, expenses


inicio1 = time.time()
x1, x2 = sym.symbols("x1 x2")
f = 100*(x2 - (x1)**2)**2 + (1 - x1)**2
variables = (x1, x2)
df = gradient(f, variables)

x0 = [-2, 2]
maxIt = 2000
tol = 1e-16

workbook = xlsxwriter.Workbook('Expermimento_gradiente.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
worksheet.write('A1', 'iteracion', bold)
worksheet.write('B1', 'x', bold)
worksheet.write('C1', 'fx', bold)
worksheet.write('D1', 'criterio parada', bold)

resultado1 = gradiente(x0, f, df, tol, maxIt, 1)

row = 1
col = 0
for iteracion, x_val, fx, parada in resultado1[3]:
    worksheet.write(row, col, iteracion)
    worksheet.write(row, col + 1, x_val)
    worksheet.write(row, col + 2, fx)
    worksheet.write(row, col + 3, parada)
    row += 1
print("final exp. 1: {}".format(time.time() - inicio1))

inicio2 = time.time()

experimento_2 = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
experimento_2.write('A1', 'iteracion', bold)
experimento_2.write('B1', 'x', bold)
experimento_2.write('C1', 'fx', bold)
experimento_2.write('D1', 'criterio parada', bold)

resultado2 = gradiente(x0, f, df, tol, maxIt, 2)

row = 1
col = 0
for iteracion, x_val, fx, parada in resultado1[3]:
    experimento_2.write(row, col, iteracion)
    experimento_2.write(row, col + 1, x_val)
    experimento_2.write(row, col + 2, fx)
    experimento_2.write(row, col + 3, parada)
    row += 1


print("final exp. 2: {}".format(time.time() - inicio2))
workbook.close()

