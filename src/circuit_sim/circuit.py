from src.circuit_sim.components import *
from src.circuit_sim.netlist_loader import Netlist
from src.circuit_sim.solver import solve_circuit
import numpy
import networkx as nx

class Circuit:
    def __init__(self,  string : str | None = None, filename = None , terminal : int | None = None):
        _temp = None
        if string:
            _temp = Netlist(string)
        elif filename:
            _temp = Netlist(filename=filename)
        elif terminal is not None:
            _temp = Netlist(terminal=terminal)
        else:
            raise SyntaxError("Invalid input. Please write valid input")
        self.nodes = _temp.nodes
        self.components = _temp.elements

    def add_element(self, string):
        """Add element from string"""
        _temp = Netlist(string = string, nodes = self.nodes, elements = self.components)
        self.components = _temp.elements
        self.nodes = _temp.nodes

    def is_valid(self):
        """Check the circuit to be valid and has uniqe solution"""
        _graph = nx.MultiDiGraph()
        for item in self.components:
            if item.id[0] in ['R', 'V', 'L', 'C']:
                _graph.add_edge(item.nodes[0].number, item.nodes[1].number, type = type(item), data = item.id)
                _graph.add_edge(item.nodes[1].number, item.nodes[0].number, type = type(item), data = item.id)
            elif item.id[0] == 'I':
                _graph.add_edge(item.nodes[0].number, item.nodes[1].number, type = type(item), data = item.id)
        for u, v, data in _graph.edges(data=True):
            if data.get("type") == CurrentSource:
                _temp = _graph.copy()
                _temp.remove_edges_from([(u, v)])
                _paths = nx.all_simple_paths(_temp, source=u, target=v)
                if next(_paths, None) is None:
                    raise ValueError("There is a current source which is series with other current sources or theer is a cutset")
                
        A, _ = self.build_system()
        if numpy.linalg.matrix_rank(A) != len(A):
            raise ValueError("The G_matrix is singular. So the circuit has no uniqe solution. It might be because of voltage sources in parallell")
        
        return True

    def kill(self, exceptions : list | None = None):
        pass

    def assign_indices(self):
        """assign indices to nodes and components for matrix construction."""

        index = 0
        flag = False
        for node in self.nodes:
            if node.number == 0:
                flag = True

        if not flag:
            self.nodes[0].number = 0

        for node in self.nodes:
            if node.number != 0: #Node not ground
                node.index = index
                index += 1
        for component in self.components:
            if isinstance(component, (VoltageSource, Inductor)):
                component.branch_index = index
                index += 1

        return index
            

    def build_matrices(self):
        """Build the G_matrix and I_vector based on the circuit components."""

        num_unknowns = self.assign_indices()

        # Initialize G_matrix and I_vector
        G_matrix = [[0.0 for _ in range(num_unknowns)] for _ in range(num_unknowns)]
        I_vector = [[0.0] for _ in range(num_unknowns)]

        return G_matrix, I_vector

    def build_system(self):
        """build the system of equations for the circuit based on the components and nodes."""

        G_matrix, I_vector = self.build_matrices()

        for component in self.components:
            component.stamp(G_matrix, I_vector)

        return G_matrix, I_vector
    
    def thevenin_norton(self, node1, node2):
        """Doing thevenin norton analyzing from node1 and node2"""
        self.V_thevenin = None
        self.I_norton = None
        self.R_thevenin = None
        counter = 0
        index = [0, 0]
        for node in self.nodes:
            if node1 == node:
                index[0] = node
            if node2 == node:
                index[1] = node

        try:
            G_matrix, I_vector = self.build_system()
            Y_matrix = solve_circuit(G_matrix, I_vector)
            if 0 not in [index[0].number, index[1].number]:
                self.V_thevenin = Y_matrix[index[0].index][0] - Y_matrix[index[1].index][0]
            else:
                self.V_thevenin = Y_matrix[index[0].index][0] if index[0].number != 0 else Y_matrix[index[1].index][0]
            counter += 1
        except:
            print("The voltage of open circuit is infinit, try to calculate information in other ways")

        _temp_components = None
        _temp_nodes = None
        flag = False
        try:
            _temp_components = list(self.components)
            _temp_nodes = list(self.nodes)
            V_test = VoltageSource("V_test", index[0], index[1], 0)
            self.components.append(V_test)
            flag = True
            G_matrix, I_vector = self.build_system()
            Y_matrix = solve_circuit(G_matrix, I_vector)
            self.I_norton = Y_matrix[V_test.branch_index][0]
            self.components = _temp_components
            self.nodes = _temp_nodes
            counter += 1
        except:
            print("The current of short circuit is infinit, try to calculate information in other ways")
            if flag == True:
                self.components = _temp_components
                self.nodes = _temp_nodes

        if counter == 2:
            return None
        flag = False

        # TODO: In development, first must simplify netlist and kill funcs be created
        # try:
        #     _temp_components = list(self.components)
        #     _temp_nodes = list(self.nodes)            
        #     I_test = CurrentSource("I_test", node1, node2, 1)
        #     self.components.append(I_test)
        #     flag = True
        #     G_matrix, I_vector = self.build_matrices

        #     Y_matrix = solve_circuit(G_matrix, I_vector)

        #     if 0 not in [index[0].number, index[1].number]:
        #         self.R_thevenin = Y_matrix[index[0].index][0] - Y_matrix[index[1].index][0]
        #     else:
        #         self.R_thevenin = Y_matrix[index[0].index][0] if index[0].number != 0 else Y_matrix[index[1].index][0]        
        # except:
        #     print("An error accured while finding R thevenin")
        #     if flag == True:
        #         self.components = _temp_components
        #         self.nodes = _temp_nodes

    def __getitem__(self, key):
        if isinstance(key, int):
            for node in self.nodes:
                if key == node:
                    return node.__repr__()
            return "The specified node not found"
            

        elif isinstance(key, str):
            for item in self.components:
                if item.id == key:
                    return item.__repr__()
            return "The specified element not found"
