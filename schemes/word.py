from dataclasses import dataclass

@dataclass(slots=True)
class Word:
    text: str
    width: float
    height: float
    x: int
    y: int

    def contains(self, x: float, y: float, padding=4) -> bool:
        return (
            self.x - padding <= x <= self.x + self.width + padding
            and
            self.y - padding <= y <= self.y + self.height + padding
        )