from dataclasses import dataclass
import uuid


def generate_random_username() -> str:
    uuid__name = str(uuid.uuid4())
    name = []
    for ix, i in enumerate(uuid__name.split("-")):
        # checking if for not letting the username be too long
        # cause max username in minecraft length is 16
        if ix == 15:
            break
        name.append(i)
    return "".join(name)


@dataclass(sorted=True)
class UserMinecraft:
    name: str = generate_random_username()
    Offline: bool
    Vanilla: bool
    Forge: bool
    Fabric: bool
    uuid: str

    def __init__(self):
        # correct values if possible
        if self.Vanilla:
            self.Forge = False
            self.Fabric = False
        elif self.Forge:
            self.Vanilla = False
            self.Fabric = False
        elif self.Fabric:
            self.Vanilla = False
            self.Forge = False
        self.uuid = str(uuid.uuid3(uuid.RESERVED_MICROSOFT, self.name))
