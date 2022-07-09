# ESTIMATIVA EVAPOTRANSPIRAÇÃO TCC

![texto](https://img.shields.io/static/v1?label=linguagem&message=Python&color=green&style=flat-square "linguagem")
![texto](https://img.shields.io/static/v1?label=ambiente&message=Python&color=orange&style=flat-square "ambiente")
![texto](https://img.shields.io/badge/status-operacional-success.svg "status")
![texto](https://img.shields.io/badge/plataforma-LINUX-lightgrey "status")


1. [Descrição do projeto](#descrição-do-projeto)  
2. [Funcionalidades](#funcionalidades)   
4. [Pré-requisitos](#pré-requisitos)  
5. [Como instalar](#como-instalar)
6. [Execução](#execucao)
7. [Desenvolvimento](#desenvolvimento)
8. [Como rodar](#como-rodar)
9. [I/O](#I/O)


## :scroll: Descrição do projeto

Este projeto, produto operacional do meu TCC, tem por objetivo gerar estimativas de evapotranspiração a partir de dados meteorológicos (dados pontuais ou de grade).


## :sparkles: Funcionalidades

:wrench:  Recortar dados grib2 e/ou Netcdf4 com base em shapefile ou pontos de latitude e longitude     
:wrench:  Tratar arquivos do modelo CAM3 e [ERA5](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means?tab=overview) para entrada no módulo de estimativa de evapotranspiração    
:wrench:  Estima evapotranspiração a partir dos dados de temperatura, umidade relativa, pressão, vento e radiação solar.         

## :warning: Pré-requisitos

- Python (obrigatório)


## :cd: Como instalar

```bash
# 1. no terminal, clone o projeto
git clone https://github.com/Ramonmurilo/ESTIMATIVA_EVAPOTRANSPIRACAO_TCC.git

# 2. entre na pasta do projeto
cd ESTIMATIVA_EVAPOTRANSPIRACAO_TCC

# 3. Reproduza o ambiente 
conda env create -n nome_qualquer -f env.yaml #ainda não implementado
```

## :arrow_forward: Execução

:fast_forward: Este trabalho de pesquisa foi executado 100% através do google colab, porém, nada impede de os scripts serem rodados localmente desde que tenha-se os dados disponíveis para acesso e análise. Seguem os links dos notebooks com códigos executados.   
  
:fast_forward: [Tratamento de variáveis e estimativa de evapotranspiração do CAM3](https://colab.research.google.com/drive/1BERQkL3sLNHpyoL_Yy-RZX5_PRxCtkjB?usp=sharing).  
:fast_forward: [Tratamento de variáveis e estimativa de evapotranspiração ERA5](https://colab.research.google.com/drive/1omqHkYAqNb0Kr-RBi8xStjG7is8tFPJ9?usp=sharing).  
:fast_forward: [Análise e tratamento de resultados](https://colab.research.google.com/drive/1yoSGNqF3VuYB_KiajLH5llHCrwtE7Qd5?usp=sharing).  


## :construction: Desenvolvimento

:dart: ...

## :rotating_light: Como rodar

Prepara os dados necessários para a estimativa e chame-os no módulo de cálculo:
```bash
from src import calcula_evapotranspiracao

evp = calcula_evapotranspiracao.main(valor_temperatura,
                                     valor_umidade_relativa, 
                                     valor_pressao,
                                     valor_vento,
                                     valor_radiacao,
                                     Rho=1000,              # opcional
                                     G=0,                   # opcional
                                     print_saidas=False)

```  

## :green_apple: I/O

Os Inputs/entradas ...   
Os outputs/saídas vão para ...


