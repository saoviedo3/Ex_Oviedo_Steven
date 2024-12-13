using System.Collections.Generic;
using System.ServiceModel;
using DAL; 

namespace SOAPService
{
    [ServiceContract] 
    public interface ILibrosService
    {
        [OperationContract] 
        List<Libros> GetAllLibros();

        [OperationContract]
        Libros GetLibroById(int id);

        [OperationContract]
        bool CreateLibro(Libros libro);

        [OperationContract]
        bool UpdateLibro(Libros libro);

        [OperationContract]
        bool DeleteLibro(int id);
    }
}
