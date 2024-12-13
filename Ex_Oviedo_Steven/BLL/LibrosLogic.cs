using System;
using System.Collections.Generic;
using System.Linq;
using DAL;

namespace BLL.Logic
{
    public class LibrosLogic
    {
        private readonly Sales_DBEntities _context;

        public LibrosLogic()
        {
            _context = new Sales_DBEntities();
        }

        public List<Libros> RetrieveAll()
        {
            return _context.Libros.ToList();
        }

        public Libros RetrieveById(int id)
        {
            return _context.Libros.FirstOrDefault(l => l.LibroID == id);
        }

        public bool Create(Libros libro)
        {
            try
            {
                _context.Libros.Add(libro);
                _context.SaveChanges();
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        public bool Update(Libros libro)
        {
            try
            {
                var existingLibro = _context.Libros.FirstOrDefault(l => l.LibroID == libro.LibroID);
                if (existingLibro == null) return false;

                existingLibro.Titulo = libro.Titulo;
                existingLibro.Autor = libro.Autor;
                existingLibro.Editorial = libro.Editorial;
                existingLibro.FechaPublicacion = libro.FechaPublicacion;
                existingLibro.Genero = libro.Genero;

                _context.SaveChanges();
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        public bool Delete(int id)
        {
            try
            {
                var libro = _context.Libros.FirstOrDefault(l => l.LibroID == id);
                if (libro == null) return false;

                _context.Libros.Remove(libro);
                _context.SaveChanges();
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }
    }
}
