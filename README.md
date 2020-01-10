### Hackernews

##### To build and run container.

From within the root directory, execute the following commands
```
docker build -t hackernews:latest .
docker run --name hackernews -d hackernews
```
##### To run/test the application

1. ssh into the container.```docker exec -it hackernews```
2. To run tests, from within the /Hackernews directory execute commad ```python -m unittest test_hackernews.py -v``` 
3. To run the application, from anywhere in the container, execute command ```hackernews --posts n```
4. To display help message, execute  ```hackernews --help```
