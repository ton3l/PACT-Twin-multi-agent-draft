from fastapi import FastAPI
from agents.reporter import ReporterAgent, ReporterOptions


class MainAgent:
    def __init__(self) -> None:
        self.app = FastAPI()
        self.reporterAgent = ReporterAgent()
        self.setup_routes()

    def setup_routes(self):
        self.app.add_api_route("/", self.read_root, methods=["GET"])
        self.app.add_api_route("/report", self.generate_report, methods=["POST"])

    def read_root(self):
        return {"Hello": "World"}

    def generate_report(self, options: ReporterOptions) -> str:
        return str(
            self.reporterAgent.run(
                options.prompt  # teste: { "prompt": "{\"nome\": \"Elton\", \"idade\": 19, \"curso\": \"ciência da computação\", \"equipe\": \"multi-agent\", \"cor favorita\": \"triste\"}" }
            ).content
        )
