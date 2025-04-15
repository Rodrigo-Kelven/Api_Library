import React, { useState } from "react";
import Api from "./Api";
import { useNavigate } from "react-router-dom";

const Login = () => {

  const pagina = useNavigate() // useNavigate usada para

  const [form, setForm] = useState({ //usa o hook useState para armazenar os dados
    email: '',  // Usando 'username' como email, conforme esperado no backend
    password: '',
  });

  // Atualiza o estado dos campos
  const Mudar_valor = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Função para enviar os dados ao backend
  const EnviarDado = async (e) => {
    e.preventDefault();

    // Preparar os parâmetros para envio (username como email)
    const params = new URLSearchParams(); // Classe do javaScript que permite manipular parâmetros de uma Url
    params.append("username", form.email);  // Aqui 'username' é o email do usuário
    params.append("password", form.password);

    try {
      
      const response = await Api.post("/api-library/v1/auth/login/", params, { // Realizar a requisição POST para login
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",  //diz que os dados serão passados no cabeçalhos em vez da url do site
        },

      });

      
      if (response.data.access_token) { // Verificar se o token foi retornado na resposta
       
        localStorage.setItem("authToken", response.data.access_token);  // Vai armazenar o token no localStorage para uso futuro
        alert("Login realizado com sucesso!"); //mensagem de sucesso caso login realizado

        pagina("") //rota para onde o usuário será redirecionado quando fizer login
      } else {
        alert("Erro: Token não retornado!");
      }

      console.log("Resposta da API:", response.data);
    } catch (error) {
      // Tratar possíveis erros
      console.error("Erro ao realizar login: ", error.response?.data || error.message);
    }
  };

  return (
    <>
      <form onSubmit={EnviarDado}>
        <input type="email"  name="email" value={form.email} placeholder="Email" onChange={Mudar_valor} required />
        <input type="password"  name="password" value={form.password} placeholder="Senha" onChange={Mudar_valor} required />  
        
        <button type="submit">Logar</button>
      </form>
    </>
  );
};

export default Login;
