# FUNÇÕES DE ESTIMATIVA DE EVAPOTRANSPIRAÇÃO
import numpy as np

def constante_psicrometrica(pressao):
  """ representado por gama

  recebe pressão ao nível do mar em KPa
  retorna constante (valor adimensional)
  """
  resultado = (0.665*0.001)*pressao
  return resultado


def pressao_de_saturacao_de_vapor(temp):
  """ representada por e_s é uma subfunção ou função auxiliar de pressao_media_de_saturacao_de_vapor.
  
  * Pressão atual de vapor (e_a):
    Está também pode ser calculada por esta fórmula substituindo temp por temperatura de ponto de orvalho

  recebe temp em C°
  retorna e° em KPa  
  """
  equacao_do_exponencial = (17.27*temp)/(temp+237.3)
  resultado = 0.6108*np.exp(equacao_do_exponencial)
  return resultado


def pressao_atual_de_vapor(temp, umidade_relativa):
  """ e_a
  """

  equacao_do_exponencial = (17.27*temp)/(temp+237.3)
  e_s = 0.6108*np.exp(equacao_do_exponencial)

  e_a = (e_s * umidade_relativa)/100

  return e_a


def deficit_de_saturacao(temp, umidade_relativa):
  """ representado por e_s - e_a. Depende da função pressao_de_vapor

  recebe temp_max e temp_min em C°
  retorna temperatura em C°
  """

  resultado = pressao_de_saturacao_de_vapor(temp) - pressao_atual_de_vapor(temp, umidade_relativa)
  return resultado


def declividade_da_curva_de_pressao_de_saturacao_de_vapor(temp):
  """ representado por delta

  recebe temperatura em C°
  retorna em KPa/C°
  """

  numerador = 4098*pressao_de_saturacao_de_vapor(temp)
  denominador = (temp+(237.3))**2
  resultado = numerador/denominador

  return resultado

def main(temp, umidade_relativa, pressao, U_2, Rn, Rho=1000, G=0, print_saidas:bool=False): #temp_max, temp_min
  """ função principal
  
  retorna em mm/dia
  """
  e_s = pressao_de_saturacao_de_vapor(temp) # apenas para print
  e_a = pressao_atual_de_vapor(temp, umidade_relativa) # apenas para print

  delta = declividade_da_curva_de_pressao_de_saturacao_de_vapor(temp)
  gama = constante_psicrometrica(pressao)
  deficit_de_saturacao_ = deficit_de_saturacao(temp, umidade_relativa) # e_s - e_a

  numerador = 0.408*delta*(Rn-G) + gama*(900/(temp+273))*U_2*(deficit_de_saturacao_)
  denominador = delta + gama*(1 + 0.34*U_2)

  saidas = f"""
  declividade da curva de pressao de saturacao de vapor delta : {delta}
  constante psicrometrica gama : {gama}
  pressão média de satturação de vapor e_s : {e_s}
  pressão de vapor e_a = {e_a}
  intensidade do vento u_2 = {U_2}
  
  """
  try:
    print(saidas) if print_saidas else None
  except:
    print('Erro ao printar as saídas. Tente acrescentar ou remover o método ".values" da dict "saidas" no código') if print_saidas else None 

  evap = numerador/denominador

  return evap