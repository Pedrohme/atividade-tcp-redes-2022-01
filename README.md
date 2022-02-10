# Projeto Redes

<!-- ![GitHub repo size](https://img.shields.io/github/repo-size/repoOwner/repoName?style=for-the-badge&label=tamanho%20do%20repo&color=blueviolet)
![GitHub contributors](https://img.shields.io/github/contributors/repoOwner/repoName?style=for-the-badge&label=colaboradores&color=blueviolet)
![GitHub stars](https://img.shields.io/github/stars/repoOwner/repoName?style=for-the-badge&label=estrelas&color=blueviolet) -->

<br>


## 📜 Sobre o projeto  

Esse projeto trata-se de duas aplicações, um servidor e um cliente que utilizam sockets TCP para se comunicarem e realizar envios de arquivos entre eles.

<br />
<br />

## 🔨 Desenvolvido com

* [Python 3.9.7](https://www.python.org/)  
* [Node.js v16.13.2](https://nodejs.org/)  

<br />
<br />

## 💻 Pré-requisitos para executar os scripts localmente ou realizar o Build


* [Python 3.9.7](https://www.python.org/)
* [Node.js v16.13.2](https://nodejs.org/) 

<br />
<br />

## 🚀 Executando o projeto

Por padrão o servidor e o cliente utilizam a porta 8124 se comunicar. Isso pode ser configurado para o cliente e o servidor, respectivamente nos arquivos [cliente.py](./cliente/cliente.py) e [config.json](./servidor/src/config.json)
<br />

### 🔌 Executando com os arquivos executáveis  

Faça o download dos arquivos executáveis apropriados para sua plataforma em Releases e execute-os. Deve ser executado o servidor e o cliente separadamente, simultaneamente.  



<br />

### ⚙️ Executando localmente e realizando o Build

Certifique-se de que está com os pré-requisitos instalados.  

<br />

#### Cliente:

Navegue até o diretório [cliente/](./cliente/)  com a CLI de preferência.  
Para executar localmente, instale os pacotes requeridos com o comando  
`$ pip install -r requirements.txt`  

E então execute  `$ python gui.py` ou `$ python3 gui.py`  

Para realizar o build do programa para um arquivo executável de sua plataforma, instale os pacotes requeridos com o comando  
`$ pip install -r build_requirements.txt`  

E então execute  `$ python buid.py` ou `$ python3 build.py` 

O arquivo executável se encontrará em [cliente/dist](./cliente/).

<br />

#### Servidor:

Navegue até o diretório [servidor/](./servidor/)  com a CLI de preferência.  
Para executar localmente, instale os pacotes requeridos com o comando:  
`$ npm install --include=dev`  

E então execute:  
`$ npm start`  

Caso queira apenas transpilar o código typescript para javascript, execute o comando:  
`$ npx tsc`

Para realizar a compilação do programa para arquivos executáveis:  
`$ npm run build`

<br />
<br />

## 🤝 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/MathVolps">
        <img src="https://avatars.githubusercontent.com/u/50723951" width="100px;" alt="Foto do Matheus"/><br>
        <sub>
          <b>Matheus Volpon</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/matheusvvb-19">
        <img src="https://avatars.githubusercontent.com/u/84142397" width="100px;" alt="Foto do Matheus 2"/><br>
        <sub>
          <b>Matheus Volpon novamente</b>
          <br>
          <b>(Ele perdeu a conta principal)</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Pedrohme">
        <img src="https://avatars.githubusercontent.com/u/48974272" width="100px;" alt="Foto do Pedro"/><br>
        <sub>
          <b>Pedro Henrique Mendes</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/luccamapt">
        <img src="https://avatars.githubusercontent.com/u/62125928" width="100px;" alt="Foto do Lucca"/><br>
        <sub>
          <b>Lucca Marques</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

