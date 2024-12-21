from fastapi import APIRouter, HTTPException, Depends, Query, Body, Path
from sqlmodel import Session, select
from typing import List

from config.config import get_session_books  # `engine` esteja configurado no arquivo de config
from models.books import Book, ResponseBook

# Criando o roteador com prefixo
rota_books = APIRouter(prefix="/api-books")


anotacoes = {
    "Sessions":{
        "1":"Session estabelece uma sessao com o banco de dados",
        "2":"session.add() -> adiciona o conteudo em uma sessao",
        "3":"sesssion.commit() -> commita a sessao 'salva'",
        "4":"session.refresh() -> atualiza a sessao, o db precisa ser atualizado !"
    },
    "Response_model":{
        "1":"Se você não usar List, mas apenas ResponseBook, o FastAPI entenderá que a resposta é um único livro, e isso gerará um erro, porque sua consulta está retornando múltiplos livros.",
        "2":"A consulta ao banco de dados (select(Book)) retorna uma lista de objetos Book.",
        "3":"A lista de objetos Book é convertida para uma lista de ResponseBook para atender ao modelo especificado no response_model."
    }
}


# Rota para listar todos os livros
@rota_books.get("/list", 
            status_code=200,
            name="Rota list",
            summary="Rota list",
            description="Esta rota lista todos os livros",
            response_model=List[Book]
            ) 
async def list_livros(session: Session = Depends(get_session_books)):
    statement = select(Book) # seleciona o modelo book
    books = session.exec(statement).all() # e procura retornando tudo
    return books  # Retornando a lista de livros diretamente


# Rota para registrar livro
@rota_books.post("/register-book",
                status_code=201,
                name="Rota register book",
                summary="Rota register book",
                description="Esta rota adiciona livros ao banco de dados",
                response_model=ResponseBook)
async def register_books(*,
                        livros: Book,
                        session: Session = Depends(get_session_books)
                        ):# o depends chama a função para retornar a sessao
    session.add(livros)
    session.commit()
    session.refresh(livros)  # Garantindo que o objeto livros seja atualizado após o commit

    if livros is None:
        raise HTTPException(status_code=404, detail="Error, book not created :(")
    return livros


# Rota para buscar um livro pelo ID 
@rota_books.get("/book/{book_id}",
                status_code=200,
                name="Rota search book with ID",
                summary="Rota search book with ID",
                description="Esta rota procura o livro por ID",
                response_model=Book
                )
async def read_book(
    book_id: int = Path(alias="book_id", description="Somente numeros inteiros! -> 0,1,2,3..."),
    session: Session = Depends(get_session_books)
    ):
    statement = select(Book).where(Book.id == book_id)
    book = session.exec(statement).first()  # Obtendo o primeiro livro ou None
    
    if book is None:
        raise HTTPException(status_code=404, detail="Book not Found!")  # Erro 404 se o livro não for encontrado
    return book


# Rota para atualizar um livro pelo ID
@rota_books.put("/book/{book_id}",
                status_code=200,
                name="Rota update book with ID",
                summary="Rota update book with ID",
                description="Esta rota atualiza o livro por ID",
                response_model=Book
                )
async def update_book(
    book_id: int,
    updated_book: Book,
    session: Session = Depends(get_session_books)
    ):
    # Busca o livro no banco de dados com o id fornecido
    statement = select(Book).where(Book.id == book_id)
    boook = session.exec(statement).first()

    if boook is None:
        raise HTTPException(status_code=404, detail="Book not Found!")  # Retorna 404 se o livro não for encontrado
    
    # Atualizando os dados do livro
    boook.nome = updated_book.nome
    boook.titulo = updated_book.titulo
    boook.categoria = updated_book.categoria
    boook.paginas = updated_book.paginas
    boook.autor = updated_book.autor
    boook.ano_publicacao = updated_book.ano_publicacao
    boook.editora = updated_book.editora
    boook.descricao = updated_book.descricao
    boook.isbn = updated_book.isbn
    boook.lingua = updated_book.lingua
    
    session.commit()  # Confirmar as alterações no banco de dados
    session.refresh(boook)  # Garantir que os dados atualizados sejam refletidos no objeto
    return boook


# Rota para excluir um livro pelo ID
@rota_books.delete("/book/delete/{book_id}",
                   status_code=202,
                   name="Rota delete book with ID",
                   summary="Rota delete book with ID",
                   description="Esta rota deleta o livro por ID"
                   )
async def delete_book(
    book_id: int = Path(alias="book_id", description="Somente numeros inteiros! -> 0.1.2.3..."),
    session: Session = Depends(get_session_books)
    ):
    statement = select(Book).where(Book.id == book_id)
    book = session.exec(statement).first()
    
    if book is None:
        raise HTTPException(status_code=404, detail="Book not Found!")  # Retorna 404 se o livro não for encontrado
    
    session.delete(book)  # Exclui o livro do banco de dados
    session.commit()  # Confirma a exclusão no banco
    message = {
        "Livro apagado":{
            "Id":f"{book.id}",
            "Nome":f"{book.nome}",
            "Titulo":f"{book.titulo}",
            "Categoria":f"{book.categoria}",
            "Paginas":f"{book.paginas}",
            "Autor":f"{book.autor}",
            "Ano de Publicação":f"{book.ano_publicacao}",
            "Editora":f"{book.editora}",
            "Descrição":f"{book.descricao}",
            "Isnb":f"{book.isbn}",
            "Lingua":f"{book.lingua}"
        }
    }
    return message  