import React from 'react';
import { BookOpen } from 'lucide-react';
import '../statics/home.css';

const Home = () => {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto py-4 px-4 flex justify-between items-center">
          <a href="/" className="flex items-center gap-2 font-bold text-xl">
            <BookOpen className="h-6 w-6" />
            <span>BiblioTech</span>
          </a>

          <div className="hidden md:flex items-center gap-6">
            <a href="/livros" className="hover:text-primary">
              Livros
            </a>
            <a href="/categorias" className="hover:text-primary">
              Categorias
            </a>
            <a href="/autores" className="hover:text-primary">
              Autores
            </a>
            <a href="/sobre" className="hover:text-primary">
              Sobre
            </a>
          </div>

          <button className="Button outline" href="/entrar">
            Entrar
          </button>
        </div>
      </header>

      <main className="flex-1 flex items-center justify-center bg-slate-50">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-2xl mx-auto text-center">
            <h1 className="text-3xl md:text-5xl font-bold mb-6">Bem-vindo à BiblioTech</h1>
            <p className="text-slate-600 text-lg mb-8">
              Sua biblioteca digital com milhares de títulos disponíveis para empréstimo. Explore nosso acervo e
              descubra novos mundos através da leitura.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="Button" href="/livros">
                Explorar Acervo
              </button>
              <button className="Button outline" href="/sobre">
                Sobre Nós
              </button>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-slate-100 py-6">
        <div className="container mx-auto px-4 text-center text-slate-600 text-sm">
          <p>© 2023 BiblioTech. Todos os direitos reservados.</p>
          <div className="flex justify-center gap-4 mt-2">
            <a href="/termos" className="hover:text-primary">
              Termos
            </a>
            <a href="/privacidade" className="hover:text-primary">
              Privacidade
            </a>
            <a href="/contato" className="hover:text-primary">
              Contato
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Home;