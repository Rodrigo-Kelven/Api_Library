import React from 'react';
import api from './Api';
import Criar_user from './teste';

const UserRegister = () => {
  const addUser = async (userData) => {
    try {
      await api.post('/users', userData);
      alert('Usuário cadastrado com sucesso!');
    } catch (error) {
      console.error('Erro ao cadastrar usuário', error);
    }
  };

  return (
    <div>
 
      <Criar_user addUser={addUser} />
    </div>
  );
};

export default UserRegister;
