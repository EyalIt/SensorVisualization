# SensorVisualization

This is a client-server application with the following abilities:
  1. Client:
     The client activates 4 sensors, each of them sample a different characteristic of the PC every 100ms.
     There are 4 types of sensors - context switch sensor, interrupts sensor, process IDs sensor and network connections sensor.
     Once the sensor gets a new sample it sends the data to the server
     
  2. Server:
     1. BE side:
        The server receives new requests with sensor data from multiple clients. 
        It differentiate the clients according to ip address.
        Each sample is saved to a database, which stores the samples on a daily collection. 
        Every 24 hours it activates an auto-backup process, zips the daily collection and stores it in an S3 storage.
        The data can be queried using and html web page.
     2. FE side:
        In order to query the database, there is a web page stored at http://localhost:8000/query_sensors/.
        The web page contains a few drop-down lists for selecting client ID and sensor type.
        Once "generate graph" button is selected, a histogram of the sensor values from the specific client is extracted 
        from the database and displayed.
        
        
In order to run the appliaction locally:
  1. run mongoDb 
  2. make sure the mongodump executable is located under "C:\Program Files\MongoDB\Server\3.4\bin"
  3. add python path to your environment variables
  4. set the environment variables that contain the AWS secret key. not going to write them here :-)  
  5. run "python main.py"
  

In order to run the clients locally and connect to a remote server:
  1. in "main.py" file change the following:
    1. In main function, change url to be "ec2-13-58-140-57.us-east-2.compute.amazonaws.com"
    2. Activate the client only by commenting out "initiate_server" 
    3. In order to view the histogram web page, go the the following URL - 
       http://ec2-13-58-140-57.us-east-2.compute.amazonaws.com:8000/query_sensors/ 


Future Enhancements:
  1. Aggregate a few samples and send them to the server as a batch
  2. Zip the data that is sent to the server to reduce the load and add encryption
  3. Create a producer-consumer pipeline at the server side in case we would like to run some manipulation on the received data 
     (machine learning classifier for example)
  4. Error handling and logging 
  5. Sensor histogram web page should work with AJAX to handle the update without refreshing the whole page   
  6. Create a configuration file that will contain environment variables, making the application suitable for both Linux and Windows 
