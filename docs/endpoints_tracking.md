# Documentação de Endpoints - Rotas de Tracking

## /<token_nfc>/<call_id>
**Método:** GET  
**Descrição:** Renderiza a página de rastreamento de um chamado de emergência ativo para o usuário identificado pelo token NFC e pelo ID do chamado.

**Variáveis esperadas:**
- token_nfc (na URL): Token NFC do usuário
- call_id (na URL): ID do chamado de emergência

**Retorno:**
- 200 OK: Página HTML de rastreamento com informações do usuário e mapa
- 403 Forbidden: "Acesso não autorizado" ou "Este chamado já foi encerrado"
- 404 Not Found: "Usuário não encontrado" ou "Chamado não encontrado"

---

## /<token_nfc>/<call_id>/route
**Método:** GET  
**Descrição:** Retorna a rota (lista de localizações) do chamado de emergência para o usuário e chamado informados.

**Variáveis esperadas:**
- token_nfc (na URL): Token NFC do usuário
- call_id (na URL): ID do chamado de emergência

**Retorno:**
- 200 OK: `{ "route": [ {"lat": <float>, "lng": <float>}, ... ] }`
- 404 Not Found: `{ "error": "Usuário não encontrado" }` ou `{ "error": "Chamado não encontrado" }` 