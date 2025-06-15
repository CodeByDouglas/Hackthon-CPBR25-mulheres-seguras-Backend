# Documento de Requisitos de Produto (PRD) – Backend de Segurança Pessoal para Mulheres

## Resumo do Projeto

Pesquisas recentes indicam que a violência contra a mulher é alarmante: 21,4 milhões de brasileiras sofreram algum tipo de agressão no último ano. Diante disso, propõe-se desenvolver um backend para um app Android de segurança pessoal.

Ao acionar uma tag NFC única vinculada à usuária, o aplicativo Android faz uma requisição GET ao servidor, que abre uma página web de confirmação de alerta. Se a usuária não cancelar em até 5 minutos, o sistema confirma automaticamente o chamado e envia mensagens SMS para todos os contatos de emergência cadastrados, com o link para acessar a página de tracking. Uma interface web (renderizada via Flask) exibe os dados da usuária e um mapa ao vivo com rastreamento, recebendo atualizações contínuas de localização. A usuária também pode encerrar manualmente o chamado via app.

## Funcionalidades Principais

* **Cadastro de Usuário**: API para criar perfil com dados pessoais (nome, CPF, e-mail, senha e foto).
* **Cadastro e gestão de Contatos de Emergência**: Registro de múltiplos contatos (nome, telefone, e-mail) vinculados ao usuário (relação 1\:N).
* **Token NFC único por usuária**: Geração de identificador NFC exclusivo (string) associado ao perfil da usuária.
* **Abertura de chamado via NFC**: `GET /emergency/nfc/<token>` invocado quando o dispositivo lê a tag; retorna dados para exibição de tela de confirmação.
* **Confirmação automática e SMS**: Se não houver cancelamento em 5 minutos, envia SMS de emergência para todos os contatos cadastrados com localização atual e mensagem pré-definida.
* **Página web de monitoramento**: Frontend em HTML (templates Flask) exibindo informações da usuária e mapa de rastreamento em tempo real via endpoint `/location`.
* **Finalização manual de chamado**: `POST /emergency/close` permite que a usuária autenticada encerre um chamado ativo.

## Funcionalidades Secundárias (opcionais)

* **Abertura offline via SMS**: Processamento de SMS recebidos contendo token e localização para abertura de chamados sem internet.
* **Envio de alerta por e-mail**: Notificação adicional via e-mail com link para mapa e detalhes do alerta.
* **Envio de alerta por WhatsApp**: Integração com API do WhatsApp (via Twilio) para envio de mensagens de emergência.

## Tecnologias Utilizadas

* **Flask 3.1.1 & Python 3.12.3**: Serviço REST leve e popular em Python.
* **SQLite**: Banco relacional embutido para usuários, contatos e chamados.
* **ngrok**: Exposição do servidor de desenvolvimento na internet para testes de integração.
* **Twilio**: Plataforma para envio de SMS, e-mail e WhatsApp.
* **Android (Kotlin)**: Cliente móvel que lê NFC, faz requisições REST e envia localização.
* **Frontend Web (Flask/Jinja2)**: Templates HTML dinâmicos exibindo mapa e dados de rastreamento.

## Modelo do Banco de Dados

* **User**: `id` (PK), `nome`, `cpf` (único), `email` (único), `senha` (hash), `foto` (URL/caminho), `created_at` (timestamp).
* **ContatoEmergencia**: `id` (PK), `user_id` (FK → User.id), `nome`, `telefone`, `email`.
* **ChamadoEmergencia**: `id` (PK), `user_id` (FK → User.id), `data_inicio`, `data_fim` (nullable), `status` (`ativo`/`encerrado`), `token` (NFC), `localizacao_atual` (JSON ou string).

## Endpoints REST Planejados

* `POST /user` — Cadastrar usuário.
* `PUT /user/<id>` — Atualizar dados do usuário.
* `POST /contact` — Adicionar contato de emergência.
* `DELETE /contact/<id>` — Remover contato.
* `GET /emergency/nfc/<token>` — Abrir chamado via NFC.
* `POST /emergency/sms` — Abrir chamado via SMS offline.
* `POST /location` — Atualizar localização durante chamado. 
* `POST /login` — Autenticação de usuário .
* `POST /emergency/close` — Finalizar chamado.

## Regras de Negócio

* **Token NFC único**: Cada usuária possui apenas um token NFC exclusivo.
* **Tempo de confirmação**: Sistema aguarda até 5 minutos por cancelamento antes de confirmar automaticamente.
* **Disparo de SMS**: Envio de SMS de emergência para todos os contatos no momento de confirmação.
* **Rastreamento contínuo**: Localização atualizada constantemente via `/location` durante chamado ativo.
* **Encerramento exclusivo**: Somente a usuária autenticada pode finalizar seu chamado.
