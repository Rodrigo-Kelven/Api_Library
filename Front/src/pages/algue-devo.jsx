import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import "../statics/Aluguel-Devolver.css"

const livrosMock = [
  { id: 1, title: "Dom Casmurro", author: "Machado de Assis", category: "Romance", available: true, pages: 256 },
  { id: 2, title: "O Cortiço", author: "Aluísio Azevedo", category: "Romance", available: false, pages: 320 },
  { id: 3, title: "Memórias Póstumas de Brás Cubas", author: "Machado de Assis", category: "Romance", available: true, pages: 288 },
  { id: 4, title: "Capitães da Areia", author: "Jorge Amado", category: "Ficção", available: true, pages: 224 },
  { id: 5, title: "Grande Sertão: Veredas", author: "Guimarães Rosa", category: "Literatura Brasileira", available: false, pages: 592 },

];

const ListarLivros = () => {
  const [livros, setLivros] = useState([]);

  useEffect(() => {
    setLivros(livrosMock); // Carrega os livros mock na primeira renderização
  }, []);

  const renderizar = useNavigate();

  const logout = () =>{
    localStorage.removeItem("authToken" );
    Swal.fire({
      icon: "success",
      title: "Vocẽ saiu da sua conta!!",
      text: "Você será redirecionado para tela de login",
      timer: 2000,
      showConfirmButton: false,
    })
    renderizar("/login");
  }

  const logado = localStorage.getItem("authToken") !== null;

  console.log("Usuário logado?", logado )

  const alugarLivro = (id) => {
    const atualizados = livros.map((livro) => {
      if (livro.id === id && livro.available) {
        Swal.fire({
          icon: "success",
          title: "Livro alugado",
        })
        return { ...livro, available: false };
      }
      return livro;
    });
    setLivros(atualizados);
  };

  const devolverLivro = (id) => {
    const atualizados = livros.map((livro) => {
      if (livro.id === id && !livro.available) {
        return { ...livro, available: true };
      }
      return livro;
    });
    setLivros(atualizados);
  };

  return (
    <div className="container">
      <div className="aluguelContainer">
        <h2 className="title">Livros Cadastrados</h2>
        <table className="livrosTable" border="1">
          <thead>
            <tr>
              <th>Título</th>
              <th>Autor</th>
              <th>Categoria</th>
              <th>Disponível</th>
              <th>Páginas</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {livros.length > 0 ? (
              livros.map((livro) => (
                <tr key={livro.id}>
                  <td>{livro.title}</td>
                  <td>{livro.author}</td>
                  <td>{livro.category}</td>
                  <td>{livro.available ? "Sim" : "Não"}</td>
                  <td>{livro.pages}</td>
                  <td>
                    
                    { livro.available ? ( //se validação for true ele faz o comando abaixo
                      <button className="alugar" onClick={() => {
                        if(logado){
                            alugarLivro(livro.id)
                          }else{
                            Swal.fire({
                              icon: "error",
                              title: "Usuário não logado!!",
                              text: "você sera redirecionado para a tela de login",
                              timer: 2000,
                              showConfirmButton: false,
                            }).then(setTimeout(() =>{
                              renderizar("/login"); 
                            }, 2000))
                          }                  
                      }} 
                      >Alugar</button>
                           
                           
                    ) : (
                      <button className="devolver" onClick={() => devolverLivro(livro.id)}>Devolver</button>
                    )}
                  </td>
                </tr>
              ))
            ) : ( // senão ele faz esse comando 
              <tr>
                <td colSpan="6" className="semLivros">Nenhum livro encontrado</td>
              </tr>
            )}
          </tbody>
        </table>
        <button className="logout" onClick={logout}>Sair</button>
      </div>
    </div>
  );
};

export default ListarLivros;
