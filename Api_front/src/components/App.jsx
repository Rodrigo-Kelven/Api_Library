import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Criar_user from './CreateUser';
import Login from './Login';

const App = () => {

  return (
    <div>
      <Router>
        <Routes>
          <Route path='/' element={<Criar_user/>}/>
          <Route path='/login' element={<Login/>}/>
          <></>
          
        </Routes>

      </Router>
    
    </div>
  );
};

export default App;
