# URL Shortner

This is service is used to create a shorter version of a given URL.
**Currently this service only works locally.**

## Local Setup

### MySQL 8.0.18
1. Docker image: `docker pull mysql/mysql-server:8.0.18`
2. Run the image: `docker run --name=mysql1 -v <path_on_host>:/var/lib/mysql -d  mysql/mysql-server:8.0.18`
	- `-v <path_on_host>:/var/lib/mysql`: Is to keep the data persistent when container restarts.
3. Get default root pass: `docker logs mysql1 2>&1 | grep GENERATED`
4. Get a terminel into the container: `docker exec -it mysql1 mysql -u root -p`	
5. Create database: `CREATE DATABASE url_shortner;`
6. Switch to the DB: 'USE url_shortner;'
7. Create user the database: `CREATE USER 'url_shortner'@'%' IDENTIFIED BY 'pass';`
8. Allow remote connections for the user: `GRANT ALL PRIVILEGES ON *.* TO 'url_shortner'@'%';`
9. Create table: ```CREATE TABLE urls (
	id int NOT NULL AUTO_INCREMENT,
	hash varchar(1000) NOT NULL,
	url varchar(1000),
	PRIMARY KEY (id)
	);```

### Application

1. Clone this repo.
2. Build the docker image: `docker build -t url_shortner:1.0 .`
3. Run the image: `docker run -d -p 8888:8888 url_shortner:1.0`
4. Open `http://localhost:8888` in the browser.

## Application End Points

1. `/`
	- Method: GET
	- Params: N/A
	- Response: Html form to generate short url.
2. `/health`
	- Method: GET
	- Params: N/A
	- Response: 200/OK
3. `/GenerateShortUrl`
	- Method: POST
	- Params: 
		- `url`: The URL that needs to be cut short.
	- Response: Hash of the url
4. `/<url_hash>`
	- Method: GET
	- Params: N/A
	- Response: 302 redirect to the original URL.

## Design

### URL to hash mechanism

1. The orignal url is stored in the DB.
2. The auto generated Integer ID (base10) for the column is hashed using `python-baseconv.base62`.
	- Hashing the url directly using algorigthm like md5 generates long string which defeats the purpose
	- The Integer ID will eventually become a large number, so using that is not good either.

### Hash to URL mechanism

1. The hash (base62) is decoded to Int (base10).
2. The Int is the ID to look up the orignal URL.
