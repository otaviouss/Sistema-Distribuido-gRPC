## Trocat

Para executar o programa, primeiro inicie seu ambiente virtual python

---

De forma mais simples, você pode executar os seguintes comandos:

``make init``

Para instalar os pacotes necessários.

``cd servidor``

``make server``

Para inicializar o servidor.

Em outro terminal, no diretório base:

``make client``

Para iniciar o cliente.

---

Outra opção, é não utilizar o makefile e seguir os seguintes passsos.

Instale as dependências listadas no arquivo requirements.txt utilizando o seguinte comando:

``pip3 install -r requirements.txt``

Após a instalação das dependências, execute o seguinte comando dentro da pasta servidor:

``prisma generate``

O objetivo desse comando é gerar a conexão com o banco por meio do prisma.

Em seguida, execute o seguinte comando:

``prisma py fetch``

Esse comando instala as dependências do prisma. Pode ser necessário rodar esse comando se o programa for executado um tempo depois de játer sido executado. Além disso, às vezes esse comando leva muito tempo para chegar aos 100% e pode ser cancelado nos 80% e ainda assim irá funcionar

Por fim, execute o servidor em um terminal usando:

``python3 servidor.py``

E em outro terminal, de dentro da pasta interface, execute o cliente:

``python3 main.py``

---

Observação: Algumas informações podem ser impressas no terminal tanto do servidor quanto do cliente, o que pode facilitar o entendimento do que está acontecendo no back-end do programa.
