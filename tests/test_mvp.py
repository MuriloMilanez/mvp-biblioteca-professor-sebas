from datetime import timedelta
from app import create_app
from app.models import db, Livro, Emprestimo, agora_utc

def test_fluxo_completo_biblioteca():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    client = app.test_client()

    # Teste de cadastro de livro (RF01)
    resp_livro = client.post('/registrar-livro', data={
        'titulo': 'Vidas Secas',
        'autor': 'Graciliano Ramos',
        'genero': 'Romance',
        'quantidade': 2
    }, follow_redirects=True)
    assert resp_livro.status_code == 200

    with app.app_context():
        livro = Livro.query.filter_by(titulo='Vidas Secas').first()
        assert livro is not None
        assert livro.quantidade == 2
        livro_id = livro.id

    # Teste de registro de empréstimo e baixa no acervo (RF02)
    hoje = agora_utc().strftime('%Y-%m-%d')
    devolucao = (agora_utc() + timedelta(days=14)).strftime('%Y-%m-%d')
    resp_emp = client.post('/registrar-emprestimo', data={
        'livro_id': livro_id,
        'usuario': 'Fernanda Lima',
        'data_retirada': hoje,
        'data_devolucao': devolucao
    }, follow_redirects=True)
    assert resp_emp.status_code == 200

    # Teste unitário de detecção de atraso e renovação (RF04)
    with app.app_context():
        livro_atualizado = db.session.get(Livro, livro_id)
        assert livro_atualizado.quantidade == 1

        emp = Emprestimo.query.filter_by(usuario='Fernanda Lima').first()
        assert emp is not None
        assert emp.em_atraso is False

        # Simula atraso de 3 dias
        emp.data_devolucao = agora_utc() - timedelta(days=3)
        assert emp.em_atraso is True
