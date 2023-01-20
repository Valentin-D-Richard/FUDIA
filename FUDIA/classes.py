# Classes used to express synchronized disjuction
# of patterns and command

# Current error number : 2

import networkx as nx
import matplotlib.pyplot as plt

##### Auxiliary functions

def tabulate(string):
    """Adds a tabulation after every newline caracter"""
    return "\n\t".join(string.split("\n"))


def snippet_name_to_indices(name:str):
    """"Extracts the integers i and j (resp. j+k) from a snippet name
    u_i_j (resp.r u_i_j_k) where word u contains no ciffer
    following an underscore.
    If the format is not respected, returns 0."""
    l = name.split("_")
    for idx, w in enumerate(l):
        if w[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            i = int(w)

            j = int(l[idx+1])   if idx+1 < len(l) else 0
            j = j+int(l[idx+2]) if idx+2 < len(l) else j

            return i, j
    return 0, 0

##### Disjunctive pattern

class Snippet():
    """ Coupled pattern excerp and command excep
    The pattern excerp has to be embedded by the 'pattern' bracketing
    and can contain NAP ('without')
    The command excetp does not have to contain the 'commands' bracketing"""
    def __init__(self, name:str):
        self.name    = name
        self.pattern = ""
        self.command = ""

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def print(self):
        string = self.name + ":\n\t"
        string += tabulate(self.pattern) + "\n\t"
        string += "commands { " + tabulate(self.command) + " }"
        return string 


ROOT = Snippet("__ROOT__") # Default root


class DisjPat(nx.DiGraph):
    """ Structure to express a dsjunction of patterns (and
    coupled commands) in a dependent way
    At any moment, self is a DAG"""
    def __init__(self, name:str, root=ROOT):
        self.rule_name = name
        self.root = root

        nx.DiGraph.__init__(self)
        self.add_node(root)

    def projection(self, node:Snippet) -> list:
        """Returns the list of leaves who are large descedants
        from node"""
        desc = list(nx.descendants(self, node)) + [node]
        return[ n for n in desc if self.out_degree(n) == 0]

    def add_snippets(self, snippets:list, dep:Snippet) -> None:
        """ Adds snippets in the DAG and connects them
        to all leaves descendant from dep"""
        # Adding nodes
        for snippet in snippets:
            assert type(snippet) == Snippet
            self.add_node(snippet)

        # Adding edges
        proj = self.projection(dep)
        for snippet in snippets:
            for node in proj:
                self.add_edge(node, snippet)

    def gen_branches(self, output="rule"):
        """Generates all rules corresponding to the concatenation
        of the patterns and command excerps of all branches of self.
        If output = rule, returns rules as strings
        If output = pattern, return patterns only"""
        result = []
        
        # Error if self is empty
        if len(self.nodes) ==0:
            msg = "DAG "+self.rule_name+" is empty"
            raise ValueError("[001] " + msg)
        
        # Computing branches
        leaves = self.projection(self.root)
        branches = nx.all_simple_paths(self, self.root, leaves)

        # Special case of only one node not properly treated by all_simple_paths
        if len(self.nodes) == 1:
            branches = [[self.root]]

        for i, branch in enumerate(branches):
            patterns = ""
            commands = ""
            # Concatenating pattern and command snippets
            for node in branch:
                p = "\n" if len(node.pattern.strip()) > 0 else ""
                c = "\n" if len(node.command.strip()) > 0 else ""
                patterns += node.pattern + p
                commands += node.command + c

            if output == "pattern":
                # Only resturn the pattern snippet concatenation
                result.append(patterns)

            else:
                # Rule construction: patterns + commands
                rule = "rule "+self.rule_name+"_"+str(i)+" { \n" # Rule name
                rule += "\t" + tabulate(patterns)
                rule += "commands {\n\t\t" + tabulate(tabulate(commands))
                result.append(rule + "}\n\t}")

        return result

    def draw(self):
        pos = { n : snippet_name_to_indices(n.name) for n in self.nodes() }
        nx.draw(self, pos=pos, with_labels=True, font_weight='bold')
        plt.show()


def gen_grs(seq:list, name:str, output="rule"):
    """Input:   list 'seq' of DisPat objects,
                name 'name' of input file (without the '.grs' extension)
        Output: Create a .grs file with
            - a package for all DisPat
            - a Onf(Seq(...)) strategy for all package
            - a Seq(...) stratagy (named 'main') of all these strategies
        If a DisPat is used several times, its packege will be written
        down only once, but taken with multiplicity in the main strategy."""
    all_names = set()
    with open(name + ".grs","w") as file:
        # Main loop
        main_strat = "strat main { Seq(" # Main strategy
        for dp in seq:  # Assuming seq is not empty
            rules = dp.gen_branches(output)

            if output == "rule":
                if not dp.rule_name in all_names:
                    # Strategy name are prefixed by "pkg_"
                    package =  "package pkg_" + dp.rule_name + " { \n"
                    package += "\t" + tabulate("\n".join(rules))
                    package += "\n\t}"
                    file.write(package + "\n")
                    
                    strategy =  "strat " + dp.rule_name 
                    strategy += " { Onf(Seq(pkg_" + dp.rule_name + ")) }"
                    file.write(strategy + "\n\n")

                main_strat += dp.rule_name + ","
                
            all_names.add(dp.rule_name)

        if output == "rule":
            file.write(main_strat[:-1] + ") }")


        