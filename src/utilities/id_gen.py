import uuid


def generate_ticket_id(event_name: str):
    """Generate a unique ticket ID for a successful purchase."""
    return f"{event_name[:3].upper()}-{uuid.uuid4().hex[:8]}"

