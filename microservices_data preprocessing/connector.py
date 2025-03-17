from pymongo import MongoClient

# MongoDB connection string - replace with your actual password
connection_string = "mongodb+srv://mostafamoeini77:09197897094%40Mm@pspark-cluster.bazje.mongodb.net/?retryWrites=true&w=majority&appName=Pspark-Cluster"

def test_mongodb_connection():
    try:
        # Create client
        client = MongoClient(connection_string)
        
        # Test connection by listing databases
        dbs = client.list_database_names()
        print("Connection successful!")
        print("Available databases:", dbs)
        
        # Close connection
        client.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing MongoDB connection...")
    test_mongodb_connection()