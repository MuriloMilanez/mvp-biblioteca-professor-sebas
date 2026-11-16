from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Livro, Emprestimo, agora_utc
from .services import criar_livro, processar_emprestimo, renovar_emprestimo

main_bp = Blueprint('main', __name__)

def popular_dados_iniciais():
    if Livro.query.count() == 0:
        livros_demo = [
            Livro(titulo='Dom Casmurro', autor='Machado de Assis', genero='Romance', quantidade=5),
            Livro(titulo='1984', autor='George Orwell', genero='Ficção', quantidade=3),
            Livro(titulo='O Pequeno Príncipe', autor='Antoine de Saint-Exupéry', genero='Infantil', quantidade=7),
            Livro(titulo='A Revolução dos Bichos', autor='George Orwell', genero='Ficção', quantidade=4),
        ]
        db.session.add_all(livros_demo)
        db.session.flush()

        hoje = agora_utc()
        emprestimos_demo = [
            Emprestimo(
                livro_id=livros_demo[0].id,
                usuario='Maria Silva',
                data_retirada=hoje - timedelta(days=18),
                data_devolucao=hoje - timedelta(days=4)
            ),
            Emprestimo(
                livro_id=livros_demo[2].id,
                usuario='Ana Costa',
                data_retirada=hoje - timedelta(days=16),
                data_devolucao=hoje - timedelta(days=2)
            ),
            Emprestimo(
                livro_id=livros_demo[1].id,
                usuario='João Souza',
                data_retirada=hoje - timedelta(days=5),
                data_devolucao=hoje + timedelta(days=9)
            ),
            Emprestimo(
                livro_id=livros_demo[3].id,
                usuario='Carlos Lima',
                data_retirada=hoje - timedelta(days=2),
                data_devolucao=hoje + timedelta(days=12)
            ),
        ]
        db.session.add_all(emprestimos_demo)
        db.session.commit()

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        if email and len(senha) >= 4:
            popular_dados_iniciais()
            return redirect(url_for('main.painel'))
        flash('E-mail ou palavra-passe incorretos. Verifique e tente novamente.', 'erro')
    return render_template('login.html')

@main_bp.route('/painel')
def painel():
    popular_dados_iniciais()
    livros = Livro.query.limit(5).all()
    emprestimos = Emprestimo.query.filter_by(devolvido=False).limit(5).all()
    return render_template('painel.html', livros=livros, emprestimos=emprestimos, aba='painel')

@main_bp.route('/registrar-livro', methods=['GET', 'POST'])
def registrar_livro():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '')
        autor = request.form.get('autor', '')
        genero = request.form.get('genero', '')
        try:
            quantidade = int(request.form.get('quantidade', 1))
        except ValueError:
            quantidade = 0

        sucesso, mensagem = criar_livro(titulo, autor, genero, quantidade)
        flash(mensagem, 'sucesso' if sucesso else 'erro')
        if sucesso:
            return redirect(url_for('main.painel'))

    return render_template('registrar_livro.html', aba='registrar_livro')

@main_bp.route('/registrar-emprestimo', methods=['GET', 'POST'])
def registrar_emprestimo():
    livros_disponiveis = Livro.query.filter(Livro.quantidade > 0).all()

    if request.method == 'POST':
        try:
            livro_id = int(request.form.get('livro_id', 0))
            usuario = request.form.get('usuario', '')
            dt_retirada = datetime.strptime(request.form.get('data_retirada', ''), '%Y-%m-%d').replace(tzinfo=timezone.utc)
            dt_devolucao = datetime.strptime(request.form.get('data_devolucao', ''), '%Y-%m-%d').replace(tzinfo=timezone.utc)
        except ValueError:
            flash('Dados de formulário ou datas inválidas.', 'erro')
            return redirect(url_for('main.registrar_emprestimo'))

        sucesso, mensagem = processar_emprestimo(livro_id, usuario, dt_retirada, dt_devolucao)
        flash(mensagem, 'sucesso' if sucesso else 'erro')
        if sucesso:
            return redirect(url_for('main.painel'))

    hoje_str = agora_utc().strftime('%Y-%m-%d')
    devolucao_str = (agora_utc() + timedelta(days=14)).strftime('%Y-%m-%d')
    return render_template(
        'registrar_emprestimo.html',
        livros=livros_disponiveis,
        hoje=hoje_str,
        devolucao_padrao=devolucao_str,
        aba='registrar_emprestimo'
    )

@main_bp.route('/consultar-acervo')
def consultar_acervo():
    busca = request.args.get('busca', '').strip()
    if busca:
        livros = Livro.query.filter(
            (Livro.titulo.ilike(f'%{busca}%')) |
            (Livro.autor.ilike(f'%{busca}%')) |
            (Livro.genero.ilike(f'%{busca}%'))
        ).all()
    else:
        livros = Livro.query.all()
    return render_template('consultar_acervo.html', livros=livros, busca=busca, aba='consultar_acervo')

@main_bp.route('/relatorios')
def relatorios():
    popular_dados_iniciais()
    filtro = request.args.get('filtro', 'todos')
    todos_ativos = Emprestimo.query.filter_by(devolvido=False).all()

    em_atraso_lista = [e for e in todos_ativos if e.em_atraso]
    em_dia_lista = [e for e in todos_ativos if not e.em_atraso]

    if filtro == 'atrasados':
        exibidos = em_atraso_lista
    elif filtro == 'em_dia':
        exibidos = em_dia_lista
    else:
        exibidos = todos_ativos

    return render_template(
        'relatorios.html',
        emprestimos=exibidos,
        total_ativos=len(todos_ativos),
        total_em_dia=len(em_dia_lista),
        total_atrasados=len(em_atraso_lista),
        filtro=filtro,
        aba='relatorios'
    )

@main_bp.route('/renovar/<int:emprestimo_id>', methods=['POST'])
def renovar_prazo(emprestimo_id):
    sucesso, mensagem = renovar_emprestimo(emprestimo_id)
    flash(mensagem, 'sucesso' if sucesso else 'erro')
    return redirect(url_for('main.relatorios'))
