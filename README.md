# smart-bot

## Executando o projeto

Este guia explica como configurar o banco de dados PostgreSQL  e as demais instruções para rodar corretamente com a aplicação. Este guia parte do principio que o usuario ja possui o postgresql instalado 

### 1. clonar o repositório
clone este repositório

### 2. Criar o Banco de Dados  
Abra o **Prompt de Comando (cmd)** ou **PowerShell** e execute:  

```cmd```
createdb -U seu_usuario novo_banco

### 3. Restaurar banco 
Ainda no **Prompt de Comando (cmd)** ou **PowerShell** e execute:  


se for usar o dump binário (.dump)
```cmd```
```pg_restore -U seu_usuario -d novo_banco backup.dump```

se o backup for um arquivo SQL (.sql)

```cmd```
```psql -U seu_usuario -d novo_banco -f backup.sql```

para verificar se funcionou

```psql -U seu_usuario -d novo_banco -c "\dt"```


### 4. Configurar variáveis de ambiente
No diretório utils crie um arquivo .env e preencha-o da seguinte maneira

DB_NAME=nome_do_banco

DB_USER=seu_user

DB_HOST=localhost

DB_PASSWORD=sua_senha

DB_PORT=porta_do_banco


### 5. Instalar dependências

Dentro do diretório smart-bot execute no cmd ou powershell

```pip install -r req.txt```

### 6. Rodar a aplicação

Entre no diretório app e rode o comando

```streamlit run app.py```



