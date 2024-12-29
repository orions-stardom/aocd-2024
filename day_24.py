#!/usr/bin/env python
import networkx as nx
from parse import parse
import more_itertools as mit

def build_graph(rawdata):
    G = nx.DiGraph()
    inputs, rules = rawdata.split("\n\n")

    for line in inputs.splitlines():
        wire, value = line.split(": ")
        G.add_node(wire, value=int(value))

    for rule in rules.splitlines():
        l, op, r, out = parse("{} {} {} -> {}", rule)
        G.add_node(out, op=op)
        G.add_edge(l, out)
        G.add_edge(r, out)

    return G

class LogicCircuit:
    def __init__(self, rawdata):
        self.G = build_graph(rawdata)
        self.swapped = set()

    def rename(self, old, new):
        # print(f"RENAME {old}->{new}")
        self.G.nodes[old]["old_name"] = old
        nx.relabel_nodes(self.G, {old: new}, copy=False)

    def swap(self, n1, n2):
        # print(f"SWAP {n1}<=>{n2}")
        if n1.startswith("z") or n2.startswith("z"):
            # FIXME I dont quite understand why this difference is needed
            # except that trial and error proved it works
            G = nx.relabel_nodes(self.G, {n1: n2, n2: n1})
            G.remove_edges_from(list(G.edges((n1, n2))))
            G.add_edges_from((n1, e[1]) for e in self.G.edges(n1))
            G.add_edges_from((n2, e[1]) for e in self.G.edges(n2))
            self.G = G
            self.swapped.add(self.G.nodes[n1].get("old_name", n1))
            self.swapped.add(self.G.nodes[n2].get("old_name", n2))
        else:
            new_n1 = list(self.outputs(n2)) 
            new_n2 = list(self.outputs(n1)) 
            self.G.remove_edges_from(list(self.G.edges((n1,n2))))
            self.G.add_edges_from((n1,n) for n in new_n1)
            self.G.add_edges_from((n2,n) for n in new_n2)
            self.swapped.add(self.G.nodes[n1].get("old_name", n1))
            self.swapped.add(self.G.nodes[n2].get("old_name", n2))

    def inputs(self, gate):
        return sorted(e[0] for e in self.G.in_edges(gate))

    def outputs(self, gate):
        return sorted(e[1] for e in self.G.edges(gate))

    @property
    def uncorrected(self):
        return (node for node in nx.topological_sort(self.G) if not node.startswith(("x", "y", "z", "AND", "XOR", "CARRY", "INTERCARRY")))


ops = {
    "AND": lambda x,y: x and y ,
    "OR":  lambda x,y: x or y ,
    "XOR":  lambda x,y: bool(x) ^ bool(y)
}
def part_1(rawdata):
    G = build_graph(rawdata)

    for node in nx.topological_sort(G):
        if "value" not in G.nodes[node]:
            inputs = [G.nodes[e[0]]["value"] for e in G.in_edges(node)]
            G.nodes[node]["value"] = ops[G.nodes[node]["op"]](*inputs)

    outputs = sorted(n for n in G if n.startswith("z"))
    res = 0
    for output in reversed(outputs):
        res = 2*res + G.nodes[output]["value"]

    return res

def part_2(rawdata):
    # Adapted from https://www.reddit.com/r/adventofcode/comments/1hnb969/2024_day_24_part_2_aliasing_wires_to_spot_the/
    circuit = LogicCircuit(rawdata)
    while True:
        try:
            node = mit.first(circuit.uncorrected)
        except ValueError:
            break
        l, r = circuit.inputs(node)
        op = circuit.G.nodes[node]["op"]

        if l.startswith("x") and r.startswith("y"):
            n = l.removeprefix("x")
            assert n == r.removeprefix("y")

            if n == "00" and op == "AND":
                circuit.rename(node, "CARRY00")
            else:
                circuit.rename(node, f"{op}{n}")

        elif l.startswith("AND") and r.startswith("INTERCARRY"):
            n = l.removeprefix("AND")
            assert r.removeprefix("INTERCARRY") == n
            assert op == "OR"
            circuit.rename(node, f"CARRY{n}")

        elif l.startswith("CARRY") and r.startswith("XOR"):
            # This should be CARRY(n-1) XOR XOR(N) => Z(N) 
            #             or CARRY(n-1) AND XOR(N) -> INTERCARRY(N)
            n = r.removeprefix("XOR")
            assert int(l.removeprefix("CARRY")) == int(n) - 1

            if op == "XOR" and not node.startswith("z"):
                circuit.swap(node, f"z{n}")
            if op == "AND":
                circuit.rename(node, f"INTERCARRY{n}")

        elif l.startswith("AND") and r.startswith("CARRY") and op == "AND":
            n = int(r.removeprefix("CARRY"))
            circuit.swap(l, f"XOR{n+1}")
        else:
            breakpoint()

    return ",".join(sorted(circuit.swapped))

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",[
("""\
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02""", 4),

("""\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj""", 2024)])
def test_part_1(data, result):
    assert part_1(data) == result

# @pytest.mark.parametrize("data, result",
#      [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
# def test_part_2(data, result):
#     assert part_2(data) == result

if __name__ == "__main__":
    if (test_result := pytest.main([__file__])):
        sys.exit(test_result)

    part_1_done = bool(puzzle.answered_a)
    submit(part_1(puzzle.input_data), part="a", reopen=False)

    if part_1_done:
        # Don't try part 2 yet if we only finished part 1 just now
        submit(part_2(puzzle.input_data), part="b", reopen=False)
