import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Criar_user from './CreateUser';
import Login from './Login';
import Cadastrar_Livro from './Cadastro_livro';
import ListarLivros from './listar-livros';
import AlugarLivros from './algue-devo';

const App = () => {

  return (
    <div>
      <Router>
        <Routes>
          <Route path='/' element={<Criar_user/>}/>
          <Route path='/login' element={<Login/>}/>
          <Route path='/C-livro' element={<Cadastrar_Livro/>}/>
          <Route path='/listar-B' element={<ListarLivros/>}/>
          <Route path='/Devo_aluga' element={<AlugarLivros/>}/>     
        </Routes>

      </Router>
    
    </div>
  );
};

export default App;
