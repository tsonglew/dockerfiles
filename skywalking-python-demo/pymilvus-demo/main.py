from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections, utility

# Connect to Milvus
connections.connect("default", host="127.0.0.1", port="19530")
# Check if a collection exists
collection_name = "demo_collection"
if utility.has_collection(collection_name):
    print(f"Collection {collection_name} already exists, dropping it for fresh start.")
    utility.drop_collection(collection_name)

# Define a collection schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=128),
]
schema = CollectionSchema(fields, description="Demo collection with vectors")

# Create a new collection
collection = Collection(name=collection_name, schema=schema)
collection.create_index(
    field_name="vector", index_params={"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 128}}
)

# Generate some sample data
import numpy as np

num_entities = 1000
data = [
    {
        # "id": i,
        "vector": np.random.rand(128).tolist(),
    }
    for i in range(num_entities)
]

# Insert data into the collection
collection.insert(data)

# Make sure insert is done
collection.flush()

# Load the collection into memory
collection.load()

# Conduct a vector similarity search
query_vectors = [np.random.rand(128).tolist() for _ in range(5)]  # searching 5 random vectors
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

results = collection.search(query_vectors, anns_field="vector", param=search_params, limit=5, expr=None)

# Display the search results
for i, result in enumerate(results):
    print(f"Search result for query vector {i}:")
    for hit in result:
        print(f"ID: {hit.id}, distance: {hit.distance}")

# Drop the collection if no longer needed
utility.drop_collection(collection_name)
