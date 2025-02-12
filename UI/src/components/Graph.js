import React, { useEffect, useState, useCallback, useRef } from "react";
import { ForceGraph3D } from "react-force-graph";
import * as THREE from "three";
import data from "./small1.json"; // Import your JSON file

// Graph configuration
const graphConfig = {
  nodeColor: "#e8c6a5", // Converted from 0xe8c6a5
  nodeSize: 25,
  nodeHoverColor: "#ffe213", // Converted from 0xffe213
  nodeConnectionColor: "#ffe213", // Converted from 0xffe213
  linkFromColor: "#732196", // Converted from 0x732196
  linkToColor: "#c6492c", // Converted from 0xc6492c
  linkConnectionFromColor: "#ffffff", // Converted from 0xffffff
  linkConnectionToColor: "#ffe213", // Converted from 0xffe213
  springLength: 200,
  springCoeff: 0.001,
  gravity: -10,
  theta: 0.2,
  dragCoeff: 0.3,
  timeStep: 1,
  backgroundColor: "#000000", // Converted from 0x0
};

const Graph = () => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [highlightNodes, setHighlightNodes] = useState(new Set());
  const [highlightLinks, setHighlightLinks] = useState(new Set());
  const [hoverNode, setHoverNode] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const fgRef = useRef();

  // Refs for controls
  const keysPressedRef = useRef({});
  const dragState = useRef(null);

  // Keyboard controls
  useEffect(() => {
    const handleKeyDown = (e) => {
      keysPressedRef.current[e.key.toLowerCase()] = true;
    };
    const handleKeyUp = (e) => {
      keysPressedRef.current[e.key.toLowerCase()] = false;
    };
    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  // WASD movement
  useEffect(() => {
    let animationFrameId;
    const updateCamera = () => {
      if (fgRef.current) {
        const camera = fgRef.current.camera();
        const controls = fgRef.current.controls();
        const moveSpeed = 2;

        const forward = new THREE.Vector3();
        camera.getWorldDirection(forward).normalize();
        const right = new THREE.Vector3();
        right.crossVectors(forward, camera.up).normalize();

        const keys = keysPressedRef.current;
        let translation = new THREE.Vector3(0, 0, 0);
        if (keys.w) translation.add(forward.multiplyScalar(moveSpeed));
        if (keys.s) translation.add(forward.multiplyScalar(-moveSpeed));
        if (keys.a) translation.add(right.multiplyScalar(-moveSpeed));
        if (keys.d) translation.add(right.multiplyScalar(moveSpeed));

        if (translation.lengthSq() > 0) {
          camera.position.add(translation);
          controls.target.add(translation);
          controls.update();
        }
      }
      animationFrameId = requestAnimationFrame(updateCamera);
    };
    updateCamera();
    return () => cancelAnimationFrame(animationFrameId);
  }, []);

  // Highlight updates
  const updateHighlight = useCallback(() => {
    if (!hoverNode) {
      setHighlightNodes(new Set());
      setHighlightLinks(new Set());
      return;
    }
    const connectedNodes = graphData.links
      .filter((link) => link.source === hoverNode || link.target === hoverNode)
      .map((link) => (link.source === hoverNode ? link.target : link.source));
    setHighlightNodes(new Set([hoverNode, ...connectedNodes]));
    setHighlightLinks(
      new Set(
        graphData.links.filter(
          (link) => link.source === hoverNode || link.target === hoverNode
        )
      )
    );
  }, [hoverNode, graphData.links]);

  useEffect(() => updateHighlight(), [hoverNode, updateHighlight]);

  // Data processing from JSON
  useEffect(() => {
    const processTopic = (topic, parentName, nodes, links) => {
      // Add current topic to nodes if not exists
      const existingNode = nodes.find((n) => n.id === topic.name);
      if (!existingNode) {
        nodes.push({
          id: topic.name,
          size: graphConfig.nodeSize,
          connections: 0,
          x: (Math.random() - 0.5) * 500,
          y: (Math.random() - 0.5) * 500,
          z: (Math.random() - 0.5) * 500,
        });
      }

      // Create link if there's a parent
      if (parentName) {
        links.push({
          source: parentName,
          target: topic.name,
          value: Math.random() * 1.5 + 0.5,
        });

        // Update connection counts
        const parentNode = nodes.find((n) => n.id === parentName);
        const childNode = nodes.find((n) => n.id === topic.name);
        if (parentNode) parentNode.connections++;
        if (childNode) childNode.connections++;
      }

      // Process children recursively
      topic.topics.forEach((child) => {
        processTopic(child, topic.name, nodes, links);
      });
    };

    const nodes = [];
    const links = [];
    processTopic(data, null, nodes, links);
    setGraphData({ nodes, links });
  }, []);

  // Initial zoom to fit
  useEffect(() => {
    if (graphData.nodes.length && fgRef.current) {
      setTimeout(() => fgRef.current.zoomToFit(400), 500);
    }
  }, [graphData]);

  // Node interactions
  const handleNodeClick = useCallback((node) => setSelectedNode(node), []);
  const handleNodeHover = useCallback((node) => {
    setHoverNode(node || null);
    document.body.style.cursor = node ? "pointer" : "default";
  }, []);

  // Custom node rendering
  const getNodeObject = useCallback(
    (node) => {
      const isHighlighted = highlightNodes.has(node);
      const group = new THREE.Group();

      // Main sphere for the node
      const sphere = new THREE.Mesh(
        new THREE.SphereGeometry(node.size, 32, 32),
        new THREE.MeshPhongMaterial({
          color: isHighlighted ? graphConfig.nodeHoverColor : graphConfig.nodeColor,
          emissive: isHighlighted ? graphConfig.nodeConnectionColor : 0x000000,
          shininess: 50,
          transparent: true,
          opacity: 0.9,
        })
      );
      group.add(sphere);

      return group;
    },
    [highlightNodes]
  );

  // Engine initialization
  const onEngineInit = useCallback((engine) => {
    // Physics tweaks
    if (engine.d3Force) {
      engine.d3Force("charge").strength(graphConfig.gravity);
      engine.d3Force("link").distance(graphConfig.springLength);
    }

    // Camera settings
    const camera = engine.camera();
    camera.near = 0.1;
    camera.far = 10000;
    camera.updateProjectionMatrix();

    // Controls tweaks
    const controls = engine.controls();
    controls.rotateSpeed = 0.8;
    controls.enableDamping = true;
    controls.dampingFactor = graphConfig.dragCoeff;
    controls.screenSpacePanning = false;

    // Lighting setup
    engine.scene.add(new THREE.AmbientLight(0xffffff, 0.4));
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
    directionalLight.position.set(50, 50, 50);
    engine.scene.add(directionalLight);
  }, []);

  return (
    <div className="relative w-full h-screen bg-gradient-to-br from-black via-gray-900 to-black overflow-hidden">
      <ForceGraph3D
        ref={fgRef}
        graphData={graphData}
        backgroundColor={graphConfig.backgroundColor}
        nodeLabel={(node) =>
          `Course: ${node.id}\nConnections: ${node.connections}`
        }
        nodeResolution={32}
        onNodeClick={handleNodeClick}
        onNodeHover={handleNodeHover}
        nodeThreeObject={getNodeObject}
        linkColor={(link) =>
          highlightLinks.has(link) ? graphConfig.linkConnectionToColor : graphConfig.linkToColor
        }
        linkOpacity={(link) => (highlightLinks.has(link) ? 0.5 : 0.15)}
        linkWidth={() => 2}
        linkDirectionalParticles={3}
        linkDirectionalParticleWidth={(link) =>
          highlightLinks.has(link) ? 3 : 2
        }
        linkDirectionalParticleSpeed={(link) =>
          highlightLinks.has(link) ? 0.006 : 0.004
        }
        linkDirectionalParticleColor={(link) =>
          highlightLinks.has(link) ? graphConfig.linkConnectionToColor : graphConfig.linkToColor
        }
        warmupTicks={100}
        width={window.innerWidth}
        height={window.innerHeight}
        showNavInfo={false}
        enableNavigationControls={true}
        controlType="orbit"
        enableNodeDrag={false}
        onEngineInit={onEngineInit}
      />
    </div>
  );
};

export default Graph;