# Sistema para redução de congestionamentos

## Siga as intruções para a instalação do projeto ao rodar pela primeira vez.

### Rodando os Algoritmos
Os algoritmos foram preparados para rodar nas instâncias requeridas. Para rodá-los execute o próprio arquivo do algoritmo, passando os argumentos necessários.

Obs: Para saber os argumentos de cada algoritmo basta rodar o arquivo do mesmo seguido de `--help`

Exemplo: `python algoritm_local_search,py --help`.

As instâncias estarão contidas dentro de `data/`

### Exemplos de uso
```python algoritm_local_search.py --ist sioux_falls/siouxFalls.json --bd 20 --it 3 --st 2```

## Instalação do projeto

1. Crie um ambiente virtual

```Bash
python -m venv .venv
```

2. Ative o ambiente virtual

Windows
```Bash
.venv\Scripts\activate
```
No Linux/Mac (Bash):
```Bash
source .venv/bin/activate
```

Instale as dependências do projeto
```Bash
pip install -r requirements.txt

```

### Atualizar o arquivo requirements.txt
´pip freeze > requirements.txt´

## Instalação do simulador

### Instalando o SUMO no Windows

1.  Faça o download do instalador mais recente do SUMO no site oficial: <https://sumo.dlr.de/docs/Downloads.php>.

2.  Execute o instalador baixado e siga as instruções na tela para concluir a instalação. Certifique-se de selecionar todas as opções de instalação relevantes para o seu projeto.

3.  Depois de concluir a instalação, defina a variável de ambiente SUMO\_HOME apontando para a pasta de instalação do SUMO. Para fazer isso, clique com o botão direito do mouse em "Meu computador" e selecione "Propriedades". Em seguida, clique em "Configurações avançadas do sistema" e selecione "Variáveis de ambiente". Em "Variáveis do sistema", clique em "Novo" e defina a variável de ambiente SUMO\_HOME com o valor do caminho da pasta de instalação do SUMO.

4.  Para testar se a instalação foi bem sucedida, abra o prompt de comando e digite "sumo-gui". Se o SUMO GUI for aberto, a instalação foi bem sucedida.

### Instalando o SUMO no MacOs

1.  Abra o terminal e instale o Homebrew, um gerenciador de pacotes para o MacOs. Para instalar o Homebrew, execute o seguinte comando no terminal:

```Bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

1.  Depois de instalar o Homebrew, use-o para instalar o SUMO. Para fazer isso, execute o seguinte comando no terminal:

```Bash
brew install sumo
```

1.  Depois de concluir a instalação, defina a variável de ambiente SUMO\_HOME apontando para a pasta de instalação do SUMO. Para fazer isso, abra o terminal e execute o seguinte comando:

```Bash
echo 'export SUMO_HOME="/usr/local/Cellar/sumo/{versão_do_sumo}/share/sumo"' >> ~/.bash_profile
source ~/.bash_profile
```

1.  Certifique-se de substituir {versão\_do\_sumo} pelo número da versão do SUMO que você instalou.

2.  Para testar se a instalação foi bem sucedida, abra o terminal e digite "sumo-gui". Se o SUMO GUI for aberto, a instalação foi bem sucedida.

### Passos iniciais.
O SUMO assim como os algoritmos, nmecessitam que as instâncias estejam preparadas para os mesmos. Para isso, antes de rodar pela primeira vez o projeto, rode o arquivo `init.config.py` Ele irá gerar as instâncias iniciais, e deixará tudo configurado para que seja possível executar os algoritmos em si.


