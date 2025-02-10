# ML Software Engineer Technical Challenge

## General
This demo api downloads the top ten profiles from the stack overflow api.  For each user it than attempts to retrieve
the users profile image to run image detection processing looking for the object supplied by the user in the query
parameter.

## Prerequisites
- Python 3.12 or later.
- [Poetry](https://python-poetry.org/) installed and working.

## Setting up the project
Once the project is cloned or the zip file expanded enter the project directory and install the project dependencies.

```shell
poetry install
```

## Running the API
After the dependencies are installed the project can be run with the following.

```shell
poetry run app
```

The api can then be accessed at http://localhost:8080 and the api documentation
can be accessed at http://localhost:8080/docs

## Next Steps
- Look into FastAPI error handling to follow prescribed patterns better.
- Look for a better library for managing object detection.  Ultralytics while easy to use has some rough edges that are gotcha points
- Add api endpoint for user to check if the object they want to detect is supported.
