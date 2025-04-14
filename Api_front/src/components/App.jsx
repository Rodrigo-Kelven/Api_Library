import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Criar_user from './CreateUser';
import Login from './Login';
import Criar_Livro from './Cadastro_livro';

const App = () => {

  return (
    <div>
      <Router>
        <Routes>
          <Route path='/' element={<Criar_user/>}/>
          <Route path='/login' element={<Login/>}/>
          <Route path='/C_livro' element={<Criar_Livro/>}/>         
        </Routes>

      </Router>
    
    </div>
  );
};

export default App;
