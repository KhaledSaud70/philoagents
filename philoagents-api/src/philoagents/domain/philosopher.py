from pydantic import BaseModel, Field


class Philosopher(BaseModel):
    """A class representing a philosopher agent with memory capabilities.

    Args:
        id (str): Unique identifier for the philosopher.
        name (str): Name of the philosopher.
        perspective (str): Description of the philosopher's theoretical views
            about AI.
        style (str): Description of the philosopher's talking style.
    """

    id: str = Field(description="Unique identifier for the philosopher")
    name: str = Field(description="Name of the philosopher")
    perspective: str = Field(
        description="Description of the philosopher's theoretical views about AI"
    )
    style: str = Field(description="Description of the philosopher's talking style")

    def __str__(self) -> str:
        return f"Philosopher(id={self.id}, name={self.name}, perspective={self.perspective}, style={self.style})"
