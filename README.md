# E.L.A. Backend - Servidor de Segurança Pessoal

![Logo do Projeto](https://via.placeholder.com/600x200.png/4a1d35/f5d5e2?text=E.L.A.+%E2%80%A2+Backend)

O **E.L.A. Backend** é o servidor central da plataforma de segurança pessoal E.L.A. (Emergency Location Alert), desenvolvido em Flask para a Hackathon CPBR25. Ele é responsável por processar alertas de emergência, gerenciar dados de usuários, notificar contatos e fornecer páginas de rastreamento em tempo real.

---

## 🏗️ Arquitetura do Projeto

Este repositório contém **apenas o backend** da solução E.L.A. Ele se comunica tanto com o aplicativo de interface do usuário quanto com o aplicativo que roda em segundo plano.

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   E.L.A.        │    │   E.L.A.         │    │   E.L.A.        │
│   Background    │◄───┤   Backend        │───►│   Frontend      │
│   (Flutter)     │    │   (Este Projeto) │    │   (Kotlin)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       ▲                       │
         │                       │                       │
         ▼                       │                       ▼
   Acionamento NFC         ✅ Processamento          Interface de
   Envio de Coordenadas    ✅ Notificação SMS         Cadastro
                           ✅ Rastreamento em         Gerenciamento
                              Tempo Real              de Contatos
                           ✅ Mapa de Calor           Histórico
```

- **[E.L.A. Background (Flutter)](https://github.com/CodeByDouglas/CodeByDouglas-Hackthon-CPBR25-mulheres-seguras-App-Background )**: App que monitora a tag NFC e envia os dados de localização.
- **[E.L.A. Frontend (Kotlin)](https://github.com/EduFrancaDev/Projeto-ELA)**: App principal para cadastro de perfil, contatos e visualização do histórico.

---

## 🚀 Funcionalidades do Backend

-   **API RESTful Robusta**: Endpoints para gerenciar usuários, contatos e chamados de emergência.
-   **Notificações Automáticas via SMS**: Integração com Twilio para enviar alertas instantâneos para contatos de segurança.
-   **Geração de Páginas de Rastreamento**: Cria URLs únicas e seguras para visualização da localização da usuária em tempo real.
-   **Mapa de Calor de Incidentes**: Endpoint que agrega todos os dados de chamados para gerar um mapa de calor, identificando áreas de risco.
-   **Gerenciamento de Banco de Dados**: Persistência de dados de usuários, contatos, chamados e rotas com SQLite.
-   **Scripts de Seed**: Facilita a criação de dados de teste para desenvolvimento e demonstração.

---

## 🛠️ Tecnologias Utilizadas

-   **Backend**: Flask (Python)
-   **Banco de Dados**: SQLite (com Flask-SQLAlchemy)
-   **Notificações**: Twilio (para envio de SMS)
-   **Frontend (Páginas Web)**: HTML, CSS, JavaScript
-   **Mapas**: Leaflet.js (com plugin Leaflet.heat)
-   **Ambiente**: Python 3, venv

---

## 📂 Estrutura do Projeto

```
/
├── app/                  # Contém o core da aplicação Flask
│   ├── models/           # Modelos do banco de dados (SQLAlchemy)
│   ├── routes/           # Definição das rotas e endpoints
│   ├── services/         # Lógica de serviços (e.g., Twilio)
│   ├── static/           # Arquivos estáticos (CSS, JS, Imagens)
│   └── templates/        # Templates HTML (Jinja2)
├── docs/                 # Documentação do projeto (API, etc.)
├── instance/             # Arquivos de instância (banco de dados .db)
├── scripts/              # Scripts de utilidade (e.g., popular o banco)
└── requirements.txt      # Dependências do projeto
```

---

## ⚙️ Guia de Instalação e Configuração

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Pré-requisitos
-   Python 3.10+
-   `pip` e `venv`

### 2. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/Hackthon-CPBR25-mulheres-seguras.git
cd Hackthon-CPBR25-mulheres-seguras
```

### 3. Crie e Ative o Ambiente Virtual
```bash
# Para Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Para Windows
python -m venv .venv
.venv\Scripts\activate
```

### 4. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 5. Configure as Variáveis de Ambiente (Twilio)
Crie um arquivo chamado `.env` na raiz do projeto e adicione suas credenciais do Twilio:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+15551234567
```

---

## ▶️ Como Usar

### 1. Popule o Banco de Dados (Opcional)
Para ter dados de exemplo (usuários e chamados em Brasília para o mapa de calor), execute o script de seed:

```bash
# Limpa o banco, cria um usuário de teste e popula o heatmap
PYTHONPATH=. python3 scripts/seed.py --all
```
*Use `python3 scripts/seed.py --help` para ver outras opções (`--clear`, `--heatmap`).*

### 2. Inicie o Servidor Flask
Com o ambiente virtual ativado, execute:
```bash
flask run
```
O servidor estará disponível em `http://127.0.0.1:5000`.

### 3. Acesse as Páginas
-   **Mapa de Calor**: `http://127.0.0.1:5000/emergency/heatmap`
-   **Rastreamento (Exemplo)**: Acione o endpoint `/emergency/nfc/auto/TOKEN_TESTE_123` para criar um chamado e use o link que seria enviado por SMS.

---

## 📖 Documentação da API

A documentação detalhada dos endpoints, incluindo exemplos de requisição e resposta, está disponível em:

-   **[Guia de Integração dos Endpoints de Emergência](./docs/endpoints_integracao.md)**
-   **[Guia de Endpoints de Rastreamento](./docs/endpoints_tracking.md)**






**Desenvolvido com ❤️ para promover a segurança para mulheres**

*Projeto desenvolvido durante o Hackathon CPBR25 - Mulheres Seguras*

