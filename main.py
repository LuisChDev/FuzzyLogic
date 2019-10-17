import skfuzzy as fuzz      # type: ignore
import numpy as np          # type: ignore


# generando las variables del universo
x_tam = np.arange(40, 801, 1)
x_dst = np.arange(1, 16, 1)
x_prc = np.arange(70, 3001, 1)

# generando los conjuntos difusos
# # tamaño
tam_peq = fuzz.trapmf(x_tam, [40, 60, 80, 90])
tam_med = fuzz.trapmf(x_tam, [80, 100, 200, 220])
tam_grd = fuzz.trapmf(x_tam, [180, 400, 600, 810])
# # distancia
dst_crc = fuzz.trimf(x_dst, [1, 4, 7])
dst_ljs = fuzz.trimf(x_dst, [5, 10, 12])
dst_afr = fuzz.trimf(x_dst, [11, 13, 16])
# # precio
prc_baj = fuzz.trapmf(x_prc, [60, 70, 80, 90])
prc_med = fuzz.trapmf(x_prc, [80, 120, 150, 200])
prc_alt = fuzz.trapmf(x_prc, [180, 200, 600, 3050])


# % pertenencia a los conjuntos
def pertenenciaTam(tam):
    tam_level_peq = fuzz.interp_membership(x_tam, tam_peq, tam)
    tam_level_med = fuzz.interp_membership(x_tam, tam_med, tam)
    tam_level_grd = fuzz.interp_membership(x_tam, tam_grd, tam)
    return (tam_level_peq, tam_level_med, tam_level_grd)


def pertenenciaDst(dst):
    dst_level_crc = fuzz.interp_membership(x_dst, dst_crc, dst)
    dst_level_ljs = fuzz.interp_membership(x_dst, dst_ljs, dst)
    dst_level_afr = fuzz.interp_membership(x_dst, dst_afr, dst)
    return(dst_level_crc, dst_level_ljs, dst_level_afr)

# 1. Si la casa ES grande, el precio ES alto.
# esto se representa con el MIN de los valores %grande y %alto.

# 2. Si la casa ESTÁ cerca del centro, el precio ES alto.
# Esto se representa con el MIN de los valores %cerca y %alto.

# 3. Si la casa ES media O pequeña Y ESTÁ lejos del centro, el precio ES medio.
# Esto se representa con el MIN de los valores
# # MIN(MAX(%media, %pequeña), %lejos) y %medio.

# 3. Si la casa ES media O pequeña Y ESTÁ en las afueras, el precio ES bajo.
# # MIN(MAX(%media, %pequeña), %afueras) y %bajo.


def compute(tam, dst):
    # se difusan los valores.
    (tam_peq, tam_med, tam_grd) = pertenenciaTam(tam)
    (dst_crc, dst_ljs, dst_afr) = pertenenciaDst(dst)

    # se calcula la regla 1.
    prc_alt_grd = np.fmin(tam_grd, prc_alt)

    # se calcula la regla 2.
    prc_alt_crc = np.fmin(dst_crc, prc_alt)

    # se calcula la regla 3.
    prc_med_peqMedLjs = np.fmin(
        np.fmin(np.fmax(tam_peq, tam_med), dst_ljs), prc_med)

    # se calcula la regla 4.
    prc_baj_peqMedAfr = np.fmin(
        np.fmin(np.fmax(tam_peq, tam_med), dst_afr), prc_baj)

    # se combinan los resultados
    resultados_ = np.fmax(prc_alt_grd, np.fmax(
        prc_alt_crc, np.fmax(
            prc_med_peqMedLjs, prc_baj_peqMedAfr)))

    # se calcula el resultado "afilado" (usando el centroide de la forma)
    precio = fuzz.defuzz(x_prc, resultados_, 'centroid')
    return precio


if __name__ == "__main__":
    print("bienvenido al programa.")
    tam = input("Ingrese el tamaño de la casa, en m^2: ")
    dst = input("Ahora la distancia al centro en km: ")

    precio = compute(tam, dst)

    print("El precio calculado es: ", precio)
