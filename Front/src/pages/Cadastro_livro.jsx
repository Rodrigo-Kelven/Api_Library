import React, { useState } from "react";
import Api from "./Api";
import "../statics/CadastroLivro.css";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";



const Cadastrar_Livro = () => {
  const renderizar = useNavigate();

  const [form, setForm] = useState({
    title: '',
    description: '',
    author: '',
    category: '',
    isbn: '',
    publication_date: '',
    pages: '',
  });

  const date = {
    ...form,
    pages: parseInt(form.pages, 10) || null,
  };


  const Mudar_valor = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  };

  const EnviarDado = async (e) => {
    e.preventDefault();

    try {
      const response = await Api.post("/api-library/v1/books/", date,);
      console.log("Resposta da API:", response);
      Swal.fire({
        icon: "success",
        title: "Livro cadastrado com sucesso!!",
        text: "Você será redirecionado para tela de listas de livros",
        timer: 2000,
        showConfirmButton: false,
        
      });
      setTimeout(() => {
        renderizar("/listar/livros");
      }, 2000);
    } catch (error) {
      console.error("Erro ao cadastrar: ", error.response?.data || error.message);7
      Swal.fire({
        icon: "error",
        title: "Erro ao cadastrar livro",
        text: "Usuário não logado",
        timer: 2000,
        showConfirmButton: false
      });
      setTimeout(() => {
        renderizar("/login");
      })
    }
  };

  return (
    <div className="container">
        <form className="cadastroLivroForm" onSubmit={EnviarDado}>
          <div className="container__in__form">
            <input
              className="Titulo" 
              type="text"
              name="title"
              value={form.title}
              placeholder="Título"
              onChange={Mudar_valor}
              required
            />
            <input
              className="Autor"
              type="text"
              name="author"
              value={form.author}
              placeholder="Autor"
              onChange={Mudar_valor}
              required
            />
            <input
              className="Categoria"
              type="text"
              name="category"
              value={form.category}
              placeholder="Categoria"
              onChange={Mudar_valor}
              required
            />
            <input
              className="ISBN"
              type="text"
              name="isbn"
              value={form.isbn}
              placeholder="ISBN"
              onChange={Mudar_valor}
            />
            <input
              className="Data"
              type="date"
              name="publication_date"
              value={form.publication_date}
              placeholder="Data de publicação"
              onChange={Mudar_valor}
            />
            <input
              className="Paginas"
              type="number"
              name="pages"
              value={form.pages}
              placeholder="Páginas"
              onChange={Mudar_valor}
            />

            <button type="submit">Cadastrar</button>
          </div>
        </form>
    </div>
  );
};

export default Cadastrar_Livro;