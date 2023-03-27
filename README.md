# Sample API

Sample FastAPI that loads a csv spreadsheet into a database and implements few basic endpoints. This project contains the following components:

- Postgres DB (storage)
- Liquibase (migrations)
- FastApi (REST API)

### Quick Start

#### Running Service Locally

This tutorial expects that you have docker installed locally and have understanding of how to use it. If you don't have docker installed, please follow the instructions [here](https://docs.docker.com/engine/install):

In your terminal, run the following commands:

```
docker compose up fast-api
```

#### Obtaining JWT Token

Clone this respository. The API implements basic authorization using self-signed JWT tokens. In order to obtain the JWT token, please run the following code:

```
import jwt

payload = {
    "iss": "auth_provider",
    "sub": "user"
}

encoded_jwt = jwt.encode(payload, "secret", algorithm="HS256")
```

#### Making Requests

Using the token you generated above, you can test the following requests:

<strong>List all properties</strong>

```
curl -H "Authorization":"Bearer <token>" http://localhost:5000/api/property/list
```

<strong>Get single property details</strong>

```
curl -H "Authorization":"Bearer <token>" http://localhost:5000/api/property/1001254
```

<strong>Search properties by name, neighbourhood or room type</strong>

<em>This end-point implements LIKE match and joins query parameters with AND</em>

```
curl -H "Authorization":"Bearer <token>" 'http://localhost:5000/api/property/list?name=dorm&neighbourhood=city&room_type_name=room'

```

<strong>Summary endpoint that returns number of listings and average room price by neighbourhood</strong>

```
curl -H "Authorization":"Bearer <token>" http://localhost:5000/api/property/summary
```

<strong>Update listing attributes</strong>

```
curl -X PUT http://localhost:5000/api/property/1001254 -H "Content-Type: application/json" -H "Authorization":"Bearer <token>"  -d '{"name":"updated name to test the put request"}'

```

###Documentation

Documentation can be accessed at:

```
http://localhost:5000/docs
```
