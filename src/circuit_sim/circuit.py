from src.circuit_sim.components import VoltageSource, Inductor
from src.circuit_sim.netlist_loader import NetlistLoader

class Circuit:
    def __init__(self,  string : str | None = None, filename = None , terminal : int | None = None):
        _temp
        if string:
            _temp = NetlistLoader(string)
        elif filename:
            _temp = NetlistLoader(filename=filename)
        elif terminal is not None:
            _temp = NetlistLoader(terminal=terminal)
    
        self.nodes = _temp.nodes
        self.components = _temp.elements

    def assign_indices(self):
        """assign indices to nodes and components for matrix construction."""

        index = 0
        for node in self.nodes:
            if node.number != 0: #Node not ground
                node.index = index
                index += 1

        for component in self.components:
            if isinstance(component, (VoltageSource, Inductor)):
                component.branch_index = index
                index += 1

        self.num_unknowns = index

    def build_matrices(self):
        """Build the G_matrix and I_vector based on the circuit components."""

        # Initialize G_matrix and I_vector
        G_matrix = [[0.0 for _ in range(self.num_unknowns)] for _ in range(self.num_unknowns)]
        I_vector = [0.0 for _ in range(self.num_unknowns)]

        return G_matrix, I_vector

    def build_system(self):
        """build the system of equations for the circuit based on the components and nodes."""

        self.assign_indices()
        G_matrix, I_vector = self.build_matrices()

        for component in self.components:
            component.stamp(G_matrix, I_vector)

        return G_matrix, I_vector
