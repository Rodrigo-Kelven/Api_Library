import React, {useState} from "react";
import Api from "./Api";
import "../statics/CreateUser.css";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";


const Criar_user = () => {
     const [form, setForm] = useState({
          username: '',
          email: '',
          full_name: '',
          password: '',
     });

     const Mudar_valor = (e) => {
          setForm({...form, [e.target.name]: e.target.value})
     };

     const EnviarDado = async (e) =>{
          e.preventDefault();

          const formData = new FormData();
          formData.append("username", form.username);
          formData.append("email", form.email);
          formData.append("full_name", form.full_name);
          formData.append("password", form.password);

          try{
               const response = await Api.post("/api-library/v1/auth/user/register/", formData);
               console.log("Resposta da API:", response);
               alert("Usuário cadastrado com sucesso!!!")
          }catch(error){
               console.error("Erro ao cadastrar: ", error.response?.data || error.message);
          }



     };

     return (
        <>
          <div className="container">
            
              <form className="createUserForm" onSubmit={EnviarDado}>
                <h1 className="Cadastro">Cadastro</h1>
                <input
                  type="text"
                  name="username"
                  value={form.username}
                  placeholder="Digite seu nome de usuário"
                  onChange={Mudar_valor}
                  required
                />
                <input
                  type="email"
                  name="email"
                  value={form.email}
                  placeholder="Digite seu email"
                  onChange={Mudar_valor}
                  required
                />
                <input
                  type="text"
                  name="full_name"
                  value={form.full_name}
                  placeholder="Digite seu nome completo"
                  onChange={Mudar_valor}
                  required
                />
                <input
                  type="password"
                  name="password"
                  value={form.password}
                  placeholder="Digite sua senha"
                  onChange={Mudar_valor}
                  required
                />

                <button type="submit">Cadastrar</button>
              </form>
          </div>
        </>
      );

}

export default Criar_user;