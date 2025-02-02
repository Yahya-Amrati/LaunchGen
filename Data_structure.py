from dataclasses import dataclass
import uuid


ILLEGAL_CHARS: str = """
"!"#$%&'()*+,/:;<=>?@[\\]^`{|}~ ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸
¹º»¼½¾¿×÷ʰʲʳʷʸⁿ℗℠™Ω℧←↑→↓↔↕✓✔✕✖✗✘☆★♠♣♥♦♪♫⛔⚠️🚀🔥
💀😊🤖中文日本語हिन्दी"""


def generate_random_username() -> str:
    uuid__name: str = str(uuid.uuid4())
    name: list = []
    for ix, i in enumerate(uuid__name.split("-")):
        # checking if for not letting the username be too long
        # cause max username in minecraft length is 16
        if ix == 15:
            break
        for x in i.split():
            if any(ILLEGAL_CHARS in x):
                i = i.replace(x, "")
            else:
                continue
        name.append(i)
    return "".join(name)


@dataclass(sorted=True)
class UserMinecraft:
    name: str = generate_random_username()
    Offline: bool = True
    Vanilla: bool
    Forge: bool
    Fabric: bool
    uuid: str

    def __init__(self):
        # correct values if possible
        new_name: list = []
        for i in self.name:
            if any(ILLEGAL_CHARS, i):
                i = ""
                new_name.append(i)
            else:
                new_name.append(i)
                continue
        self.name = "".join(new_name)
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
