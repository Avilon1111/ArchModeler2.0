Как запустить проект:
1) Склонировать проект
2) Запустить БД через терминал:
docker run -e ARANGO_RANDOM_ROOT_PASSWORD=1 -p 8529:8529 -d --name ArchModeler-arangodb arangodb
3) Узнать пароль от БД:
docker logs --details ArchModeler-arangodb
Пароль находится сверху логов
4) Зайти в БД:
http://localhost:8529/
username: root
password: {пароль из логов из 3 пункта}
5) Запустить API из директории Backend:
uvicorn app:app --reload --port 5259
