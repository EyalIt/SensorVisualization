# SensorVisualization

This is a client-server application with the following abilities:
  1. Client:
     The client activates 4 sensors, each of them sample a different characteristic of the PC every 100ms.
     There are 4 types of sensors - context switch sensor, interrupts sensor, process IDs sensor and network connections sensor.
     Once the sensor gets a new sample it sends the data to the server
     
  2. Server:
     a. BE side:
        The server receives new requests with sensor data from multiple clients. 
        It differentiate the clients according to ip address.
        Each sample is saved to a database, which stores the samples on a daily collection. 
        Every 24 hours it activates an auto-backup process, zips the daily collection and stores it in an S3 storage.
        The data can be queried using and html web page.
     b. FE side:
        In order to query the database, there is a web page stored at http://localhost:8000/query_sensors/.
        The web page contains a few drop-down lists for selecting client ID and sensor type.
        Once "generate graph" button is selected, a histogram of the sensor values from the specific client is extracted 
        from the database and displayed.
        
     
