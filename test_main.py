from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

# Testing root
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "This API will provide you to perform fundamental operations on job search database"}

# Get all jobs
def test_getAll():
    response = client.get("/jobsearch")
    assert response.status_code == 200
    assert response.json() == {"message": "All jobs listed"}
    
# Add a job
def test_post():
    response = client.get("/jobsearch")
    assert response.status_code == 200
    assert response.json() == {"message": "Job has been created!"}
    
# Apply for a valid job
def test_applyvalid():
    response = client.get("/jobsearch/1/apply/")
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully applied to the job"}
    
# Apply for an invalid job
def test_applyvalid():
    response = client.get("/jobsearch/9/apply/")
    assert response.status_code == 404
    assert response.json() == {"message": "Invalid job"}

# Delete a valid job
def test_deletevaljob():
    response = client.get("/jobsearch/2")
    assert response.status_code == 200
    assert response.json() == {"message": "Deleted the job listing"}
    
# Delete an invalid job
def test_deleteinvaljob():
    response = client.get("/jobsearch/8")
    assert response.status_code == 404
    assert response.json() == {"message": "Invalid job listing"}

# Job search by ID
def test_getID():
    response = client.get("/jobsearch/1")
    assert response.status_code == 200
    assert response.json() == {
    			"ID":"1",
    			"role":"Developer",
    			"aow":"Software",
    			"company":"ABC limited",
    			"city":"Chennai",
    			"country":"India",
    			"work":"5",
    			}
    			
# Job search by work
def test_getID():
    response = client.get("/jobsearch/5")
    assert response.status_code == 404
    assert response.json() == {"message":"Try searching using ID"}
 

    
    
    
    
    
    




