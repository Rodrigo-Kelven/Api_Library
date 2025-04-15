import React, { useState } from "react";
import Api from "./Api";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import "../statics/Login.css"

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
          "Content-Type": "application/x-www-form-urlencoded",  //diz queDevo_aluga os dados serão passados no cabeçalhos em vez da url do site
        },

      });

      
      if (response.data.access_token) { // Ve se o token foi retornado na resposta
       
        localStorage.setItem("authToken", response.data.access_token);  // Vai armazenar o token no localStorage para uso futuro
          Swal.fire({
            icon: "success",  
            title: "Login realizado com sucesso!!",
            timer: 2000,
            showConfirmButton: false,
          })//mensagem de sucesso caso login realizado

          setTimeout(() =>{
            pagina("/Devo_aluga");

          }, 2000); //rota para onde o usuário será redirecionado quando fizer login
      } else {
        
           Swal.fire({
            icon: "error",  
            title: "Login não realizado!!",
            timer: 2000,
            showConfirmButton: false,
          })
      }

      console.log("Resposta da API:", response.data);
    } catch (error) {
      // Tratar possíveis erros
      console.error("Erro ao realizar login: ", error.response?.data || error.message);
    }
  };

  return (
    <>
      <div className="login_container">
   
        <form className="login_form" onSubmit={EnviarDado}>
          <h1 className="title">Login</h1>
          <input
            type="email"
            name="email"
            value={form.email}
            placeholder="Email"
            onChange={Mudar_valor}
            required
          />
          <input
            type="password"
            name="password"
            value={form.password}
            placeholder="Senha"
            onChange={Mudar_valor}
            required
          />
          <div className="container_n_conta">
            <p className="p">Não tem conta?</p>
            <a className="n_conta" href="/cadastro">Cadastre-se Aqui</a>
          </div>
          <button type="submit">Logar</button>
        </form>
      </div>
    </>
  );
};

export default Login;
