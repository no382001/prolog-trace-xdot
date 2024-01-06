import pygraphviz as pgv

graph = pgv.AGraph(strict=False, directed=True)
graph.graph_attr['ranksep'] = '10.0'  # increases the space between ranks
graph.node_attr['shape'] = 'ellipse'
def get_first_word(line):
    if line == "":
        return
    words = line.split()
    if len(words) > 0:
        return words[0]

def add_node(graph, parent, line):
    node_name = line.strip()
    graph.add_node(node_name)
    if parent is not None:
        graph.add_edge(parent, node_name)
    return node_name

with open("trace.txt", 'r') as trace_file:
    call_stack = []

    while True:
        line = trace_file.readline()
        if line.strip() == "":
            break
        first_word = get_first_word(line)
        if first_word == "Call:":
            current = add_node(graph, call_stack[-1] if call_stack else None, line)
            call_stack.append(current)
        elif first_word in ["Exit:", "Fail:"]:
            if call_stack:
                add_node(graph, call_stack[-1], line)
                call_stack.pop()
        elif first_word == "Redo:":
            current = add_node(graph, call_stack[-1] if call_stack else None, line)

# try for best result
# sccmap, dot, acyclic, ccomps, osage, gc, neato, gvpr, nop, patchwork, twopi, sfdp, tred, gvcolor, circo, fdp, unflatten 
graph.layout(prog='dot')
graph.write('call_tree.dot')
