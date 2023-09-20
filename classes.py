# Classes used to express synchronized disjuction
# of requests and command

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
    l = name.strip('.').split("_")
    for idx, w in enumerate(l):
        if w[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            i = int(w)

            j = int(l[idx+1])   if idx+1 < len(l) else 0
            j = j+int(l[idx+2]) if idx+2 < len(l) else j

            return i, j
    return 0, 0

##### Disjunctive rule

class Snippet():
    """ Coupled request excerp and command excep
    The request excerp has to be embedded by the 'request' bracketing
    and can contain NAP ('without')
    The command except does not have to contain the 'commands' bracketing"""
    def __init__(self, name:str):
        self.name    = name
        self.request = ""
        self.command = ""

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def print(self):
        string = self.name + ":\n\t"
        string += tabulate(self.request) + "\n\t"
        string += "commands { " + tabulate(self.command) + " }"
        return string 


ROOT = Snippet("__ROOT__") # Default root


class DisjRule(nx.DiGraph):
    """ Structure to express a dsjunction of requests (and
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

    def gen_branches(self, output="rule", group_by_trace=False) -> list:
        """Generates all rules corresponding to the concatenation
        of the requests and command excerps of all branches of self.
        If output = rule, returns rules as strings
        If output = request, return requests only
        'group_by_trace' : if True, requests having the same trace are
            merged. The trace of a branch is the concatenation of the names
            of its snippets"""
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
            trace = ""
            requests = ""
            commands = ""
            # Concatenating request and command snippets
            for node in branch:
                trace += node.name
                p = "\n" if len(node.request.strip()) > 0 else ""
                c = "\n" if len(node.command.strip()) > 0 else ""
                requests += node.request + p
                commands += node.command + c

            if output == "request":
                # Only resturn the request snippet concatenation
                result.append((trace,requests))

            else:
                # Rule construction: requests + commands
                rule = "rule "+self.rule_name+"_"+str(i)+" { \n" # Rule name
                rule += "\t" + tabulate(requests)
                rule += "commands {\n\t\t" + tabulate(tabulate(commands))
                result.append((trace, rule + "}\n\t}"))

        # Formatting output
        if group_by_trace == False:
            return [elt for (_,elt) in result]
        
        else:
            dict = {trace:[] for (trace,_) in result}
            for (trace, elt) in result: # Grouping by trace
                dict[trace].append(elt)
            return [dict[trace] for trace in dict.keys()]

    def draw(self):
        pos = { n : snippet_name_to_indices(n.name) for n in self.nodes() }
        nx.draw(self, pos=pos, with_labels=True, font_weight='bold')
        plt.show()


def gen_grs(seq:list, filename:str) -> ():
    """Input:   list 'seq' of DisjRule objects,
                file name 'filename' of output file
        Output: Create a .grs file with
            - a package for all DisPat
            - a Onf(Seq(...)) strategy for all package
            - a Seq(...) stratagy (named 'main') of all these strategies
        If a DisjRule is used several times, its package will be written
        down only once, but taken with multiplicity in the main strategy."""
    all_names = set()
    with open(filename,"w") as file:
        # Main loop
        main_strat = "strat main { Seq(" # Main strategy
        assert len(seq) > 0 # Assuming seq is not empty
        for dr in seq:  
            rules = dr.gen_branches("rule")

            if not dr.rule_name in all_names:
                # Strategy name are prefixed by "pkg_"
                package =  "package pkg_" + dr.rule_name + " { \n"
                package += "\t" + tabulate("\n".join(rules))
                package += "\n\t}"
                file.write(package + "\n")
                
                strategy =  "strat " + dr.rule_name 
                strategy += " { Onf(Seq(pkg_" + dr.rule_name + ")) }"
                file.write(strategy + "\n\n")

            main_strat += dr.rule_name + ","
            
        all_names.add(dr.rule_name)

        file.write(main_strat[:-1] + ") }")

