from datetime import timedelta
from .models import db, Livro, Emprestimo, agora_utc

def criar_livro(titulo: str, autor: str, genero: str, quantidade: int) -> tuple[bool, str]:
    if not titulo or not autor or not genero:
        return False, 'Todos os campos de texto são obrigatórios.'
    if quantidade < 1:
        return False, 'A quantidade inicial deve ser de pelo menos 1 exemplar.'

    novo_livro = Livro(
        titulo=titulo.strip(),
        autor=autor.strip(),
        genero=genero.strip(),
        quantidade=quantidade
    )
    db.session.add(novo_livro)
    db.session.commit()
    return True, 'Livro registrado no acervo com sucesso!'

def processar_emprestimo(livro_id: int, usuario: str, data_retirada, data_devolucao) -> tuple[bool, str]:
    livro = db.session.get(Livro, livro_id)
    if not livro:
        return False, 'Livro não encontrado no acervo.'
    if livro.quantidade <= 0:
        return False, 'Não há exemplares disponíveis deste livro no momento.'
    if not usuario.strip():
        return False, 'O nome do usuário é obrigatório.'
    if data_devolucao < data_retirada:
        return False, 'A data de devolução não pode ser anterior à data de retirada.'

    novo_emp = Emprestimo(
        livro_id=livro.id,
        usuario=usuario.strip(),
        data_retirada=data_retirada,
        data_devolucao=data_devolucao
    )
    livro.quantidade -= 1
    db.session.add(novo_emp)
    db.session.commit()
    return True, 'Operação realizada com sucesso!'

def renovar_emprestimo(emprestimo_id: int, dias: int = 14) -> tuple[bool, str]:
    emp = db.session.get(Emprestimo, emprestimo_id)
    if not emp or emp.devolvido:
        return False, 'Empréstimo inválido ou já finalizado.'

    emp.data_devolucao = agora_utc() + timedelta(days=dias)
    db.session.commit()
    return True, 'Prazo renovado por mais 14 dias com sucesso!'
