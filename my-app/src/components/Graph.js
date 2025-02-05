import React, { useEffect, useState, useCallback } from "react";
import { ForceGraph3D } from "react-force-graph";
import neo4j from "neo4j-driver";
import * as THREE from "three";

const Graph = () => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [highlightNodes, setHighlightNodes] = useState(new Set());
  const [highlightLinks, setHighlightLinks] = useState(new Set());
  const [hoverNode, setHoverNode] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);

  const updateHighlight = useCallback(() => {
    if (!hoverNode) {
      setHighlightNodes(new Set());
      setHighlightLinks(new Set());
      return;
    }

    const connectedNodes = graphData.links
      .filter(link => link.source === hoverNode || link.target === hoverNode)
      .map(link => (link.source === hoverNode ? link.target : link.source));

    setHighlightNodes(new Set([hoverNode, ...connectedNodes]));

    const connectedLinks = graphData.links.filter(
      link => link.source === hoverNode || link.target === hoverNode
    );

    setHighlightLinks(new Set(connectedLinks));
  }, [hoverNode, graphData.links]);

  useEffect(() => {
    updateHighlight();
  }, [hoverNode, updateHighlight]);

  useEffect(() => {
    const fetchData = async () => {
      const driver = neo4j.driver(
        "bolt://localhost:7687",
        neo4j.auth.basic("neo4j", "hyperloo")
      );
      const session = driver.session();
      try {
        const result = await session.run(`
          MATCH (c:Course)-[r:PREREQUISITE]->(d:Course)
          RETURN c.course_id AS source, d.course_id AS target
        `);

        // Use a map to store nodes with a set of unique adjacent nodes.
        const nodesMap = new Map();
        const links = [];

        result.records.forEach(record => {
          const sourceId = record.get("source");
          const targetId = record.get("target");
          if (sourceId && targetId) {
            if (!nodesMap.has(sourceId)) {
              nodesMap.set(sourceId, { 
                id: sourceId,
                size: 2,
                neighborSet: new Set()
              });
            }
            if (!nodesMap.has(targetId)) {
              nodesMap.set(targetId, { 
                id: targetId,
                size: 2,
                neighborSet: new Set()
              });
            }

            nodesMap.get(sourceId).neighborSet.add(targetId);
            nodesMap.get(targetId).neighborSet.add(sourceId);

            links.push({ 
              source: sourceId, 
              target: targetId,
              value: Math.random() * 1.5 + 0.5
            });
          }
        });

        const nodes = Array.from(nodesMap.values()).map(node => ({
          id: node.id,
          size: node.size,
          connections: node.neighborSet.size
        }));

        setGraphData({ nodes, links });
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        session.close();
        driver.close();
      }
    };

    fetchData();
  }, []);

  const handleNodeClick = useCallback(node => {
    setSelectedNode(node);
  }, []);

  const handleNodeHover = useCallback(node => {
    setHoverNode(node || null);
    document.body.style.cursor = node ? "pointer" : "default";
  }, []);

  // Improved node three-object with an outline and glow effect
  const getNodeObject = (node) => {
    const isHighlighted = highlightNodes.has(node);
    const group = new THREE.Group();

    // Main sphere
    const sphereGeometry = new THREE.SphereGeometry(node.size, 32, 32);
    const sphereMaterial = new THREE.MeshPhongMaterial({
      color: isHighlighted ? "#ffffff" : "#bbbbbb",
      emissive: isHighlighted ? "#222222" : "#000000",
      shininess: 50,
      transparent: true,
      opacity: 0.9
    });
    const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    group.add(sphere);

    // Glow effect (an outline-like glow)
    const glowGeometry = new THREE.SphereGeometry(node.size * 1.25, 32, 32);
    const glowMaterial = new THREE.ShaderMaterial({
      uniforms: {
        glowColor: { value: new THREE.Color(isHighlighted ? "#ff1493" : "#ff69b4") },
        viewVector: { value: new THREE.Vector3(0, 0, 0) }
      },
      vertexShader: `
        uniform vec3 viewVector;
        varying float intensity;
        void main() {
          vec3 vNormal = normalize(normalMatrix * normal);
          vec3 vNormel = normalize(normalMatrix * viewVector);
          intensity = pow(0.6 - dot(vNormal, vNormel), 2.0);
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 glowColor;
        varying float intensity;
        void main() {
          vec3 glow = glowColor * intensity;
          gl_FragColor = vec4(glow, intensity);
        }
      `,
      side: THREE.BackSide,
      blending: THREE.AdditiveBlending,
      transparent: true
    });
    const glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
    group.add(glowMesh);

    return group;
  };

  return (
    <div className="relative w-full h-screen bg-gradient-to-br from-black via-gray-900 to-black overflow-hidden">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 p-4 z-10">
        <h1 className="text-3xl font-bold text-white opacity-90">
          Course Prerequisites Network
        </h1>
        <p className="text-gray-400 mt-1">
          Interactive visualization of course dependencies
        </p>
      </div>

      {/* Info Panel */}
      <div className="absolute top-24 right-4 z-10">
        <div className="bg-black/70 backdrop-blur-sm border border-gray-800 rounded-lg p-4 text-white w-64">
          <div className="mb-3">
            <h3 className="font-semibold">Network Statistics</h3>
          </div>
          <div className="space-y-2 text-sm">
            <p>Nodes: {graphData.nodes.length}</p>
            <p>Connections: {graphData.links.length}</p>
            {selectedNode && (
              <div className="mt-4 pt-4 border-t border-gray-700">
                <h4 className="font-semibold mb-2">Selected Course</h4>
                <p>ID: {selectedNode.id}</p>
                <p>Connections: {selectedNode.connections}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 left-4 z-10">
        <div className="bg-black/70 backdrop-blur-sm border border-gray-800 rounded-lg p-4 text-white">
          <h3 className="font-semibold mb-2">Legend</h3>
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-pink-500"></div>
              <span>Course Node</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-[2px] bg-pink-400"></div>
              <span>Prerequisite</span>
            </div>
          </div>
        </div>
      </div>

      <ForceGraph3D
        graphData={graphData}
        backgroundColor="rgba(0,0,0,0)"
        nodeLabel={node =>
          `Course: ${node.id}\nConnections: ${node.connections}`
        }
        nodeResolution={32}
        onNodeClick={handleNodeClick}
        onNodeHover={handleNodeHover}
        nodeThreeObject={getNodeObject}
        linkColor={link =>
          highlightLinks.has(link) ? "#ff1493" : "#ff69b4"
        }
        linkOpacity={link => (highlightLinks.has(link) ? 0.5 : 0.15)}
        linkWidth={link =>
          highlightLinks.has(link) ? link.value * 2 : link.value
        }
        linkDirectionalParticles={3}
        linkDirectionalParticleWidth={link =>
          highlightLinks.has(link) ? 3 : 2
        }
        linkDirectionalParticleSpeed={link =>
          highlightLinks.has(link) ? 0.006 : 0.004
        }
        linkDirectionalParticleColor={link =>
          highlightLinks.has(link) ? "#ff1493" : "#ff69b4"
        }
        width={window.innerWidth}
        height={window.innerHeight}
        showNavInfo={false}
        enableNavigationControls={true}
        controlType="orbit"
        enableNodeDrag={false}
        // Add improved lighting to the scene
        onEngineInit={engine => {
          const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
          engine.scene.add(ambientLight);

          const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
          directionalLight.position.set(50, 50, 50);
          engine.scene.add(directionalLight);
        }}
      />
    </div>
  );
};

export default Graph;
