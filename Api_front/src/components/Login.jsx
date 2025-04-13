import React, { useState } from "react";
import Api from "./Api";
import { useNavigate } from "react-router-dom";

const Login = () => {

  const pagina = useNavigate()

  const [form, setForm] = useState({
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
    const params = new URLSearchParams();
    params.append("username", form.email);  // Aqui 'username' é o email do usuário
    params.append("password", form.password);

    try {
      // Realizar a requisição POST para login
      const response = await Api.post("/api-library/v1/auth/login/", params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      // Verificar se o token foi retornado na resposta
      if (response.data.access_token) {
        // Armazenar o token no localStorage para uso futuro
        localStorage.setItem("authToken", response.data.access_token);
        alert("Login realizado com sucesso!");

        pagina("/")
      } else {
        alert("Erro: Token não retornado!");
      }

      console.log("Resposta da API:", response.data);
    } catch (error) {
      // Tratar possíveis erros
      console.error("Erro ao realizar login: ", error.response?.data || error.message);
      alert("Erro ao realizar login. Verifique as credenciais.");
    }
  };

  return (
    <>
      <form onSubmit={EnviarDado}>
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
        <button type="submit">Logar</button>
      </form>
    </>
  );
};

export default Login;
