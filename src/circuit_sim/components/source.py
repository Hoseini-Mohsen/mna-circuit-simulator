from .base import Component


class VoltageSource(Component):
    """VoltageSource is an active component that provides a constant voltage difference between its terminals."""

    def __init__(self, component_id: str, node1, node2, voltage: int | float):
        if not isinstance(voltage, (int, float)):
            raise TypeError("Voltage must be a numeric value.")

        super().__init__(component_id, node1, node2)

        self.voltage = voltage
        self.branch_index = None

    def stamp(self, G_matrix, I_vector):
        """Stamp the voltage source into the G_matrix and I_vector."""

        a, b = self.nodes[0].index, self.nodes[1].index
        k = self.branch_index
        v = self.voltage

        if a is not None:
            G_matrix[k][a] += 1
            G_matrix[a][k] += 1
        if b is not None:
            G_matrix[k][b] -= 1
            G_matrix[b][k] -= 1
        I_vector[k][0] += v

    def __repr__(self):
        return (
            f"VoltageSource(id={self.id}, "
            f"voltage={self.voltage}V, "
            f"nodes=({self.nodes[0].index}, {self.nodes[1].index}))"
        )

class CurrentSource(Component):
    """CurrentSource is an active component that provides a constant current between its terminals."""

    def __init__(self, component_id: str, node1, node2, current: int | float):
        if not isinstance(current, (int, float)):
            raise TypeError("Current must be a numeric value.")

        super().__init__(component_id, node1, node2)

        self.current = current

    def stamp(self, G_matrix, I_vector):
        """Stamp the current source into the I_vector."""

        a, b = self.nodes[0].index, self.nodes[1].index
        i = self.current

        if  a is not None:
            I_vector[a][0] -= i
        if b is not None:
            I_vector[b][0] += i

    def __repr__(self):
        return (
            f"CurrentSource(id={self.id}, "
            f"current={self.current}A, "
            f"nodes=({self.nodes[0].index}, {self.nodes[1].index}))"
        )

# TODO: Add affiliate resources
