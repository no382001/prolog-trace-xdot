import pygraphviz as pgv

def get_layer_number(line):
    start = line.find('(') + 1
    end = line.find(')')
    return int(line[start:end]) if start > 0 and end > start else None

def add_node(graph, line, node_id, parent_id=None):
    node_name = f"{node_id}: {line.strip()}"
    graph.add_node(node_name)
    if parent_id is not None:
        graph.add_edge(parent_id, node_name)
    return node_name

graph = pgv.AGraph(strict=False, directed=True)
graph.graph_attr['ranksep'] = '15.0'
graph.node_attr['shape'] = 'box'

call_stack = {}
node_id = 0

with open("trace.txt", 'r') as trace_file:
    for line in trace_file:
        line = line.strip()
        if line:
            layer = get_layer_number(line)
            first_word = line.split()[0] if line else None

            parent_id = call_stack.get(layer - 1) if layer is not None else None
            current_id = add_node(graph, line, node_id, parent_id)
            
            if first_word == "Call:":
                call_stack[layer] = current_id
            elif first_word in ["Exit:", "Fail:"]:
                if call_stack.get(layer):
                    call_stack.pop(layer)    
            node_id += 1

graph.layout(prog='dot')
graph.write('call_tree.dot')
