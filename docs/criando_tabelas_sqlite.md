# Como criar as tabelas no banco SQLite (Flask + SQLAlchemy)

Este guia explica como criar as tabelas do seu projeto Flask no banco de dados SQLite, utilizando SQLAlchemy.

## Passo a passo

1. **Ative o ambiente virtual:**
   ```bash
   source .venv/bin/activate
   ```

2. **Abra o interpretador Python:**
   ```bash
   python
   ```

3. **Execute os comandos abaixo no prompt do Python:**
   ```python
   from app import create_app, db
   from app.models.base import init_models
   app = create_app()
   with app.app_context():
       init_models()  # Garante que todos os modelos estão importados
       db.create_all()  # Cria as tabelas no banco
   ```

4. **Saia do interpretador Python:**
   ```python
   exit()
   Ctrl + d
   ```

5. **Verifique se o arquivo `database.db` foi criado/atualizado**
   - O arquivo deve estar na raiz do projeto.
   - Você pode visualizar as tabelas usando um plugin de SQLite na sua IDE (ex: Cursor).

## Dicas importantes
- Se o arquivo `database.db` já existia e estava vazio, apague-o antes de rodar o passo a passo novamente.
- Certifique-se de que o caminho do banco está correto em `app/config`:
  ```python
  'SQLALCHEMY_DATABASE_URI': 'sqlite://database.db'
  ```
- Se aparecer algum erro, confira se todos os modelos estão corretamente importados e se não há erros de digitação.

