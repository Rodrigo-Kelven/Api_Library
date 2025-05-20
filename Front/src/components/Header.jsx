import React from 'react';
import "../statics/Header.css"


const Header = () =>{
     return(
        <>
          <header className="Header">
            
            <nav style={{ marginBottom: "20px" }} className="Header__links">
              <a href=""></a>
              <a href='/cadastro/livro'>Cadastrar Livros</a> |
              <a href='/register'> Cadastro Usuário</a> |
              <a href='/login'>Login</a> |
              <a href='/alugar/livros'> Empréstimos</a> |
              <a href='/listar/livros'>Listar Livros</a>
            </nav>                         
          </header>
        </>
     )
}
export default Header;