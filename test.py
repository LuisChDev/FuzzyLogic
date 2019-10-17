import numpy as np  # type: ignore
from main import compute
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore

tamanos = np.arange(41, 801, 20)
distancias = np.arange(2, 16, 1)

posibles = []
for x in tamanos:
    posiblesRow = []
    for y in distancias:
        posiblesRow.append((x, y))
    posibles.append(posiblesRow)

resultados = []
for x in posibles:
    resultadosRow = []
    for y in x:
        resultado = round(compute(y[0], y[1]), 2)
        resultadosRow.append(resultado)
        # print(resultado)
    resultados.append(resultadosRow)

resultados_ = np.array(resultados)


def pprintMtrx(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return('\n'.join(table))


if __name__ == "__main__":
    # print(resultados[50:100])

    # print(resultados_)

    # plt.imshow(resultados_, cmap='hot', interpolation='nearest')
    # plt.show()

    with open("tabla_resultados.txt", 'w') as f:
        f.write(pprintMtrx(resultados))

    # # graficando con seaborn
    # hm = sns.heatmap(resultados)
    # fig = hm.get_figure()
    # fig.savefig("heatmap5.png")
