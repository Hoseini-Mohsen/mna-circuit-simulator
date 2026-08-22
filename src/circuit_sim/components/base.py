from abc import ABC, abstractmethod

from circuit_sim.node import Node


class Component(ABC):
    """Base class for all circuit components."""

    def __init__(self, component_id: str, *nodes):
        if not all(isinstance(node, Node) for node in nodes):
            raise TypeError("All nodes must be instances of the Node class.")

        self.id = component_id
        self.nodes = nodes

    @abstractmethod
    def stamp(self, G_matrix, I_vector):
        pass
