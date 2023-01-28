# Deuthsche Bahn
Deutsche Bahn

## Build Docker image
- Start Docker Desktop
- Build image
``` batch
docker build -t local-mysql . docker run --name my_postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres
```
- Run container
``` batch
docker run -dp 3307:3307 local-mysql
```