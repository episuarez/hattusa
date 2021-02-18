# Hattusa

Hattusa is a multi-format book reader.
Currently it can read EPUB, PDF, CBZ and CBR. More formats will be available in the future.

The application is a web application developed in Python on top of Flask.

At this moment contributions are not accepted yet.

## How to install it?

The first option is to upload it to any web server that can serve flask web pages.
```
gunicorn --bind 0.0.0.0.0:5000 main:app
```

And the second option is to compile the Docker image that is in the same repository or use the image uploaded to the docker hub https://hub.docker.com/r/owaristudios/hattusa.

## Application details

The important path of the same are:
* /books - Reading directory of the books
* /app.log - Log of the application

These paths will be inside /app in the case of the Docker image.

## More information

* You can open an issue at https://github.com/OwariStudios/Hattusa/issues
* And you can open a discussion at https://github.com/OwariStudios/Hattusa/discussions

## List of functions under development

- [X] Read EPUB
- [X] Read PDF
- [ ] Read MOBI
- [X] Read CBZ
- [X] Read CBR
- [ ] Homogenize reading with the same format, regardless of the book.
- [ ] Read only available pages
- [ ] Grouping by tags or equivalent
- [ ] Recursive traversal of the library
- [X] Create a beautiful interface
- [ ] Improve speed
- [ ] Save reading position
- [ ] Dark mode
- [ ] User management
- [ ] Image creation for Docker
- [ ] Executable creation for Windows, Linux and Mac

## Screenshot
<img src="https://raw.githubusercontent.com/OwariStudios/Hattusa/main/screenshot01.jpg?raw=true" alt="Hattusa"/>
<img src="https://raw.githubusercontent.com/OwariStudios/Hattusa/main/screenshot02.jpg?raw=true" alt="Hattusa"/>
