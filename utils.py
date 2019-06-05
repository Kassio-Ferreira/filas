import math
import pandas as pd
import json


def rho(s, lamb, mu):
    return lamb / (s * mu)


# 1 probabilidade de todos os servidores ficarem ociosos
def p0(s, lamb, mu):
    denominador = 0
    for n in range(0, s):
        denominador += ((lamb / mu) ** n) / math.factorial(n)

    denominador += (lamb / mu) ** s / math.factorial(s) * (1 - lamb / (s * mu)) ** (-1)

    return 1 / denominador


# probabilidade de haver n pacientes no sistema
def pn(n, s, lamb, mu):
    if n <= s:
        cn = (lamb / mu) ** n / math.factorial(n)
    else:
        cn = (lamb / mu) ** n / (math.factorial(s) * s ** (n - s))

    p_0 = p0(s, lamb, mu)

    return cn * p_0


# numero esperado de pessoas na fila
def lq(s, lamb, mu):
    ro = rho(s, lamb, mu)
    p_0 = p0(s, lamb, mu)

    return (p_0 * ((lamb / mu) ** s) * ro) / (math.factorial(s) * (1 - ro) ** 2)


# numero esperado de pessoas no sistema
def l(s, lamb, mu):
    return lq(s, lamb, mu) + lamb / mu


# tempo esperado no sistema
def w(s, lamb, mu):
    return l(s, lamb, mu) / lamb


# tempo de espera na fila
def wq(s, lamb, mu):
    return lq(s, lamb, mu) / lamb


# probabilidade de que haja pelo menos z pacientes na fila
def pz(z, s, lamb, mu):
    soma = p0(s, lamb, mu)

    for i in range(1, z):
        soma += pn(i, s, lamb, mu)

    return 1 - soma


# probabilidade de que um paciente espere mais do que t minutos
def omega_q(t, s, lamb, mu):
    ro = rho(s, lamb, mu)
    soma = p0(s, lamb, mu)

    for a in range(1, s):
        soma += pn(a, s, lamb, mu)

    return (1 - soma) * math.exp(-s * mu * (1 - ro) * t)


# chama os metodos
def call_methods(objeto):
    s = objeto['s']
    lamb = objeto['lambda']
    mu = objeto['mu']

    output = dict(prob_ociosos=p0(s, lamb, mu),
                  numero_esperado_pessoas_fila=lq(s, lamb, mu),
                  numero_esperado_pessoas_sistema=l(s, lamb, mu),
                  tempo_espera_fila=wq(s, lamb, mu),
                  tempo_espera_sistema=w(s, lamb, mu),
                  fator_de_utilizacao=rho(s, lamb, mu))

    return json.dumps(round_dict(output), ensure_ascii=False)


# arrendonda os numeros de um dicionario
def round_dict(dic):
    for k, v in dic.items():
        dic[k] = round(v, 3)
    return dic
