from zeep import Client
from zeep.transports import Transport
from requests import Session
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime

# Configuración inicial del cliente SOAP
warnings.simplefilter('ignore', InsecureRequestWarning)
session = Session()
session.verify = False
transport = Transport(session=session)
wsdl_url = "http://localhost:56622/Service1.svc?wsdl"
client = Client(wsdl=wsdl_url, transport=transport)

def validate_number_input(prompt):
    while True:
        try:
            value = int(input(prompt).strip())
            if value < 0:
                raise ValueError("El valor no puede ser negativo.")
            return value
        except ValueError as e:
            print(f"Entrada inválida: {e}. Intente nuevamente.")

def validate_date_input(prompt):
    while True:
        try:
            date_input = input(prompt).strip()
            year, month, day = map(int, date_input.split("-"))
            date_obj = datetime(year, month, day)
            if date_obj > datetime.now():
                raise ValueError("La fecha no puede ser mayor que la fecha actual.")
            return date_obj.strftime("%Y-%m-%d")
        except (ValueError, IndexError) as e:
            print(f"Fecha inválida. {e} Intente nuevamente ingresando en el formato YYYY-MM-DD.")

def validate_text_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("El campo no puede estar vacío.")

def handle_soap_fault(exception):
    print(f"Error: {exception}")

def get_all_books():
    try:
        libros = client.service.GetAllLibros()
        if not libros:
            print("\nNo hay libros en la base de datos.")
            return
        print("\nLista de libros:")
        for libro in libros:
            fecha_publicacion = libro.FechaPublicacion.strftime("%Y-%m-%d") if libro.FechaPublicacion else "N/A"
            print(f"- ID: {libro.LibroID}, Título: {libro.Titulo}, Autor: {libro.Autor}, "
                  f"Editorial: {libro.Editorial}, Fecha: {fecha_publicacion}, Género: {libro.Genero}")
    except Exception as e:
        handle_soap_fault(e)

def get_book_by_id():
    try:
        book_id = validate_number_input("Ingrese el ID del libro: ")
        book = client.service.GetLibroById(book_id)
        
        if book is None or book.LibroID is None:
            print(f"El libro con ID {book_id} no existe en la base de datos.")
            return

        fecha_publicacion = book.FechaPublicacion.strftime("%Y-%m-%d") if book.FechaPublicacion else "N/A"
        print(f"Detalles del libro - ID: {book.LibroID}, Título: {book.Titulo}, Autor: {book.Autor}, "
              f"Editorial: {book.Editorial}, Fecha: {fecha_publicacion}, Género: {book.Genero}")
    except Exception as e:
        handle_soap_fault(e)

def create_book():
    try:
        title = validate_text_input("Ingrese el título del libro: ")
        author = validate_text_input("Ingrese el autor del libro: ")
        publisher = validate_text_input("Ingrese la editorial del libro: ")
        publication_date = validate_date_input("Ingrese la fecha de publicación (YYYY-MM-DD): ")
        genre = validate_text_input("Ingrese el género del libro: ")

        result = client.service.CreateLibro({
            "Titulo": title,
            "Autor": author,
            "Editorial": publisher,
            "FechaPublicacion": publication_date,
            "Genero": genre
        })
        if result:
            print("Libro creado exitosamente.")
        else:
            print("No se pudo crear el libro.")
    except Exception as e:
        handle_soap_fault(e)

def update_book():
    try:
        book_id = validate_number_input("Ingrese el ID del libro a actualizar: ")
        book = client.service.GetLibroById(book_id)
        if book is None or book.LibroID is None:
            print(f"El libro con ID {book_id} no existe en la base de datos.")
            return
        
        while True:
            print("\nSeleccione el campo que desea actualizar:")
            print("1. Título")
            print("2. Autor")
            print("3. Editorial")
            print("4. Fecha de publicación")
            print("5. Género")
            print("6. Salir")
            option = input("Ingrese una opción: ")

            if option == "1":
                book.Titulo = validate_text_input("Ingrese el nuevo título del libro: ")
            elif option == "2":
                book.Autor = validate_text_input("Ingrese el nuevo autor del libro: ")
            elif option == "3":
                book.Editorial = validate_text_input("Ingrese la nueva editorial del libro: ")
            elif option == "4":
                book.FechaPublicacion = validate_date_input("Ingrese la nueva fecha de publicación (YYYY-MM-DD): ")
            elif option == "5":
                book.Genero = validate_text_input("Ingrese el nuevo género del libro: ")
            elif option == "6":
                print("Saliendo de la actualización...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
                continue
            
            confirm = input("¿Desea realizar otra actualización en este libro? (s/n): ").strip().lower()
            if confirm != "s":
                break

        result = client.service.UpdateLibro({
            "LibroID": book.LibroID,
            "Titulo": book.Titulo,
            "Autor": book.Autor,
            "Editorial": book.Editorial,
            "FechaPublicacion": book.FechaPublicacion,
            "Genero": book.Genero
        })

        if result:
            print("Libro actualizado exitosamente.")
        else:
            print(f"No se pudo actualizar el libro con ID {book_id}.")
    except Exception as e:
        handle_soap_fault(e)

def delete_book():
    try:
        book_id = validate_number_input("Ingrese el ID del libro a eliminar: ")
        result = client.service.DeleteLibro(book_id)
        if result:
            print("Libro eliminado exitosamente.")
        else:
            print(f"No se pudo eliminar el libro con ID {book_id}.")
    except Exception as e:
        handle_soap_fault(e)

def menu():
    while True:
        print("\n************Menú de opciones************")
        print("1. Obtener todos los libros")
        print("2. Obtener un libro por ID")
        print("3. Crear un libro")
        print("4. Actualizar un libro")
        print("5. Eliminar un libro")
        print("6. Salir")
        try:
            option = int(input("\nSeleccione una opción: "))
            match option:
                case 1:
                    get_all_books()
                case 2:
                    get_book_by_id()
                case 3:
                    create_book()
                case 4:
                    update_book()
                case 5:
                    delete_book()
                case 6:
                    print("Saliendo del programa...")
                    break
                case _:
                    print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Entrada no válida. Ingrese un número entre 1 y 6.")

if __name__ == "__main__":
    menu()
