from uuid import uuid4
from fastapi import FastAPI, Form, Body, status
from fastapi.responses import JSONResponse


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.id = str(uuid4())


# условная база данных - набор объектов Person
people = [Person("Tom", 38),
          Person("Bob", 42),
          Person("Sam", 28)
          ]


# для поиска пользователя в списке people
def find_person(id):
    for person in people:
        if person.id == id:
            return person
    return None


app = FastAPI()


@app.get("/")
async def main():
    return ("Список пользователей")


@app.get("/api/users")
def get_people():
    return people


@app.get("/api/users/{id}")
def get_person(id):
    # получаем пользователя по id
    person = find_person(id)
    print(person)
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )
    # если пользователь найден, отправляем его
    return person


@app.post("/create")
def create_person(username: str = Form(""), age: int = Form()):
    person = Person(username, age)
    # добавляем объект в список people
    people.append(person)
    return person


@app.put("/api/users")
def edit_person():
    # получаем пользователя по id
    person = find_person(data["id"])
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    person.age = data["age"]
    person.name = data["name"]
    return person


@app.delete("/api/users/{id}")
def delete_person(id):
    # получаем пользователя по id
    person = find_person(id)

    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )

    # если пользователь найден, удаляем его
    people.remove(person)
    return person