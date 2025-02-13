import React, { useEffect, useState } from "react";
import ForceGraph3D from "react-force-graph-3d";
import small1 from "./small1.json"; // Ensure the path is correct

// Function to generate color based on depth
const getNodeColor = (depth) => {
  const r = Math.min(255, Math.floor(255 * (1 - depth * 0.1))); // Red decreases as depth increases
  const g = Math.min(255, Math.floor(165 + depth * 20)); // Green increases as depth increases
  const b = 0; // Blue remains 0
  return `rgb(${r},${g},${b})`;
};

const convertToGraphData = (json) => {
  const nodes = [];
  const links = [];

  const traverse = (node, parent = null, depth = 0) => {
    const nodeId = node.name;
    nodes.push({ id: nodeId, name: node.name, color: getNodeColor(depth) });

    if (parent) {
      links.push({ source: parent, target: nodeId });
    }

    if (node.topics && node.topics.length > 0) {
      node.topics.forEach((child) => traverse(child, nodeId, depth + 1));
    }
  };

  traverse(json);
  return { nodes, links };
};

const GraphComponent = () => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  useEffect(() => {
    setGraphData(convertToGraphData(small1));
  }, []);

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        overflow: "hidden",
        position: "fixed",
        top: 0,
        left: 0,
      }}
    >
      <ForceGraph3D
        graphData={graphData}
        nodeAutoColorBy="color" // Use the color from the node data
        linkDirectionalParticles={2}
        linkDirectionalParticleSpeed={0.01}
        nodeLabel="id"
        onNodeClick={(node) => alert(`Clicked node: ${node.name}`)}
        width={window.innerWidth}
        height={window.innerHeight}
      />
    </div>
  );
};

export default GraphComponent;
