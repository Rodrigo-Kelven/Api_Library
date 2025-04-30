import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Criar_user from './CreateUser';
import Login from './Login';
import Cadastrar_Livro from './Cadastro_livro';
import ListarLivros from './listar-livros';
import AlugarLivros from './algue-devo';



const App = () => {

  return (
    <div>
      <Router>
      <nav style={{ marginBottom: "20px" }}>
        <Link to='/cadastro/livro'>Cadastrar Livros</Link> | 
        <Link to='register'> Cadastro Usuário</Link> | 
        <Link to='/login'>Login</Link> | 
        <Link to='/alugar/livros'> Empréstimos</Link> |
        <Link to='listar/livros'>Listar Livros</Link> 
      </nav>

        <Routes>
          <Route path="/" element={<h1>Bem-vindo à Biblioteca</h1>} />
          <Route path='/register' element={<Criar_user/>}/>
          <Route path='/login' element={<Login/>}/>
          <Route path='/cadastro/livro' element={<Cadastrar_Livro/>}/>
          <Route path='/listar/livros' element={<ListarLivros/>}/>
          <Route path='/alugar/livros' element={<AlugarLivros/>}/>     
        </Routes>

      </Router>
    
    </div>
  );
};

export default App;
