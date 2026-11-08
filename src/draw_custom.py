import json
import networkx as nx
import matplotlib.pyplot as plt
import os

topology_path = 'SeQUeNCe/example/demo_for_beginners/star_network.json'
output_path = r'C:\Users\s3cr3t\.gemini\antigravity-ide\brain\39b0888b-b358-45e0-bced-76cb17728ef0\topology.png'

with open(topology_path) as f:
    config = json.load(f)

G = nx.Graph()

for node in config.get('nodes', []):
    G.add_node(node['name'])

for conn in config.get('qconnections', []):
    G.add_edge(conn['node1'], conn['node2'], color='blue', label='quantum')
    
for conn in config.get('cconnections', []):
    # Only add if it doesn't already exist to avoid overriding color, or just let networkx handle multigraphs?
    # Networkx Graph doesn't support multiple edges between same nodes natively, it will just update the edge. 
    # Let's use MultiGraph just in case
    pass

# We will use MultiGraph to show multiple edges (classical + quantum)
G = nx.MultiGraph()
for node in config.get('nodes', []):
    G.add_node(node['name'])

for conn in config.get('qconnections', []):
    G.add_edge(conn['node1'], conn['node2'], color='blue', style='solid')

for conn in config.get('cconnections', []):
    G.add_edge(conn['node1'], conn['node2'], color='red', style='dashed')

pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(10, 8))

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=3000)
nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

# Draw edges
ax = plt.gca()
for u, v, data in G.edges(data=True):
    ax.annotate("",
                xy=pos[u], xycoords='data',
                xytext=pos[v], textcoords='data',
                arrowprops=dict(arrowstyle="-", color=data['color'],
                                shrinkA=20, shrinkB=20,
                                patchA=None, patchB=None,
                                connectionstyle="arc3,rad=0.1" if data['color'] == 'red' else "arc3,rad=-0.1",
                                linestyle=data.get('style', 'solid'),
                                linewidth=2
                                ),
                )

# Add legend
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], color='blue', lw=2, label='Quantum Connection'),
                   Line2D([0], [0], color='red', lw=2, linestyle='dashed', label='Classical Connection')]
plt.legend(handles=legend_elements, loc='upper left')

plt.title("Star Network Topology")
plt.axis('off')
plt.savefig(output_path, bbox_inches='tight')
print(f"Saved {output_path}")
