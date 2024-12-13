using BLL.Logic;
using DAL;
using System;

namespace Test
{
    class Program
    {
        static void Main(string[] args)
        {
            var librosLogic = new LibrosLogic();

            // Crear un nuevo libro
            var nuevoLibro = new Libros
            {
                Titulo = "Cien años de soledad",
                Autor = "Gabriel García Márquez",
                Editorial = "Sudamericana",
                FechaPublicacion = new DateTime(1999, 6, 5),
                Genero = "Realismo mágico"
            };
            librosLogic.Create(nuevoLibro);
            Console.WriteLine("Libro creado con éxito.");

            // Obtener todos los libros
            var libros = librosLogic.RetrieveAll();
            foreach (var libro in libros)
            {
                Console.WriteLine($"{libro.LibroID} - {libro.Titulo} ({libro.Autor})");
            }
        }
    }
}
