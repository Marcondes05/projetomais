# 🧾 Sistema de Gestão de Projetos Acadêmicos – **PROJETOMAIS**

Sistema desenvolvido como Trabalho de Conclusão de Curso (TCC) para centralização, organização e gerenciamento de projetos acadêmicos no âmbito do Instituto Federal do Triângulo Mineiro (IFTM).

O sistema permite que docentes e discentes realizem cadastro, consulta, gerenciamento e acompanhamento de projetos acadêmicos vinculados aos campi da instituição.

---

## 👨‍💻 **Autor**
**Marcondes Fernandes Ferreira Neto**

## 👩‍🏫 **Orientadora**
**Profa. Reane Franco Goulart**

---

# 📌 **Objetivo do Sistema**

O **PROJETOMAIS** foi criado para resolver problemas comuns na gestão de projetos acadêmicos:

- Dispersão de informações entre diferentes documentos e plataformas  
- Falta de um ambiente único para consulta e acompanhamento  
- Dificuldade de controle pelas coordenações e orientadores  
- Falta de transparência e organização para estudantes

O sistema centraliza **todo o ciclo de vida dos projetos**, desde o cadastro até sua visualização e filtragem por vários critérios.

---

# 🚀 **Funcionalidades do Sistema**

## 👤 **Autenticação**
- Login seguro (Flask-Login)
- Perfis: **Docente**, **Discente** e **Técnico**
- Controle de acesso (RBAC)
- Senhas protegidas (hashing seguro)
- Exibição/ocultação de senha no formulário

---

## 📚 **Gestão de Projetos (Docentes)**

### Criar projetos com:
- Título
- Resumo
- Tipo (Ensino, Pesquisa, Extensão)
- Edital
- Ano
- Financiador
- Campus herdado automaticamente do orientador
- Seleção de estudantes
- Seleção de coorientadores
- Seleção de orientador (autocomplete)

### Editar projetos
- Atualização completa do cadastro
- Atualização de vínculos (alunos e coorientadores)

### Excluir projetos
- Exclusão permitida apenas ao orientador do projeto

---

## 🔍 **Listagem e Filtros**

### Filtros avançados na página "Projetos":
- Título
- Tipo
- Ano
- Edital
- Orientador (autocomplete)
- Campus  
- Combinação simultânea de filtros  
- Ordenação automática (mais recentes primeiro)

### Página “Meus Projetos”
- Exibe:
  - Projetos onde o usuário é orientador
  - Projetos onde o usuário é coorientador
  - Projetos onde o estudante está vinculado
- Filtros básicos (título e ano)

---

## ⚡ **Experiência do Usuário (UX/UI)**

- Interface leve e moderna
- Navbar com navegação inteligente
- Botões de retorno automática
- Autocomplete otimizado para:
  - Orientadores  
  - Estudantes  
  - Coorientadores  
- Badges removíveis para seleção múltipla
- Layout responsivo
- Feedback visual com Flash Messages

---------------------------------------------------------------------------

## 🏛 **Arquitetura do Projeto**

        projetomais/
        │
        ├── app/
        │ ├── models/
        │ │ ├── user.py
        │ │ ├── project.py
        │ │
        │ ├── routes/
        │ │ ├── auth_routes.py
        │ │ ├── project_routes.py
        │ │ ├── main_routes.py
        │ │ ├── user_routes.py
        │ │
        │ ├── utils/
        │ │ ├── auth_utils.py
        │ │
        │ ├── templates/
        │ │ ├── base.html
        │ │ ├── home.html
        │ │ ├── login.html
        │ │ ├── register.html
        │ │ ├── projetos_list.html
        │ │ ├── meus_projetos.html
        │ │ ├── projeto_view.html
        │ │ ├── project_form.html
        │ │ ├── projeto_edit.html
        │ │
        │ ├── static/
        │ │ ├── css/style.css
        │ │ ├── js/autocomplete.js
        │ │
        │ ├── init.py
        │
        ├── config.py
        ├── run.py
        ├── requirements.txt
        ├── README.md
        ├── .env


---------------------------------------------------------------------------

# 🛢 Banco de Dados – **Supabase (PostgreSQL)**

### Tabela **usuarios**
| Campo | Tipo | Descrição |
|-------|-------|-----------|
| id | integer | PK |
| nome | varchar | Nome completo |
| cpf | varchar | Documento do usuário |
| email | varchar | Login institucional |
| senha | varchar | Hash seguro |
| tipo | varchar | docente / discente / técnico |
| campus | varchar | Campus vinculado |
| curso | varchar | Curso (somente discentes) |

### Tabela **projects**
| Campo | Tipo | Descrição |
|-------|-------|-----------|
| id | integer | PK |
| titulo | varchar | Nome do projeto |
| resumo | text | Pode repetir o título |
| tipo | varchar | Ensino / Pesquisa / Extensão |
| edital | varchar | Ex: 15/2024 |
| ano | varchar | Ex: 2025 |
| financiador | varchar | PIBIC, PIVIC, FAPEMIG etc |
| campus | varchar | Herdado do orientador |
| orientador_id | integer | FK → usuarios.id |

### Tabelas auxiliares
- **project_students**
- **project_coorientadores**

Relacionamentos muitos-para-muitos.

---

# 🔧 Instalação e Configuração

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/projetomais.git
cd projetomais
```

### 2️⃣ Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Criar arquivo .env
```ini
DATABASE_URL=postgresql://usuario:senha@host:5432/postgres
SECRET_KEY=sua_chave_secreta
```

### 5️⃣ Rodar o sistema
```bash
python run.py
```

---

# 🧠 Lógica do Autocomplete

O autocomplete utilizado para Orientadores, Estudantes e Coorientadores implementa:

- Requisições AJAX a `/buscar-usuarios`
- Preenchimento automático do campo *hidden*
- Exibição de badges com opção de remover
- Prevenção de duplicação de itens selecionados
- Navegação por teclado (↑ ↓ Enter)

---

# 📈 Melhorias futuras sugeridas

- Recuperação de senha via e-mail  
- Anexos e upload de documentos do projeto   
- Dashboard com estatísticas (gráficos)  
- Módulo de certificados  
- Histórico e versões do projeto  

---

# 📄 Licença
Projeto desenvolvido exclusivamente para fins acadêmicos no Instituto Federal do Triângulo Mineiro.

---

# 🏁 Conclusão

O **PROJETOMAIS** entrega uma solução eficiente, organizada e moderna para docentes e discentes acompanharem seus projetos de forma clara e centralizada.  
É uma plataforma completa que pode ser expandida e integrada futuramente para outros setores acadêmicos.

---

# 🙌 Agradecimentos

A todos os professores, colegas e à orientadora **Reane Franco Goulart** pelo apoio no desenvolvimento deste trabalho.
