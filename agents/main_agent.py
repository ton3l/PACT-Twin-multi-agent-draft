from fastapi import FastAPI
from agents.reporter import ReporterAgent

class MainAgent:
    def __init__(self) -> None:
        self.app = FastAPI()
        self.reporterAgent = ReporterAgent()
        self.setup_routes()

    def setup_routes(self):
        self.app.add_api_route("/", self.read_root, methods=["GET"])
        self.app.add_api_route("/report", self.generate_report, methods=["GET"])

    def read_root(self):
        return {"Hello": "World"}
    
    def generate_report(self):
        return self.reporterAgent.run('{"nome": "Elton","idade: 19,"curso": "ciência da coputação","equipe": "multi-agent","cor favorita": "batata"}').content