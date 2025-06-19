# Documentação de Endpoints - Rotas de Emergência

## /ping
**Método:** GET  
**Descrição:** Endpoint de teste para verificar se o serviço está online. Retorna 'pong-emergency'.

**Variáveis esperadas:** Nenhuma
**Retorno:**
- 200 OK: 'pong-emergency'

---

## /nfc/<token>
**Método:** GET  
**Descrição:** Renderiza a página de confirmação de emergência ao receber um token NFC válido. Exibe opções para confirmar ou abortar o chamado.

**Variáveis esperadas:**
- token (na URL): Token NFC do usuário

**Retorno:**
- 200 OK: Página HTML de confirmação
- 404 Not Found: "Token NFC inválido"

---

## /confirm/<token>
**Método:** POST  
**Descrição:** Cria um novo chamado de emergência ativo para o usuário do token NFC recebido.

**Variáveis esperadas:**
- token (na URL): Token NFC do usuário

**Retorno:**
- 201 Created: `{ "success": true, "call_id": <id>, "message": "Chamado de emergência criado com sucesso" }`
- 400 Bad Request: `{ "success": false, "error": "Já existe um chamado ativo para este usuário" }`
- 404 Not Found: `{ "success": false, "error": "Token NFC inválido" }`
- 500 Internal Server Error: `{ "success": false, "error": "Erro ao criar chamado: ..." }`

---

## /abort/<token>
**Método:** POST  
**Descrição:** Aborta o chamado de emergência ativo do usuário do token NFC recebido.

**Variáveis esperadas:**
- token (na URL): Token NFC do usuário

**Retorno:**
- 200 OK: `{ "success": true, "message": "Chamado abortado com sucesso" }`
- 404 Not Found: `{ "success": false, "error": "Token NFC inválido" }` ou `{ "success": false, "error": "Não há chamado ativo para este usuário" }`
- 500 Internal Server Error: `{ "success": false, "error": "Erro ao abortar chamado: ..." }`

---

## /update-location
**Método:** POST  
**Descrição:** Atualiza a localização do usuário durante um chamado ativo.

**Variáveis esperadas (JSON no corpo):**
- token_nfc: string (obrigatório)
- latitude: float (obrigatório)
- longitude: float (obrigatório)

**Retorno:**
- 200 OK: `{ "message": "Localização atualizada com sucesso", "call_id": <id>, "route_length": <n>, "current_location": {"lat": ..., "lng": ...} }`
- 400 Bad Request: `{ "error": "Token NFC, latitude e longitude são obrigatórios" }` ou `{ "error": "Latitude e longitude devem ser números" }`
- 404 Not Found: `{ "error": "Usuário não encontrado" }` ou `{ "error": "Não há chamado ativo para este usuário" }`
- 500 Internal Server Error: `{ "error": "Erro ao atualizar localização: ..." }`

---

## /success/active
**Método:** GET  
**Descrição:** Renderiza a página de sucesso para chamado de emergência ativo, informando que a localização está sendo compartilhada.

**Variáveis esperadas:** Nenhuma
**Retorno:**
- 200 OK: Página HTML de sucesso

---

## /success/aborted
**Método:** GET  
**Descrição:** Renderiza a página de sucesso para chamado de emergência abortado.

**Variáveis esperadas:** Nenhuma
**Retorno:**
- 200 OK: Página HTML de sucesso

---

## /close-call
**Método:** POST  
**Descrição:** Encerra o chamado ativo do usuário identificado pelo token NFC recebido.

**Variáveis esperadas (JSON no corpo):**
- token_nfc: string (obrigatório)

**Retorno:**
- 200 OK: `{ "success": true, "message": "Chamado encerrado com sucesso" }`
- 400 Bad Request: `{ "success": false, "error": "Token NFC não fornecido" }`
- 404 Not Found: `{ "success": false, "error": "Usuário não encontrado para o token informado" }` ou `{ "success": false, "error": "Nenhum chamado ativo encontrado para este usuário" }`
- 500 Internal Server Error: `{ "success": false, "error": "Erro ao encerrar chamado: ..." }`

---

## /add-contact
**Método:** POST  
**Descrição:** Cadastra um novo contato de emergência vinculado ao usuário do token NFC recebido.

**Variáveis esperadas (JSON no corpo):**
- token_nfc: string (obrigatório)
- contact: objeto com os campos:
    - nome: string (obrigatório)
    - telefone: string (obrigatório)
    - email: string (obrigatório)

**Retorno:**
- 201 Created: `{ "success": true, "message": "Contato cadastrado com sucesso", "contact_id": <id> }`
- 400 Bad Request: `{ "success": false, "error": "Token NFC e dados do contato são obrigatórios" }`
- 404 Not Found: `{ "success": false, "error": "Usuário não encontrado para o token informado" }`
- 500 Internal Server Error: `{ "success": false, "error": "Erro ao cadastrar contato: ..." }`

---

## /calls/<token_nfc>
**Método:** GET  
**Descrição:** Retorna todos os chamados do usuário do token NFC informado e indica se há algum chamado ativo.

**Variáveis esperadas:**
- token_nfc (na URL): Token NFC do usuário

**Retorno:**
- 200 OK: 
```
{
  "success": true,
  "calls": [
    {
      "id": <id>,
      "status": "Ativo" | "Encerrado" | "Abortado",
      "date": "YYYY-MM-DD",
      "start_time": "HH:MM:SS",
      "end_time": "HH:MM:SS" | null,
      "route": [...],
      "token_nfc": <token>,
      "localizacao_atual": <string|null>
    },
    ...
  ],
  "has_active": true | false
}
```
- 404 Not Found: `{ "success": false, "error": "Usuário não encontrado para o token informado" }` 

---

## /nfc/auto/<token>
**Método:** GET  
**Descrição:** Cria um chamado de emergência imediatamente ao receber o token NFC, salva coordenadas iniciais (se fornecidas) e envia SMS para todos os contatos de emergência do usuário.

**Variáveis esperadas:**
- token (na URL): Token NFC do usuário
- lat (query string, opcional): Latitude inicial (float)
- lng (query string, opcional): Longitude inicial (float)

**Retorno:**
- 201 Created: 
  - Sucesso total: `{ "success": true, "call_id": <id>, "message": "Chamado de emergência criado e SMS enviados com sucesso" }`
  - Sucesso parcial: `{ "success": false, "call_id": <id>, "message": "Chamado criado mas houve erros no envio de SMS", "sms_errors": [...] }`
- 400 Bad Request: 
  - `{ "success": false, "error": "Já existe um chamado ativo para este usuário" }`
  - `{ "error": "Latitude e longitude devem ser números válidos" }`
- 404 Not Found: `{ "success": false, "error": "Token NFC inválido" }`
- 500 Internal Server Error: `{ "success": false, "error": "Erro ao criar chamado: ..." }`

---

## /delete-contact/<contact_id>
**Método:** DELETE  
**Descrição:** Remove um contato de emergência pelo ID.

**Variáveis esperadas:**
- contact_id (na URL): ID do contato a ser removido

**Retorno:**
- 200 OK: `{ "success": true, "message": "Contato removido com sucesso" }`
- 404 Not Found: `{ "success": false, "error": "Contato não encontrado" }`
- 500 Internal Server Error: `{ "success": false, "error": "Erro ao remover contato: ..." }` 