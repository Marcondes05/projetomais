📘 Projetomais – Sistema de Gestão de Projetos Acadêmicos (IFTM)
🗓️ Status do Desenvolvimento – Atualizado após conclusão da Etapa 3
✅ O que já está pronto

As três primeiras etapas do planejamento foram totalmente concluídas, assegurando a fundação do sistema e garantindo uma base sólida para o restante do desenvolvimento.

🟢 ETAPA 0 — Setup Inicial (Concluída)

✔ Estrutura do projeto criada:
app/, models/, routes/, templates/, static/, utils/

✔ Configuração de ambiente (.env, config.py)
✔ Conexão funcional com o banco Supabase (PostgreSQL)
✔ App Flask executando com sucesso
✔ Repositório GitHub organizado

🟢 ETAPA 1 — Planejamento e Arquitetura (Concluída)

✔ Definição das entidades (usuário, projeto e relações N:N)
✔ Definição das regras de negócio
✔ Perfis de usuário definidos: discente e docente
✔ Domínio institucional configurando o tipo automaticamente
✔ Modelo relacional definido
✔ Estrutura de pastas e fluxo de rotas planejados

🟢 ETAPA 2 — Banco de Dados e Models (Concluída)

✔ Model User implementado
✔ Model Project implementado (estrutura base para CRUD futuro)
✔ Tabelas auxiliares de relacionamento criadas
✔ Banco sincronizado com SQLAlchemy
✔ Inserção e leitura de dados testadas com sucesso

🟢 ETAPA 3 — Sistema de Usuários (Concluída)

Toda autenticação e fluxo de usuário está pronto e funcional:

✔ Autenticação completa:

Login

Logout

Registro

Carregamento de sessão

Proteção de rotas

✔ Validação automática por domínio institucional:

@estudante.iftm.edu.br → discente

@iftm.edu.br → docente

✔ Templates totalmente estilizados (conforme o artigo):

login.html

register.html

perfil.html

home.html

✔ Navbar funcional e responsiva
✔ Mensagens flash integradas
✔ Páginas organizadas com CSS padrão IFTM
✔ Estrutura limpa e coerente para continuar o desenvolvimento
🚀 PRÓXIMA ETAPA — ETAPA 4: CRUD de Projetos

Agora que o sistema está autenticando corretamente os usuários e registrando seus perfis, vamos iniciar a parte mais importante do sistema:

🎯 Objetivo da Etapa 4

Criar todas as funcionalidades para manipular projetos acadêmicos.

📝 Tarefas da Etapa 4:

Criar formulário completo de cadastro de projeto

Validar acesso (somente docentes podem criar/editar)

Criar página de listagem Todos os Projetos

Criar página Meus Projetos

Criar página de detalhes do projeto

Implementar edição e exclusão

Integrar alunos e coorientadores ao projeto

Preparar autocomplete simples para usuários

Adaptar tudo ao estilo visual já aplicado

🧱 Status Geral Atual

O sistema tem:

✔ Auth funcional
✔ Estrutura de navegação pronta
✔ Modelos base funcionando
✔ Estilo visual padronizado
✔ Banco conectado e sincronizado

O ambiente está 100% pronto para iniciar o desenvolvimento do módulo principal: gestão de projetos.