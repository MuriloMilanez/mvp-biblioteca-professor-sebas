Sistema de Gestão - Biblioteca Municipal Professor Sebas (MVP)

Mínimo Produto Viável (MVP) desenvolvido para otimizar o controle de acervo, o registro de empréstimos e o monitoramento de prazos da Biblioteca Municipal Professor Sebas, promovendo a democratização do acesso à leitura e alinhando-se ao ODS 4 (Educação de Qualidade).

🎯 Funcionalidades e Requisitos Atendidos

RF01 - Registro de Livros: Cadastro estruturado de obras do acervo (título, autor e disponibilidade).
RF02 - Registro de Empréstimos: Associação ágil entre leitores cadastrados e exemplares disponíveis, com cálculo automático de prazo de devolução.
RF03 - Consulta de Acervo: Listagem e busca rápida de livros e empréstimos ativos.
RF04 - Alertas Visuais de Atrasos: Painel de avisos para identificação imediata de empréstimos expirados ou próximos do vencimento.
RNF02 - Segurança e Proteção de Dados: Autenticação de voluntários com controle de acesso e proteção contra exposição de dados sensíveis.
RNF03 - Desempenho: Operações de consulta e persistência otimizadas para respostas em menos de 3 segundos.
Acessibilidade (WCAG 2.1 Nível AA): Comunicação de estados baseada em múltiplos canais (cor, rótulo textual explícito e símbolo/ícone), eliminando barreiras para pessoas com daltonismo ou baixa visão.

🛠️ Tecnologias Utilizadas

Linguagem: Python 3.12.
Framework Web: Flask 3.0.
Persistência e ORM: SQLite + SQLAlchemy.
Qualidade e Testes: Pytest + GitHub Actions (Integração Contínua).
Frontend: HTML5, CSS3 responsivo (foco em dispositivos móveis e áreas de toque acessíveis).
