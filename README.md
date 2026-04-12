# N8N PYTHON SALES AUTOMATION

Automação inteligente de vendas com Python + IA + N8N
----

# Visão geral do projeto

O n8n Python Sales Automation é uma solução em desenvolvimento contínuo que automatiza a análise de dados de vendas utilizando Python, n8n e inteligência artificial.

A aplicação já é capaz de coletar dados via API, processá-los e gerar insights estratégicos automaticamente, enviando os resultados para o Telegram.

O projeto segue em evolução, com foco em melhorias de arquitetura, segurança e experiência do usuário, visando se tornar uma solução cada vez mais robusta e escalável.

----

# Fluxo no n8n
<p align="center">
  <img src="images/fluxo-n8n.png" width="500"/>
</p>

# Estruturação dos dados
<p align="center">
  <img src="images/backend-python.png" width="500"/>
</p>

# Resultado da Análise via Telegram
<p align="center">
  <img src="images/report-telegram.png" width="500"/>
</p>


# Objetivos

Pequenos negócios frequentemente possuem dados de vendas, mas não conseguem extrair valor estratégico deles.

Este projeto tem como objetivo a resolução desse problema ao:

* Transformar dados brutos em insights acionáveis
* Automatizar análises que seriam feitas manualmente
* Reduzir o tempo de tomada de decisão
* Apoiar o aumento de faturamento com base em dados

----

# Arquitetura da solução

Fluxo da aplicação:

1.API em Python (Flask) disponibiliza dados de vendas via endpoint protegido

2.n8n consome os dados via HTTP Request

3.Node em JavaScript estrutura os dados e gera prompts inteligentes

4.OpenAI processa os dados e gera análises estratégicas

5.Resultado é enviado automaticamente para o Telegram

----

# Tecnologias Utilizadas

* Python
* Flask
* API REST
* n8n
* JavaScript
* OpenAI API
* Telegram Bot API
-----

# Segurança

A API implementa autenticação via API Key para proteger o endpoint de vendas.

Boas práticas aplicadas:

* Proteção de rota com verificação de header
* Separação de responsabilidades
* Planejamento de uso de variáveis de ambiente (.env)

Evoluções planejadas:

* Implementação de .env
* Autenticação via JWT
* Logs de acesso

-----

# Funcionalidades
  
* 📈 Análise automatizada de vendas
* 🧠 Geração de insights com IA
* 📦 Agrupamento por categoria
* 💰 Cálculo de receita total
* 🔍 Identificação de padrões e tendências
* 📩 Envio automático de relatórios para Telegram
* 🔐 Proteção de endpoint com API Key

---------

# Evoluções Planejadas

* Refatoração completa para Programação Orientada a Objetos (POO)
* Criação de dashboard front-end
* Visualização gráfica de dados
* Deploy em nuvem
* Transformação em produto SaaS

----
 
# Diferencial do Projeto

Este projeto se destaca por integrar:

* Automação de workflows
* Análise de dados
* Inteligência artificial

Gerando valor real para negócios de forma automatizada.

----

## 🤝 Vamos nos conectar

- LinkedIn: https://www.linkedin.com/in/artemis-costa/
- Email: artemiscomoura@hotmail.com
