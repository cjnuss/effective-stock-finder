# Description
This program utilizes daily SEC filings to predict stocks that can go up in the future.

# Set up
To run the code, you need to follow these steps:

**1. Install Docker from:** 
```
https://www.docker.com/products/docker-desktop/
```

**2. After installing Docker, clone this repository and open up a terminal at the folder.**

**3. Now cd into the main-project folder by running the following command:**
```
cd main-project
```

**4. Once you are in the main-project folder, start Docker desktop and run the following command to install all required libraries:**
```
docker compose up --build
```

**5. Wait about a minute or two for everything to start running.**

**6. Next go to the following link in your web browser:**
```
http://127.0.0.1:5000
```

**7. To close the program run the following command**
```
docker compose up --down
```

**To update the data being used for predictions manually, you can follow the following steps:**

**7. Open the docker-compose.yaml and change the command from python3 src/main.py to python3 src/tsvGenerator.py**

**8. Run the command from step 4 and wait a 20-30 minutes for data to update.**

**9. Once the program ends, follow step 7 to close the program.**

**10. Next, change the docker-compose.yaml command back to python3 src/main.py.**

**11. Finally, follow the instructions from steps 4-7 to run the program with updated data!**


