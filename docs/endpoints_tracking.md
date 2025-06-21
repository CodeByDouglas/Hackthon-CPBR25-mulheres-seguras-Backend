# Documentação de Endpoints - Rotas de Tracking (`/tracking`)

## /tracking/<token_nfc>/<call_id>
**Método:** GET  
**Descrição:** Renderiza a página de rastreamento de um chamado de emergência ativo.

**Variáveis esperadas:**
- token_nfc (na URL): Token NFC do usuário
- call_id (na URL): ID do chamado de emergência

**Retorno:**
- 200 OK: Página HTML de rastreamento com mapa.
- 403 Forbidden: "Acesso não autorizado" ou "Este chamado já foi encerrado"
- 404 Not Found: "Usuário não encontrado" ou "Chamado não encontrado"

---

## /tracking/<token_nfc>/<call_id>/route
**Método:** GET  
**Descrição:** Retorna a rota (lista de localizações) de um chamado para atualização dinâmica no mapa.

**Variáveis esperadas:**
- token_nfc (na URL): Token NFC do usuário
- call_id (na URL): ID do chamado de emergência

**Retorno:**
- 200 OK: `{ "route": [ {"lat": <float>, "lng": <float>}, ... ] }`
- 404 Not Found: `{ "error": "Usuário não encontrado" }` ou `{ "error": "Chamado não encontrado" }` 