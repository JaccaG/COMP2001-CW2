Dockerhub link: https://hub.docker.com/repository/docker/jaccagoulding/trail_management_api

How to run the API through Docker

docker build -t trail_management_api .
docker login
docker tag trail_management_api jaccagoulding/trail_management_api
docker push jaccagoulding/trail_management_api


PULL AND RUN THE CONTAINER

docker pull jaccagoulding/trail_management_api
docker run -p 8000:8000 jaccagoulding/trail_management_api

EXPECTED RESPONSE

`ConnexionMiddleware.run` is optimized for development. For production, run using a dedicated ASGI server.
INFO:     Started server process [1]      
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

All users must authenticate to access protected endpoints, please use the following logins to login and get a token:
EMAIL                 PASSWORD
grace@plymouth.ac.uk	ISAD123!
tim@plymouth.ac.uk	COMP2001!
ada@plymouth.ac.uk	insecurePassword


Once you execute you will receive a token, paste just the token without the "" into the authenticate button and press authorize on swagger. 

You will now have access to the protected endpoints.
