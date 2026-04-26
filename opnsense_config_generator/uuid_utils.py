import uuid

# Fixed namespace for deterministic uuid5 generation.
# Generated once: uuid.uuid4() → never change after first commit.
# DNS namespace UUID — do not change after first commit.
NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")


def make_uuid(section: str, name: str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"{section}:{name}"))
