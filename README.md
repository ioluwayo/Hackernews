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

##### Libraries used and why.

These are the main libraries used. Some of them have dependencies which can be seen in requirements.txt
1. beautifulsoup4: For parsing/extracting content from html.
2. requests: For making HTTP requests
3. rfc3986: For validating URI's
4. json: For parsing python dictionaires/lists into JSON and vice-versa
5. argparse: For handling user input through the command line and displaying usage information.
6. logging: For displaying log messages during run time
