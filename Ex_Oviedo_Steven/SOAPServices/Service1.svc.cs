using System.Collections.Generic;
using BLL.Logic;
using DAL;

namespace SOAPService
{
    public class Service1 : IService1
    {
        private readonly LibrosLogic _librosLogic;

        public Service1()
        {
            _librosLogic = new LibrosLogic();
        }

        public List<Libros> GetAllLibros()
        {
            return _librosLogic.RetrieveAll();
        }

        public Libros GetLibroById(int id)
        {
            return _librosLogic.RetrieveById(id);
        }

        public bool CreateLibro(Libros libro)
        {
            return _librosLogic.Create(libro);
        }

        public bool UpdateLibro(Libros libro)
        {
            return _librosLogic.Update(libro);
        }

        public bool DeleteLibro(int id)
        {
            return _librosLogic.Delete(id);
        }
    }
}
