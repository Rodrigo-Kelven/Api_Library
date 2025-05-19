import React, { useEffect, useState } from "react";
import "../statics/Aluguel-Devolver.css"

const livrosMock = [
  { id: 1, title: "Dom Casmurro", author: "Machado de Assis", category: "Romance", available: true, pages: 256 },
  { id: 2, title: "1984", author: "George Orwell", category: "Ficção", available: true, pages: 328 },
  { id: 3, title: "O Pequeno Príncipe", author: "Saint-Exupéry", category: "Fábula", available: true, pages: 96 },
];

const ListarLivros = () => {
  const [livros, setLivros] = useState([]);
  const [filtros, setFiltros] = useState({
    title: "",
    author: "",
    category: "",
    available: "",
  });

  useEffect(() => {
    buscarLivros();
  }, []);

  const buscarLivros = () => {
    let resultado = livrosMock;

    if (filtros.title) {
      resultado = resultado.filter((livro) =>
        livro.title.toLowerCase().includes(filtros.title.toLowerCase())
      );
    }

    if (filtros.author) {
      resultado = resultado.filter((livro) =>
        livro.author.toLowerCase().includes(filtros.author.toLowerCase())
      );
    }

    if (filtros.category) {
      resultado = resultado.filter((livro) =>
        livro.category.toLowerCase().includes(filtros.category.toLowerCase())
      );
    }

    if (filtros.available !== "") {
      resultado = resultado.filter(
        (livro) => livro.available === (filtros.available === "true")
      );
    }

    setLivros(resultado);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFiltros({ ...filtros, [name]: value });
  };

  const aplicarFiltros = () => {
    buscarLivros();
  };

  const alugarLivro = (id) => {
    const atualizados = livros.map((livro) => {
      if (livro.id === id && livro.available) {
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
    <div>
      <h2>Livros Cadastrados</h2>

      <div style={{ marginBottom: "20px" }}>
        <input type="text" name="title" placeholder="Título" value={filtros.title} onChange={handleInputChange} />
        <input type="text" name="author" placeholder="Autor" value={filtros.author} onChange={handleInputChange} />
        <input type="text" name="category" placeholder="Categoria" value={filtros.category} onChange={handleInputChange} />
        <select name="available" value={filtros.available} onChange={handleInputChange}>
          <option value="">Todos</option>
          <option value="true">Disponível</option>
          <option value="false">Indisponível</option>
        </select>
        <button onClick={aplicarFiltros}>Filtrar</button>
      </div>

      <table border="1" style={{ width: "100%" }}>
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
                  {
                    (() => {
                      if (livro.available) {
                        return <button onClick={() => alugarLivro(livro.id)}>Alugar</button>;
                      } else {
                        return <button onClick={() => devolverLivro(livro.id)}>Devolver</button>;
                      }
                    })()
                  }
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6">Nenhum livro encontrado</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ListarLivros;
