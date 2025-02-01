from dataclasses import dataclass
import uuid


@dataclass
class UserMinecraft:
    name: str
    Offline: bool
    Forge: bool
    Fabric: bool
    def __init__(self):
        self.uuid = uuid.uuid3(uuid.RESERVED_MICROSOFT, self.name)

    def __repr__(self):
        return f"UserMinecraft(name={self.name}, Offline={self.Offline}, Forge={self.Forge}, Fabric={self.Fabric})"
    

        
