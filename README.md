
# Algoritmo Genético para o Problema das 8-Rainhas em Tabuleiro N x N

## **Visão Geral**

Este projeto implementa um **Algoritmo Genético (AG)** para resolver o clássico **Problema das 8-Rainhas** em tabuleiros de diferentes tamanhos (NxN). O objetivo é posicionar 8 rainhas em um tabuleiro NxN de forma que nenhuma rainha possa atacar outra, respeitando as regras de movimento das rainhas no xadrez. O aplicativo possui uma interface gráfica intuitiva desenvolvida com **Tkinter**, permitindo que usuários configurem os parâmetros do algoritmo, visualizem o progresso e obtenham soluções animadas.

## **Características Principais**

- **Seleção Estratégica:** Combinação eficiente dos métodos de **Seleção por Torneio** e **Seleção por Roleta** para escolher os melhores indivíduos da população.
- **Crossover Adaptado:** Implementação de crossover específico para 8 genes, garantindo a recombinação eficaz das soluções.
- **Mutação Inteligente:** Aplicação de mutações por troca de genes para introduzir diversidade genética e evitar a convergência prematura.
- **Visualização Gráfica:** Monitoramento em tempo real do progresso do algoritmo através de gráficos dinâmicos que mostram a evolução dos conflitos.
- **Animação das Soluções:** Animação das rainhas movendo-se suavemente para suas posições finais quando uma solução válida é encontrada.
- **Verificação de Validade:** Validação automática das soluções para garantir que nenhuma rainha está em posição de ataque, proporcionando confiança nos resultados obtidos.
- **Interface Intuitiva:** Design amigável e responsivo, facilitando a interação e configuração dos parâmetros do algoritmo.

## **Requisitos**

Antes de iniciar, certifique-se de que você possui os seguintes requisitos instalados em seu sistema:

- **Python 3.7 ou Superior**
- **Bibliotecas Python:**
  - `tkinter` (geralmente incluído com Python no Windows)
  - `matplotlib`
  - `numpy` *(se utilizado no projeto)*
- **PyInstaller** (para gerar o executável)

## **Instalação**

### **1. Clone o Repositório**

Primeiro, clone o repositório do projeto para o seu computador:

```bash
git clone https://github.com/seu-usuario/8-rainhas-genetico.git
cd 8-rainhas-genetico
```

### **2. Configurar um Ambiente Virtual** (Opcional, mas Recomendado)
Usar um ambiente virtual ajuda a isolar as dependências do projeto.

```bash
python -m venv venv
```
Ative o ambiente virtual:

- Windows:
    ```bash
    venv\Scripts\activate
    ```
- macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

### **3. Instalar as Dependências**
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install --upgrade pip
pip install matplotlib numpy
```

**Nota:** O Tkinter geralmente já vem instalado com o Python no Windows. Se você encontrar erros relacionados ao Tkinter, pode ser necessário instalá-lo separadamente conforme a documentação do seu sistema operacional.

### **4. Verificar a Estrutura do Projeto**
Certifique-se de que o diretório do projeto contém os seguintes arquivos:

```
8_rainhas_genetico/
├── genetic_algorithm.py
├── helpers.py
└── main.py
```

## **Uso**

### **1. Executar o Programa**
Para iniciar o aplicativo, execute o seguinte comando no terminal dentro do diretório do projeto:

```bash
python main.py
```

### **2. Configurar Parâmetros**
Na interface gráfica, você poderá ajustar os seguintes parâmetros:

- **Tamanho do Tabuleiro (N):** Define o tamanho do tabuleiro NxN (mínimo 8).
- **Tamanho da População:** Número de indivíduos na população inicial.
- **Probabilidade de Mutação:** Chance de alterar genes durante a mutação.
- **Probabilidade de Crossover:** Chance de combinar genes entre pais.
- **Número de Gerações:** Máximo de iterações do algoritmo.
- **Elite Size:** Número de melhores indivíduos preservados a cada geração.

### **3. Iniciar o Algoritmo**
Após configurar os parâmetros desejados, clique no botão "Iniciar Algoritmo" para executar o Algoritmo Genético. O progresso será exibido através de gráficos dinâmicos e animações das rainhas.

### **4. Visualizar Resultados**
- **Gráfico de Progresso:** Mostra a evolução do número de conflitos ao longo das gerações.
- **Animação das Rainhas:** Demonstração visual das rainhas se posicionando em suas posições finais.
- **Console de Solução:** Exibe detalhes das gerações e a disposição final das rainhas.

### **5. Tratamento de Falhas**
Caso o algoritmo não encontre uma solução válida com os parâmetros fornecidos, o programa notificará o usuário com uma mensagem de aviso e listará as rainhas em conflito. Nesse caso, considere ajustar os parâmetros e tentar novamente.

## **Gerar Executável para Windows**

Para distribuir o aplicativo sem a necessidade de instalar Python e dependências, você pode gerar um executável do Windows utilizando o PyInstaller.

### **1. Instalar o PyInstaller**
Caso ainda não tenha o PyInstaller instalado, instale-o via pip:

```bash
pip install pyinstaller
```

### **2. Criar o Executável**
Execute o seguinte comando no terminal dentro do diretório do projeto:

```bash
python -m PyInstaller --onefile --windowed main.py
```

Explicação das Opções:

- `--onefile`: Cria um único arquivo executável.
- `--windowed` ou `-w`: Evita que uma janela de console apareça ao executar o aplicativo (ideal para aplicativos GUI).

### **3. Localizar o Executável**
Após a conclusão do processo, o executável será gerado na pasta `dist`:

```
8_rainhas_genetico/
├── build/
├── dist/
│   └── main.exe
├── main.spec
├── genetic_algorithm.py
├── helpers.py
└── main.py
```

### **4. Executar o Aplicativo**
Navegue até a pasta `dist` e execute `main.exe` para iniciar o aplicativo sem necessidade de ambiente Python.
