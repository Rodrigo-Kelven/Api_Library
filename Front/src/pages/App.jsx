import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Criar_user from './CreateUser';
import Login from './Login';
import Cadastrar_Livro from './Cadastro_livro';
import ListarLivros from './listar-livros';
import AlugarLivros from './algue-devo';
import Header from '../components/Header';
import Home from './home'






const App = () => {

  return (
    <div className='Container'>
      <Header/>
      <Router>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path='/register' element={<Criar_user />} />
          <Route path='/login' element={<Login />} />
          <Route path='/cadastro/livro' element={<Cadastrar_Livro />} />
          <Route path='/listar/livros' element={<ListarLivros />} />
          <Route path='/alugar/livros' element={<AlugarLivros />} />
        </Routes>
      </Router>

    </div>
  );
};

export default App;
