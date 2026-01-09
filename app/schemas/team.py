from pydantic import BaseModel

class Team(BaseModel):
    team_id : str
    primary_indudtry : str
    secondary_industry : str

class NewTeam(Team):
    password : str
