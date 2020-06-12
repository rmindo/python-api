# Python RESTful API

Python-Flask RESTful API with MySQL


### Run docker with separate container

##### Create Network
Create docker network api 
```
$ docker network create -d bridge api
```

##### MySQL Container
Run mysql in a network api with MYSQL_ROOT_PASSWORD and MYSQL_ROOT_HOST specified.
```
$ docker pull mysql
```
```
$ docker run --network=api --name=mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=demo -e MYSQL_ROOT_HOST=% mysql
```


##### Flask API Container
Run a separate container with public port 2000 in a network api

```
$ docker pull rmindo/python-api
```
```
$ docker run --rm -it -p 2000:80 --network=api --name=api -v /$(pwd):/www/api rmindo/python-api
```

### Run with docker-compose
Create a docker-compose.yml and copy the configuration below.
```
version: '3.7'

services:
  mysql:
    image: mysql:latest
    restart: always
    container_name: mysql
    ports:
      - 3306:3306
    networks:
      - api
    environment:
      MYSQL_USER: root
      MYSQL_ROOT_HOST: '%'
      MYSQL_PASSWORD: demo
      MYSQL_DATABASE: demo
      MYSQL_ROOT_PASSWORD: demo
    command: --default-authentication-plugin=mysql_native_password
  api:
    image: rmindo/python-api
    restart: always
    container_name: api
    ports:
      - 2000:80
    volumes:
      - ./:/www/api
    networks:
      - api
    links:
      - mysql
    environment:
      DB_HOST: mysql
      DB_USER: root
      DB_NAME: demo
      DB_PASSWORD: demo

networks:
  api:
    driver: bridge
```

##### Run docker-compose containers
```
$ docker-composer up
```

### Authorization
HTTP header request should have authorization field with token generated from GET /api/v1/init
```
{
    "Authorization": "Bearer {API_TOKEN_HERE}"
}
```

### API Endpoints

##### Init
Initialize database and generate token
- GET /api/v1/init

##### Users
- POST /api/v1/users
- GET /api/v1/users
- GET /api/v1/users/{user_id}
- PUT /api/v1/users/{user_id}
- DELETE /api/v1/users/{user_id}

##### Contacts
- GET /api/v1/users/{user_id}/contacts
- POST /api/v1/users/{user_id}/contacts
- GET /api/v1/users/{user_id}/contacts/{contact_id}
- PUT /api/v1/users/{user_id}/contacts/{contact_id}
- DELETE /api/v1/users/{user_id}/contacts/{contact_id}

##### Addresses
- GET /api/v1/users/{user_id}/contacts/{contact_id}/addresses
- POST /api/v1/users/{user_id}/contacts/{contact_id}/addresses
- GET /api/v1/users/{user_id}/contacts/{contact_id}/addresses/{address_id}
- PUT /api/v1/users/{user_id}/contacts/{contact_id}/addresses/{address_id}
- DELETE /api/v1/users/{user_id}/contacts/{contact_id}/addresses/{address_id}



### Response Status Code
```
200: Ok
201: Created
400: Bad Request
401: Unauthorized
403: Forbidden
404: Not Found
405: Method Not Allowed
406: Not Acceptable
409: Conflict
500: Internal Server Error
```

### Add New Routes
##### Configuration
Configuration file is located at /src/config.py
```
config = {
  'resource': [
    {
      'users': {
        'var': 'string:id',
        'extra': [
          ['GET', '/init', 'init', True]
        ]
      },
      'contacts': {
        'pass': True,
        'var': 'string:key'
      },
    },
  ]
}
```

##### Resource Fields
| Field Name         | Description                                                       | Required          |
|--------------------|-------------------------------------------------------------------|-------------------|
| var                | Variable rule of the path /resource/\<string:id\>                 | true              |
| pass               | Pass through without authentication including single item.        | false             |
| extra              | Extra routes from a resource                                      | false             |

##### Extra Field
Method, Path, Function, Pass Through
```
['GET', '/init', 'init', True]
```



### Database Schema
##### Parent table users
```
CREATE TABLE IF NOT EXISTS `users` (
  `id`        	   INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `firstname`		   VARCHAR(50) DEFAULT NULL,
  `lastname`		   VARCHAR(50) DEFAULT NULL,
  `title`	         VARCHAR(50) DEFAULT NULL,
  `gender`	       VARCHAR(1)  DEFAULT NULL,
  `dateofbirth`	   VARCHAR(10) DEFAULT NULL,
  `auth`	         JSON  DEFAULT NULL,
  `datecreated` 	 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `datemodified`   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
```
##### Child table contacts
```
CREATE TABLE IF NOT EXISTS `contacts` (
  `id`        	   INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user`		       INT(11) DEFAULT NULL,
  `type`		       VARCHAR(20) DEFAULT NULL,
  `value`		       VARCHAR(20) DEFAULT NULL,
  `preferred`	     BOOLEAN DEFAULT 0,
  `datecreated` 	 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `datemodified`   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `contacts` (`id`,`user`),
  FOREIGN KEY (user) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
```
##### Child table addresses
```
CREATE TABLE IF NOT EXISTS `addresses` (
  `id`        	   INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user`		       INT(11) DEFAULT NULL,
  `number`		     INT(20) DEFAULT NULL,
  `type`		       VARCHAR(20) DEFAULT NULL,
  `street`	       VARCHAR(50) DEFAULT NULL,
  `unit`	         VARCHAR(50) DEFAULT NULL,
  `city`	         VARCHAR(50) DEFAULT NULL,
  `state`	         VARCHAR(50) DEFAULT NULL,
  `zipcode`	       VARCHAR(50) DEFAULT NULL,
  `datecreated` 	 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `datemodified`   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `addresses` (`id`,`user`),
  FOREIGN KEY (user) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
```


### Diagram
<p align="center">
	<img width="600" src="https://i.ibb.co/R2cPg12/Schema-Design.png">
</p>
