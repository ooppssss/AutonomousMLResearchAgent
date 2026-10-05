import json
from multiprocessing.sharedctypes import Value
from pathlib import Path
from textwrap import indent

from research_agent.preregistration.integrity import lock_preregistration, verify_integrity
from research_agent.preregistration.validator import validate_preregistration

from .models import PreRegistration, PreregistrationStatus

class PreregistrationRegistry:
    def __init__(self, directory="preregistrations"):
        self.directory = Path(directory)
        self.directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(self, prereg: PreRegistration):
        if prereg.status == PreregistrationStatus.LOCKED:
            raise ValueError("Locked preregistration cannot be modified.")

        path = self.directory / (f"{prereg.preregistration_id}.json")

        path.write_text(prereg.model_dump_json(indent=2))

        return path

    def validate(self, prereg: PreRegistration):
        errors = validate_preregistration(prereg)

        if errors:
            return False, errors

        prereg.status = PreregistrationStatus.VALIDATED
        return True, []

    def lock(self, prereg: PreRegistration):
        if prereg.status != PreregistrationStatus.VALIDATED:
            raise ValueError("Only VALIDATED preregistrations can be locked.")

        lock_preregistration(prereg)

        self.save_locked(prereg)

    def save_locked(self, prereg: PreRegistration):
        path = self.directory / (f"{prereg.preregistration_id}.json")

        path.write_text(prereg.model_dump_json(indent=2))
        return path

    def load(self, preregistration_id: str):

        path = self.directory / (
            f"{preregistration_id}.json"
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Preregistration {preregistration_id} not found."
            )

        data = json.loads(path.read_text())

        return PreRegistration.model_validate(data)

    def verify(self, preregistration_id: str):

        prereg = self.load(preregistration_id)

        return verify_integrity(prereg)