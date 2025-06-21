# E.L.A. - Projeto Mulheres Seguras

![Logo do Projeto](https://via.placeholder.com/600x200.png/4a1d35/f5d5e2?text=E.L.A.+%E2%80%A2+Mulheres+Seguras)

**E.L.A.** (Emergency Location Alert) é uma plataforma de segurança pessoal desenvolvida para a Hackathon CPBR25, com o objetivo de oferecer uma ferramenta rápida e eficaz para que mulheres em situação de perigo possam pedir ajuda.

Através de um dispositivo NFC (como um adesivo ou chaveiro), a usuária pode acionar um alerta de emergência de forma discreta, notificando seus contatos de confiança e compartilhando sua localização em tempo real.

---

## 🚀 Funcionalidades Principais

-   **Alerta Rápido via NFC**: Acione um chamado de emergência simplesmente aproximando o celular de um dispositivo NFC.
-   **Notificações Automáticas por SMS**: Contatos de segurança pré-cadastrados recebem um SMS instantâneo com um link para rastreamento.
-   **Rastreamento em Tempo Real**: Uma página web segura exibe a rota da usuária em um mapa, atualizada continuamente.
-   **Mapa de Calor de Incidentes**: Visualize um mapa de calor que mostra as áreas com maior frequência de chamados, ajudando a identificar zonas de risco.
-   **API Robusta**: Endpoints REST bem documentados que permitem a integração com diferentes clientes (e.g., aplicativo Android).
-   **Gerenciamento de Contatos**: Usuárias podem adicionar e remover seus contatos de emergência.

---

## 🛠️ Tecnologias Utilizadas

-   **Backend**: Flask (Python)
-   **Banco de Dados**: SQLite (com Flask-SQLAlchemy)
-   **Notificações**: Twilio (para envio de SMS)
-   **Frontend**: HTML, CSS, JavaScript
-   **Mapas**: Leaflet.js (com plugins Leaflet.heat)
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
├── docs/                 # Documentação do projeto
├── instance/             # Arquivos de instância (banco de dados)
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
*Use `python3 scripts/seed.py --help` para ver outras opções.*

### 2. Inicie o Servidor Flask
Com o ambiente virtual ativado, execute:
```bash
flask run
```
O servidor estará disponível em `http://127.0.0.1:5000`.

### 3. Acesse as Páginas
-   **Mapa de Calor**: `http://127.0.0.1:5000/emergency/heatmap`
-   **Rastreamento (Exemplo)**: Use o endpoint de criação de chamado (`/emergency/nfc/auto/<token>`) e acesse o link de rastreamento gerado.

---

##  документи API

A documentação detalhada dos endpoints, incluindo exemplos de requisição e resposta, está disponível em:

-   **[Guia de Integração dos Endpoints de Emergência](./docs/endpoints_integracao.md)**

---

