🌐 Sistema Web de Monitoramento de LED com Arduino + Flask
📌 Descrição

Este projeto educacional tem como objetivo demonstrar a integração entre sistemas embarcados (Arduino) e aplicações web utilizando Python e Flask.

A aplicação permite controlar um LED conectado ao Arduino através de uma interface web, além de registrar e armazenar eventos (liga/desliga) com data e hora em um banco de dados SQLite.

O sistema funciona como uma ponte entre o mundo físico (hardware) e o mundo digital (web), utilizando comunicação serial.

🎯 Objetivo Educacional
Compreender comunicação serial entre Arduino e computador
Desenvolver APIs com Flask
Trabalhar com banco de dados SQLite
Implementar persistência de dados (logs)
Criar sistemas web integrados com hardware
Aplicar conceitos de backend e tempo real
⚙️ Funcionalidades
🔌 Conexão e desconexão com Arduino via porta serial
💡 Controle remoto do LED (ligar/desligar via navegador)
🕒 Atualização automática da data e hora no Arduino
📊 Registro de eventos com data/hora em banco de dados
📜 Listagem dos últimos registros na interface web
🔄 Atualização de status em tempo real
🛠️ Tecnologias Utilizadas
Python
Flask
SQLite
PySerial
HTML (template web)
Arduino (integração serial)
🧱 Arquitetura do Sistema

O sistema é dividido em três partes principais:

1️⃣ Arduino (Hardware)
Controla o LED
Envia mensagens com status e data/hora
Recebe comandos via serial
2️⃣ Backend (Python + Flask)
Gerencia comunicação serial
Processa comandos
Salva registros no banco SQLite
Disponibiliza rotas HTTP (API)
3️⃣ Interface Web
Exibe status da conexão
Permite controle do LED
Mostra histórico de eventos
💻 Como Funciona
🔁 Comunicação Serial

O sistema escuta continuamente a porta serial:

Recebe mensagens do Arduino
Processa os dados
Armazena no banco

Exemplo de mensagem esperada:

LED Ligado 02/12/2025 16:30:10
🌐 Rotas da Aplicação
Rota	Método	Função
/	GET	Página principal
/conectar	POST	Conecta ao Arduino
/desconectar	POST	Desconecta
/ligar	GET/POST	Liga o LED
/desligar	POST	Desliga o LED
/atualiza_datahora	POST	Atualiza data/hora no Arduino
/status	GET	Retorna status e registros
🗄️ Banco de Dados

Tabela: led_inteligente

Campo	Tipo	Descrição
id	INTEGER	Identificador
descricao	TEXT	Ação (LED Ligado/Desligado)
data_hora	TEXT	Data e hora do evento
status	TEXT	Estado do LED
▶️ Como Executar
1️⃣ Instalar dependências
pip install flask pyserial
2️⃣ Configurar porta serial

No código:

PORTA = "COM7"

📌 Ajuste conforme seu sistema:

Windows: COM3, COM4, etc.
Linux: /dev/ttyUSB0
Mac: /dev/tty.usbserial
3️⃣ Executar aplicação
python app.py

Acesse no navegador:

http://localhost:5000
📊 Exemplo de Fluxo
Usuário acessa a interface web
Conecta ao Arduino
Clica em “Ligar LED”
Comando é enviado via serial
Arduino responde com status + data/hora
Sistema salva no banco
Interface atualiza os registros
🎓 Contexto Educacional

Este projeto foi desenvolvido como uma atividade prática para alunos de cursos técnicos, com foco na integração entre:

Programação backend
Sistemas embarcados
Banco de dados
Comunicação entre sistemas

A proposta é proporcionar uma visão completa de como sistemas reais funcionam, conectando hardware e software.
