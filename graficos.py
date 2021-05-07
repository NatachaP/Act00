from P6_newton import resultado
from P6_gradiente_ import resultado1, resultado2
import matplotlib.pyplot as plt

graf1 = resultado1[2]
graf2 = resultado2[2]
graf3 = resultado[2]

r1x = [x[0] for x in graf1]
r1y = [x[1] for x in graf1]

r2x = [x[0] for x in graf2]
r2y = [x[1] for x in graf2]

r3x = [x[0] for x in graf3]
r3y = [x[1] for x in graf3]

plt.scatter(r1y[:10], r1x[:10])
plt.scatter(r2y[:10], r2x[:10])
plt.scatter(r3y, r3x)
plt.show()

plt.scatter(r1y, r1x)
plt.scatter(r2y, r2x)
plt.scatter(r3y, r3x)
plt.show()


