import React, { useEffect, useState } from 'react';
import '../statics/home.css';

const Home = () => {
  return (
    <>
      <div className='container'>
        <div className="home">
          <h1>Bem-vindo ao Sistema de Empréstimo de Livros</h1>
          <p>Faça login ou cadastre-se para começar a usar o sistema.</p>
          <a href='/listar/livros'>Listar Livros</a>
        </div>
      </div>
    </>
  );

}
export default Home;
