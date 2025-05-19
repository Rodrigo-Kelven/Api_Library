import React, { useEffect, useState } from "react";
import Api from "./Api"; // Instância do axios

const ListarLivros = () => {
  const [livros, setLivros] = useState([]);
  const [filtros, setFiltros] = useState({
    title: "",
    author: "",
    category: "",
    available: "", // string: "", "true", "false"
  });
  const [skip, setSkip] = useState(0);
  const limit = 5; // quantidade de livros por página

  const buscarLivros = async () => {
    try {
      let available

      if(filtros.available === ""){
        available = undefined
      }else{
        available = filtros.available === "true";
      }

      const params = {
        ...filtros,
        skip,
        limit,
        available,
      };

      console.log("🔍 Enviando para a API:", params);
      const response = await Api.get("/api-library/v1/books/search-filters/", {
        params,
      });

      console.log("📦 Resposta da API:", response.data);
      setLivros(response.data);
    } catch (error) {
      console.error("❌ Erro ao buscar livros:", error);
    }
  };

  useEffect(() => {
    buscarLivros();
  }, [skip]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFiltros({ ...filtros, [name]: value });
  };

  const aplicarFiltros = () => {
    setSkip(0); // volta para a primeira página ao filtrar
    buscarLivros();
  };

  const paginaAtual = skip / limit + 1;

  return (
    <div style={{ padding: "20px" }}>
      <h2>📚 Livros Cadastrados</h2>

      <div style={{ marginBottom: "10px" }}>
        <input
          type="text"
          name="title"
          placeholder="Título"
          value={filtros.title}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="author"
          placeholder="Autor"
          value={filtros.author}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="category"
          placeholder="Categoria"
          value={filtros.category}
          onChange={handleInputChange}
        />
        <select
          name="available"
          value={filtros.available}
          onChange={handleInputChange}
        >
          <option value="">Todos</option>
          <option value="true">Disponível</option>
          <option value="false">Indisponível</option>
        </select>
        <button onClick={aplicarFiltros}>Filtrar</button>
      </div>

      <table border="1" style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Título</th>
            <th>Autor</th>
            <th>Categoria</th>
            <th>Disponível</th>
            <th>Páginas</th>
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
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5" style={{ textAlign: "center" }}>
                Nenhum livro encontrado
              </td>
            </tr>
          )}
        </tbody>
      </table>

      <div style={{ marginTop: "20px" }}>
        <button
          onClick={() => setSkip((prev) => Math.max(prev - limit, 0))}
          disabled={skip === 0}
        >
          Anterior
        </button>
        <span style={{ margin: "0 10px" }}>Página {paginaAtual}</span>
        <button
          onClick={() =>
            livros.length < limit
              ? null
              : setSkip((prev) => prev + limit)
          }
          disabled={livros.length < limit}
        >
          Próxima
        </button>
      </div>
    </div>
  );
};

export default ListarLivros;
