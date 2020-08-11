# Importing necessary libraries
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
# Declaring base
Base = declarative_base()
# Attributes are declared: ID,role,area of work, company, city,country,prior work experience needed
class Jobsearch(Base):
    __tablename__ = "Company"
    ID = Column(Integer,primary_key=True)
    role = Column(String)
    aow = Column(String)
    company = Column(String)
    city = Column(String)
    country = Column(String)
    work = Column(Integer)

    # Initialising values
    def __init__(self,ID,role,aow,company,city,country,work):
        self.ID = ID
        self.role = role
        self.aow = aow
        self.company = company
        self.city = city
        self.country = country
        self.work = work

    # Assigning dictionary    
    def toDict(self):
        final = {
            "ID": self.ID,
            "role": self.role,
            "area of work": self.aow,
            "company": self.company,
            "city": self.city,
            "country":self.country,
            "work experience":self.work
        }
        return final
# Defining Job
class Jobsearch(BaseModel):
    ID:int
    role:str
    aow:str
    company:str
    city:str
    country:str
    work:int

# Creating an engine for connecting sqlite
enginejs = create_engine("sqlite:///jobsearch.db")

session = sessionmaker(bind=enginejs)()

app = FastAPI()
# Endpoints of "app"
@app.get('/')
async def root():
    return {"message": "This API will provide you to perform fundamental operations on job search database"}

# Retrieve all jobs
@app.get('/jobsearch/')
async def getAll():
    final = []
    jdata = session.query(Jobsearch).all()
    for row in jdata:
        final.append(row.toDict())
    return final

# Job Addition
@app.post('/jobsearch/')
async def post(jobsearch:Jobsearch):
    data = jobsearch.dict()
    n = len(session.query(Jobsearch).all())
    result = Jobsearch(data["ID"],data["role"],data["area of work"],data["company"],data["city"],data["country"],data["work experience"],n)
    session.add(result)
    session.commit()
    return {
    	# OK status
        "Status":200,
        # Created job
        "message": "Job has been created!"
    }


# Search a job by ID
@app.get('/jobsearch/{ID}')
async def get(ID:int):
    dataval = session.query(Jobsearch).filter(Jobsearch.ID == ID)
    result = dataval[0].toDict()
    return result

# Apply for a job 
@app.post('/jobsearch/{ID}/apply/')
async def apply(ID:int):
    try:
        uapply = session.query(Jobsearch).filter(Jobsearch.ID == ID)
        # Applying for the job
        uapply[0].applied += 1
        session.commit()
        return {
            "Status":200,
            "message": "You have successfully applied for this job!"
        }
    # Invalid ID
    except:
        return {
            "Status": 404,
            "message":"Due to invalid ID, your request could not be processed"
        }
# Delete a job listing
@app.delete('/jobsearch/{ID}')
async def delete(ID:int):
    try:
        deljob = session.query(Jobssearch).filter(Jobsearch.ID == ID)
        session.delete(deljob[0])
        session.commit()
        return {
            "Status":200,
            "message": "Job lisiting is deleted"
        }
    except:
        return {
            "Status": 404,
            "message": "Invalid ID Error"
        }
