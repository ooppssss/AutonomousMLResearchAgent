from research_agent.preregistration.models import PreregistrationStatus
from research_agent.preregistration.registry import PreregistrationRegistry


class ExperimentGate:
    def __init__(self, registry: PreregistrationRegistry):
        self.registry = registry

    def check(self, preregistration_id: str) -> bool:
        prereg = self.registry.load(preregistration_id)

        if prereg.status != PreregistrationStatus.LOCKED:
            raise PermissionError("Experiment blocked: preregistration is not locked")

        if not self.registry.verify(preregistration_id):
            raise PermissionError("Experiment blocked: preregistration integrity check failed")

        return True

    def authorize(self, preregistraion_id: str):
        self.check(preregistraion_id)
        print("Experiment authorized.")