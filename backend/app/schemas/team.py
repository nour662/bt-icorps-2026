from pydantic import BaseModel

class Team(BaseModel):
    team_id : str
    team_name: str
    industry: str

class NewTeam(Team):
    password : str
class TeamLogin(BaseModel):
    team_id : str
    password : str
