
# Gestor de Tarefas

Uma aplicação web de gerenciamento de tarefas baseada em Flask que oferece autenticação de usuários e rastreamento de atividades. O sistema possui gerenciamento completo de usuários com registro, login, recuperação de senha e uma interface abrangente para gestão de tarefas.

## ✨ Funcionalidades

### Gerenciamento de Usuários
- **Cadastro de Usuário** - Crie novas contas com verificação por e-mail
- **Login/Logout Seguro** - Autenticação baseada em sessão
- **Recuperação de Senha** - Sistema de recuperação por e-mail
- **Gerenciamento de Perfil** - Função para alterar senha

### Gerenciamento de Tarefas
- **Criação de Tarefas** - Crie tarefas com descrição, prioridade e prazos
- **Sistema de Prioridade** - Quatro níveis: Baixa, Média, Alta, Crítica com cores
- **Fluxo de Status** - Pendente → Em andamento → Concluída → Cancelada
- **Prazos Automáticos** - Baseados no nível de prioridade (15, 10, 5, 2 dias)
- **Atribuição de Tarefas** - Atribua tarefas a responsáveis
- **Localização** - Especifique o local da tarefa

### Interface
- **Design Responsivo** - Interface com Bootstrap 5 para todos os dispositivos
- **Atualizações em Tempo Real** - Mudanças dinâmicas de status e tarefas
- **Navegação Intuitiva** - Interface limpa e fácil de usar
- **Acesso em Rede** - Suporte multiusuário na rede local

### Screenshots
👉 https://github.com/lucasbm92/miniature-octo-giggle/blob/main/SCREENSHOTS.md

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python Flask
- **Banco de Dados**: MySQL com SQLAlchemy ORM
- **Frontend**: HTML5, Bootstrap 5, templates Jinja2
- **E-mail**: Flask-Mail para notificações
- **Segurança**: Hash de senha com Werkzeug, gerenciamento de sessão
- **Deploy**: Pronto para Gunicorn WSGI

## 📋 Requisitos

- Python 3.7+
- MySQL 5.7+
- pip (gerenciador de pacotes Python)

## 🚀 Início Rápido

### 1. Clone o Repositório
```bash
git clone https://github.com/lucasbm92/miniature-octo-giggle.git
cd miniature-octo-giggle
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o Ambiente
#3.1 Copie o arquivo de exemplo de ambiente
```bash
copy .env.example .env
```
#3.2 Edite o .env com suas configurações:
# - Gere SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))"
# - Atualize as credenciais do banco de dados
# - Configure as opções de e-mail

### 4. Configure o Banco de Dados
```bash
# Crie ou atualize o schema do banco de dados
python migrate_db.py
```

### 5. Inicie a Aplicação
```bash
# Modo desenvolvimento
python app.py

# Modo produção
python start_production.py
```

### 6. Acesse a Aplicação
- **Local**: http://localhost:5000
- **Rede**: http://SEU_IP:5000

## 🌐 Implantação em Rede

Para acesso multiusuário na rede local:

1. **Descubra seu endereço IP**:
   ```cmd
   ipconfig
   ```

2. **Configure o firewall** para liberar o Python/porta 5000

3. **Acesse de outros dispositivos**: `http://IP_DO_SERVIDOR:5000`

4. **Usuários podem se cadastrar e logar** de qualquer dispositivo na rede

## ⚙️ Configuração

### Variáveis de Ambiente (.env)
```env
SECRET_KEY=sua-chave-secreta-de-64-caracteres
SQLALCHEMY_DATABASE_URI=mysql+pymysql://usuario:senha@localhost:3306/banco
MAIL_USERNAME=seu-email@dominio.com
MAIL_PASSWORD=sua-senha-do-email
FLASK_ENV=production
```

### Configuração do Banco de Dados
```sql
CREATE DATABASE gestor_tarefas;
# Atualize o .env com suas credenciais
```

## 📝 Uso

### Primeiros Passos
1. **Cadastre-se** com nome de usuário, e-mail e senha
2. **Faça login** com suas credenciais
3. **Crie tarefas** usando o botão "+"
4. **Gerencie tarefas** com níveis de prioridade e prazos
5. **Acompanhe o progresso** com atualizações de status

### Fluxo de Tarefas
1. **Criar** → Tarefa inicia como "Pendente"
2. **Iniciar** → Muda para "Em andamento"
3. **Concluir** → Marca como "Concluída"
4. **Excluir** → Remove tarefas concluídas ou indesejadas

### Níveis de Prioridade
- **Baixa** - prazo de 15 dias
- **Média** - prazo de 10 dias
- **Alta** - prazo de 5 dias
- **Crítica** - prazo de 2 dias

## 🔧 Desenvolvimento

### Estrutura do Projeto
```
miniature-octo-giggle/
├── app.py              # Ponto de entrada da aplicação Flask
├── auth.py             # Rotas e lógica de autenticação
├── models.py           # Modelos e funções do banco de dados
├── migrate_db.py       # Script de migração do banco
├── backup.py           # Utilitário de backup do banco
├── start_production.py # Script de inicialização em produção
├── templates/          # Templates HTML
├── static/             # Arquivos estáticos (CSS, JS, imagens)
├── logs/               # Logs da aplicação
└── backups/            # Backups do banco
```

### Adicionando Funcionalidades
1. **Modelos**: Adicione novos modelos em `models.py`
2. **Rotas**: Adicione rotas em `auth.py` ou crie novos blueprints
3. **Templates**: Crie templates HTML em `templates/`
4. **Banco de dados**: Execute `python migrate_db.py` após alterações no modelo ou em um deploy novo

## 🔒 Recursos de Segurança

- **Hash de Senha** - Armazenamento seguro com Werkzeug
- **Gerenciamento de Sessão** - Controle de sessão Flask
- **Validação de Entrada** - Validação e sanitização de formulários
- **Tratamento de Erros** - Páginas de erro amigáveis e logs
- **Cabeçalhos de Segurança** - Proteção XSS, prevenção de sniffing de conteúdo

## 📊 Backup & Manutenção

### Backup do Banco de Dados
```bash
# Criar backup
python backup.py

# Backups são armazenados na pasta backups/
```

### Monitoramento de Logs
```bash
# Visualizar logs da aplicação
tail -f logs/gestor_tarefas.log
```

## 🐛 Solução de Problemas

### Problemas Comuns

**Não consegue acessar de outros computadores:**
- Verifique as configurações do firewall
- Confirme que o app está rodando com `host='0.0.0.0'`
- Certifique-se que o IP está correto

**Erros de conexão com o banco:**
- Verifique as credenciais no `.env`
- Confirme que o MySQL está rodando
- Teste a conectividade do banco

**E-mail não funciona:**
- Verifique as configurações de e-mail no `.env`
- Cheque as configurações de segurança do provedor
- Teste a conectividade SMTP

## 📈 Melhorias Futuras

- [ ] Categorias e tags de tarefas
- [ ] Notificações de vencimento
- [ ] Anexos de arquivos
- [ ] Comentários e histórico de tarefas
- [ ] Exportação (PDF, Excel)
- [ ] Aplicativo mobile
- [ ] API REST
- [ ] Relatórios avançados

## 🤝 Contribuindo

1. Faça um fork do repositório
2. Crie uma branch de funcionalidade
3. Faça suas alterações
4. Adicione testes se aplicável
5. Envie um pull request


## 📄 Licença

Este projeto está sob licença MIT - veja o arquivo LICENSE para detalhes.

## 👨‍💻 Autor

**Lucas Brito Marinho** - [lucasbm92](https://github.com/lucasbm92)

## 🙏 Agradecimentos

- Framework Flask e comunidade
- Bootstrap pelos componentes responsivos
- MySQL pelo armazenamento confiável
- Contribuidores e testadores

---

**Pronto para uso em produção!** 🚀

Para instruções detalhadas de implantação, veja [DEPLOYMENT.md](DEPLOYMENT.md)