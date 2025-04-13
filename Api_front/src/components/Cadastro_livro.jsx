import React, {useState} from "react";
import Api from "./Api";

const Criar_user = () => {
     const [form, setForm] = useState({
          title: '',
          description: '',
          author: '',
          category: '',
          isbn:'',
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
               const response = await Api.post("/api-library/v1/auth/users/", formData);
               console.log("Resposta da API:", response);
               alert("Usuário cadastrado com sucesso!!!")
          }catch(error){
               console.error("Erro ao cadastrar: ", error.response?.data || error.message);
          }



     };

     return(
          <>
               <form onSubmit={EnviarDado}>
                    <input type="text" name="username" value={form.username} placeholder="Digite seu nome" onChange={Mudar_valor} required/>
                    <input type="email" name="email" value={form.email} placeholder="email" onChange={Mudar_valor} required />
                    <input type="text" name="full_name" placeholder="Nome completo" value={form.full_name} onChange={Mudar_valor} required />
                    <input type="password" name="password" value={form.password} placeholder="Senha" onChange={Mudar_valor} required />

                    <button type="submit">Cadastrar</button>
               </form>     
          </>
     )

}

export default Criar_user;