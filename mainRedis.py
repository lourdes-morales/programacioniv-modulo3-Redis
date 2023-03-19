import redis
import sys

try:
    #MÉTODO PARA ESTABLECER CONEXION A REDIS
    def connect_to_redis():
        r = redis.Redis(host='localhost', port=6379, db=0)
        return r
    #MÉTODO PARA CREAR DOCUMENTO
    def create_document(connection, key, document):
        result = connection.set(key, document)
        print("Document created with key:", key)
    #MÉTODO PARA AGREGAR PALABRA
    def add_word(connection, word, meaning):
        key = "word:" + word.lower()
        document = meaning
        create_document(connection, key, document)
    #MÉTODO PARA EDITAR PALABRA
    def edit_word(connection, word, new_meaning):
        key = "word:" + word.lower()
        connection.set(key, new_meaning)
        print(f"Palabra actualizada: {word}")
    #MÉTODO PARA ELIMINAR PALABRA
    def remove_word(connection, word):
        key = "word:" + word.lower()
        connection.delete(key)
        print(f"Palabra eliminada: {word}")
    #MÉTODO PARA OBTENER TODAS LAS PALABRAS
    def get_words(connection):
        keys = connection.keys("word:*")
        return [key.decode('utf-8').split(":")[1] for key in keys]
    #MÉTODO PARA OBTENER SIGNIFICADO DE UNA PALABRA
    def get_meaning(connection, word):
        key = "word:" + word.lower()
        meaning = connection.get(key)
        if meaning is not None:
            return meaning.decode('utf-8')
        else:
            return None
    #MÉTODO PRINCIPAL CON MENÚ Y CONDICIONES
    def principal():
        connection = connect_to_redis()
        menu = """
    __________________________________________
            DICCIONARIO DE SLANG PANAMEÑO
    a) Agregar nueva palabra
    b) Editar palabra existente
    c) Eliminar palabra existente
    d) Ver listado de palabras
    e) Buscar significado de palabra
    f) Salir
    __________________________________________
    Selecciona una opción: """

        option = ""
        while option != "f":
            option = input(menu).lower()
            if option == "a":
                word = input("Ingresa la palabra: ")
                possible_meaning = get_meaning(connection, word)
                if possible_meaning:
                    print(f"La palabra '{word}' ya existe")
                else:
                    meaning = input("Ingresa el significado: ")
                    add_word(connection, word, meaning)
                    print(f"Palabra agregada: {word}")
            if option == "b":
                word = input("Ingresa la palabra que quieres editar: ")
                new_meaning = input("Ingresa el nuevo significado: ")
                edit_word(connection, word, new_meaning)
            if option == "c":
                word = input("Ingresa la palabra a eliminar: ")
                remove_word(connection, word)
            if option == "d":
                words = get_words(connection)
                print("=== Lista de palabras ===")
                for word in words:
                    print(word)
            if option == "e":
                word = input("Ingresa la palabra de la cual quieres saber el significado: ")
                meaning = get_meaning(connection, word)
                if meaning:
                    print(f"El significado de '{word}' es: {meaning}")
                else:
                    print(f"Palabra '{word}' no encontrada")
        else:
            print("\nEl programa ha finalizado")
            sys.exit()

    if __name__ == '__main__':
        principal()

#MANEJO DE EXCEPCIONES
except ValueError:
    print("ExceptionError - ValueError: Database not connected")
except TypeError:
    print("ExceptionError - TypeError: Database not connected")
except TimeoutError:
    print("ExceptionError - Timeout: Database not connected")

finally:
    connection = connect_to_redis()
    connect_to_redis().close