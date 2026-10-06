from email import message

from research_agent.preregistration.experiment_gate import ExperimentGate


class ExperimentRunner:
    def __init__(self, gate: ExperimentGate):
        self.gate = gate

    def run(self, preregistration_id: str):
        self.gate.authorize(preregistration_id)

        result = self._execute_experiment()

        return result

    def _execute_experiment(self):
        print("Running Experiment")

        return {
            "status": "completed",
            "message": "Experiment executed successfully."
        }
            