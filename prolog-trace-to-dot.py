import pygraphviz as pgv

graph = pgv.AGraph(strict=False, directed=True)

def get_first_word(line):
    if line == "":
        return
    words = line.split()
    if len(words) > 0:
        first_word = words[0]
        return first_word

def add_node(graph, parent, line):
    node_name = line.strip()
    graph.add_node(node_name)
    if parent is not None:
        graph.add_edge(parent, node_name)
    return node_name


with open("trace.txt", 'r') as trace_file:
    current = None

    while True:
        line = trace_file.readline()
        if line.strip() == "":
            break
        first_word = get_first_word(line)
        if current is None or first_word == "Call:":
            current = add_node(graph, current, line)
        elif first_word in ["Exit:", "Fail:"]:
            add_node(graph, current, line)
            current = None  # or set to the parent node if you have a way to track it
        elif first_word == "Redo:":
            current = add_node(graph, current, line)

graph.layout(prog='dot')
graph.write('call_tree.dot')
