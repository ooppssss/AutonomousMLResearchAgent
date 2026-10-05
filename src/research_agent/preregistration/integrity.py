import hashlib
import json

from .models import PreRegistration, PreregistrationStatus


def calculate_hash(prereg: PreRegistration) -> str:
    data = prereg.model_dump(
        mode="json",
        exclude={"content_hash"}
    )

    canonical = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()


def lock_preregistration(prereg: PreRegistration):
    prereg.status = PreregistrationStatus.LOCKED
    prereg.content_hash = calculate_hash(prereg)
    return prereg


def verify_integrity(prereg: PreRegistration) -> bool:
    if not prereg.content_hash:
        return False

    stored_hash = prereg.content_hash
    calculated_hash = calculate_hash(prereg)

    return stored_hash == calculated_hash