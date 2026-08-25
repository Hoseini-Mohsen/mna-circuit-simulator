from base import Component


class Resistor(Component):
    """Resistor is a passive component that resists the flow of electric current."""

    def __init__(self, component_id: str, node1, node2, resistance: int | float):
        if not isinstance(resistance, (int, float)):
            raise TypeError("Resistance must be a numeric value.")

        super().__init__(component_id, node1, node2)

        self.resistance = resistance
        self.conductance = 1 / resistance  # G = 1/R

    def stamp(self, G_matrix, I_vector):
        """Stamp the resistor into the G_matrix and I_vector."""

        a, b = self.nodes[0].index, self.nodes[1].index
        g = self.conductance

        if a is not None:
            G_matrix[a][a] += g
        if b is not None:
            G_matrix[b][b] += g
        if a is not None and b is not None:
            G_matrix[a][b] -= g
            G_matrix[b][a] -= g

    def __repr__(self):
        return (
            f"Resistor(id={self.id}, "
            f"resistance={self.resistance}Ohms, "
            f"nodes=({self.nodes[0].index}, {self.nodes[1].index}))"
        )

class Capacitor(Component):
    """Capacitor is a passive component that stores electrical energy in an electric field."""

    def __init__(self, component_id: str, node1, node2, capacitance: int | float, initial_condition : int | float | None = None):
        if not isinstance(capacitance, (int, float)):
            raise TypeError("Capacitance must be a numeric value.")

        super().__init__(component_id, node1, node2)

        self.capacitance = capacitance
        self.initial_condition = initial_condition

    def stamp(self, G_matrix, I_vector):
        """Stamp the capacitor into the G_matrix and I_vector."""
        # For DC analysis, capacitors are open circuits (no current flows)
        pass

    def __repr__(self):
        return (
            f"Capacitor(id={self.id}, "
            f"capacitance={self.capacitance}F, "
            f"nodes=({self.nodes[0].index}, {self.nodes[1].index}))"
        )

class Inductor(Component):
    """Inductor is a passive component that stores energy in a magnetic field
    when electric current flows through it."""

    def __init__(self, component_id: str, node1, node2, inductance: int | float, initial_condition : int | float | None = None):
        if not isinstance(inductance, (int, float)):
            raise TypeError("Inductance must be a numeric value.")

        super().__init__(component_id, node1, node2)

        self.inductance = inductance
        self.branch_index = None  # Will be assigned during index assignment
        self.initial_condition = initial_condition

    def stamp(self, G_matrix, I_vector):
        """Stamp the inductor into the G_matrix and I_vector."""
        # For DC analysis, inductors are short circuits (zero resistance)
        a, b = self.nodes[0].index, self.nodes[1].index
        k = self.branch_index

        if a is not None:
            G_matrix[k][a] += 1
            G_matrix[a][k] += 1
        if b is not None:
            G_matrix[k][b] -= 1
            G_matrix[b][k] -= 1

    def __repr__(self):
        return (
            f"Inductor(id={self.id}, "
            f"inductance={self.inductance}H, "
            f"nodes=({self.nodes[0].index}, {self.nodes[1].index}))"
        )
