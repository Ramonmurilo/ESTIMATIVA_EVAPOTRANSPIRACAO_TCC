##################################
#### PREPARAÇÃO DE VARIÁVEIS #####
##################################
"""
    Este bloco de código prepara as variáveis para o cálculo da estimativa de evapotranspiração. Os passos são:
    Geral:
          - seleciona nivel mais próximo a superfície

    Para cada variável:
          - Seleciona a variável e recorta com base em um shapefile (feito em um único passo)
          - converte para a unidade da fórmula (se necessário)
          - faz a média dos valores na área 
"""

import xarray as xr
from src import recorta_dado_meteorologico
from src import calcula_evapotranspiracao

class estimativa_from_cam3():
    """Classe para trabalhar vazões previstas pelo SMAP
        Função principal é gerar vazão por semana operativa para todos os postos
    """
       
    def __init__(self, arquivo_cam3:str, geometria_shp:str) -> None:
        """
        Args:
            deck_saida (str): caminho até a pasta raiz com as bacias do smap
            arquivo_RAH (str): arquivo excel de vazões RAH do ONS
        Attributes:
            deck (str): retorna o argumento deck_saida
            RAH (str): retorna o argumento arquivo_RAH
        """
        nc_cam = xr.open_dataset(arquivo_cam3, decode_times=False)
        # este passo é necessário apenas por uma particularidade do CAM
        self.nc_cam = xr.decode_cf(nc_cam, use_cftime=True)

        self.geometria_shp = geometria_shp
        return None


    def intensidade_do_vento(self, u, v):
        """Intensidade do vento em m/s
        Args:
            u (_type_): Componente U do vento
            v (_type_): Componente V do vento
        Returns:
            DataSet: intensidade do vento calculado por ponto de grade
        """
        intensidade = (u ** 2 + v ** 2) ** 0.5

        return intensidade 
    
    def horas_de_sol(self, mes:int):
        horas_de_sol = {
            1:13,
            2:12,
            3:12,
            4:11,
            5:10,
            6:10,
            7:10,
            8:11,
            9:11,
            10:12,
            11:13,
            12:13
        }

        return horas_de_sol[mes]


    def prepara_cam3(self, mes_referencia:int):
        ################################## SELECIONA OS DADOS NO NÍVEL DE SUPERFÍCIE
        dados_cam_nivel_superficie = self.nc_cam.sel(lev=1000, method='nearest')


        ################################## TEMPERATURA
        # recorte de variáveis
        cam_temperatura_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.T, 
                                                        contorno_tipo='shapefile', 
                                                        xdim='lon',
                                                        ydim='lat',
                                                        dado_contorno=self.geometria_shp )
        # conversão de Kelvin para Celsius
        temp = cam_temperatura_recortado - 273.15 
        # Média dos valores na área
        self.temp_mean = temp.mean()


        ################################## UMIDADE RELATIVA
        # recorte de variáveis
        cam_umidade_relativa_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.RELHUM, 
                                                                        contorno_tipo='shapefile', 
                                                                        xdim='lon',
                                                                        ydim='lat',  
                                                                        dado_contorno=self.geometria_shp )
        # VERSÃO ATUAL: sem conversão
        # VERSÃO OLD: conversão do valor de umidade relativa em percentual de 0 a 100 para 0 a 1
        umidade_relativa = cam_umidade_relativa_recortado
        # média dos valores na área
        self.umidade_relativa_mean = umidade_relativa.mean()


        ################################## PRESSÃO
        #converte pressão de Pa para KPa
        cam_pressao_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.PSL, 
                                                        contorno_tipo='shapefile', 
                                                        xdim='lon',
                                                        ydim='lat',  
                                                        dado_contorno=self.geometria_shp )
        pressao = cam_pressao_recortado/1000 
        self.pressao_mean = pressao.mean()


        ################################## VENTO
        cam_ventou_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.U, 
                                                        contorno_tipo='shapefile', 
                                                        xdim='lon',
                                                        ydim='lat', 
                                                        dado_contorno=self.geometria_shp )

        cam_ventov_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.V, 
                                                        contorno_tipo='shapefile', 
                                                        xdim='lon',
                                                        ydim='lat', 
                                                        dado_contorno=self.geometria_shp )
        u_2 = self.intensidade_do_vento(cam_ventou_recortado, cam_ventov_recortado)
        self.u_2_mean = u_2.mean() 


        ################################## RADIAÇÃO SOLAR LÍQUIDA
        # conversão de W/m² para MJ/m²*dia
        cam_radiacao_solar_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.FSDS, 
                                                        contorno_tipo='shapefile', 
                                                        xdim='lon',
                                                        ydim='lat', 
                                                        dado_contorno=self.geometria_shp )
        valor_horas_de_sol = self.horas_de_sol(mes_referencia)
        #Rn = cam_radiacao_solar_recortado*valor_horas_de_sol*3600/1000000
        Rn = cam_radiacao_solar_recortado*24*3600/1000000
        self.Rn_mean = Rn.mean()

        return self.temp_mean, self.umidade_relativa_mean, self.pressao_mean, self.u_2_mean, self.Rn_mean


    def prepara_cam3_opcao2(self, mes_referencia:int):
        ################################## SELECIONA OS DADOS NO NÍVEL DE SUPERFÍCIE
        dados_cam_nivel_superficie = self.nc_cam.sel(lev=1000, method='nearest')


        ################################## TEMPERATURA
        # recorte de variáveis
        cam_temperatura_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.T, 
                                                        contorno_tipo='shapefile', 
                                                        xdim='lon',
                                                        ydim='lat',
                                                        dado_contorno=[self.geometria_shp] )
        # conversão de Kelvin para Celsius
        temp = cam_temperatura_recortado - 273.15 
        # Média dos valores na área
        self.temp_mean = temp.mean()


        ################################## UMIDADE RELATIVA
        # recorte de variáveis
        cam_umidade_relativa_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.RELHUM, 
                                                                        contorno_tipo='shapefile', 
                                                                        xdim='lon',
                                                                        ydim='lat',  
                                                                        dado_contorno=[self.geometria_shp] )
        # VERSÃO ATUAL: sem conversão
        # VERSÃO OLD: conversão do valor de umidade relativa em percentual de 0 a 100 para 0 a 1
        umidade_relativa = cam_umidade_relativa_recortado
        # média dos valores na área
        self.umidade_relativa_mean = umidade_relativa.mean()


        ################################## PRESSÃO
        #converte pressão de Pa para KPa
        cam_pressao_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.PSL, 
                                                        contorno_tipo='shapefile', 
                                                        xdim='lon',
                                                        ydim='lat',  
                                                        dado_contorno=[self.geometria_shp] )
        pressao = cam_pressao_recortado/1000 
        self.pressao_mean = pressao.mean()


        ################################## VENTO
        cam_ventou_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.U, 
                                                        contorno_tipo='shapefile', 
                                                        xdim='lon',
                                                        ydim='lat', 
                                                        dado_contorno=[self.geometria_shp] )

        cam_ventov_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.V, 
                                                        contorno_tipo='shapefile', 
                                                        xdim='lon',
                                                        ydim='lat', 
                                                        dado_contorno=[self.geometria_shp] )
        u_2 = self.intensidade_do_vento(cam_ventou_recortado, cam_ventov_recortado)
        self.u_2_mean = u_2.mean() 


        ################################## RADIAÇÃO SOLAR LÍQUIDA
        # conversão de W/m² para MJ/m²*dia
        cam_radiacao_solar_recortado = recorta_dado_meteorologico.main(dados=dados_cam_nivel_superficie.FSDS, 
                                                        contorno_tipo='shapefile', 
                                                        xdim='lon',
                                                        ydim='lat', 
                                                        dado_contorno=[self.geometria_shp] )
        valor_horas_de_sol = self.horas_de_sol(mes_referencia)
        #Rn = cam_radiacao_solar_recortado*valor_horas_de_sol*3600/1000000
        Rn = cam_radiacao_solar_recortado*24*3600/1000000
        self.Rn_mean = Rn.mean()

        return self.temp_mean, self.umidade_relativa_mean, self.pressao_mean, self.u_2_mean, self.Rn_mean



    def estima_evapotranspiracao(self, print_saidas=False, Rho=1000, G=0):

        resultado_por_bacia = calcula_evapotranspiracao.main(self.temp_mean, self.umidade_relativa_mean, 
                                                            self.pressao_mean, self.u_2_mean, self.Rn_mean,
                                                            Rho, G, print_saidas)

        return resultado_por_bacia