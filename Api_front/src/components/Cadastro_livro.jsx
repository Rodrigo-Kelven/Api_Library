import React, {useState} from "react";
import Api from "./Api";
import "../statics/CadastroLivro.css";

const Cadastrar_Livro = () => {
     const [form, setForm] = useState({
          title: '',
          description: '',
          author: '',
          category: '',
          isbn:'',
          publication_date:'',
          pages:'',
     });

     const date = {
          ...form,
          pages: parseInt(form.pages, 10) || null,
     };

   
     const Mudar_valor = (e) => {
          setForm({...form, [e.target.name]: e.target.value})
     };

     const EnviarDado = async (e) =>{
          e.preventDefault();

          try{
               const response = await Api.post("/api-library/v1/books/", date, {
                    headers: {
                         "Content-Type": "application/json"
                    }
               });
               console.log("Resposta da API:", response);
               alert("Usuário cadastrado com sucesso!!!")
          }catch(error){
               console.error("Erro ao cadastrar: ", error.response?.data || error.message);
          }



     };

     return (
          <div className="cadastroLivroContainer">
            <form className="cadastroLivroForm" onSubmit={EnviarDado}>
              <input
                type="text"
                name="title"
                value={form.title}
                placeholder="Título"
                onChange={Mudar_valor}
                required
              />
              <textarea
                name="description"
                value={form.description}
                placeholder="Descrição"
                onChange={Mudar_valor}
              ></textarea>
              <input
                type="text"
                name="author"
                value={form.author}
                placeholder="Autor"
                onChange={Mudar_valor}
                required
              />
              <input
                type="text"
                name="category"
                value={form.category}
                placeholder="Categoria"
                onChange={Mudar_valor}
                required
              />
              <input
                type="text"
                name="isbn"
                value={form.isbn}
                placeholder="ISBN"
                onChange={Mudar_valor}
              />
              <input
                type="date"
                name="publication_date"
                value={form.publication_date}
                placeholder="Data de publicação"
                onChange={Mudar_valor}
              />
              <input
                type="number"
                name="pages"
                value={form.pages}
                placeholder="Páginas"
                onChange={Mudar_valor}
              />
      
              <button type="submit">Cadastrar</button>
            </form>
          </div>
        );
      };
      
      export default Cadastrar_Livro;