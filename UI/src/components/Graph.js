import React, { useEffect, useState, useCallback, useRef } from "react";
import { ForceGraph3D } from "react-force-graph";
import neo4j from "neo4j-driver";
import * as THREE from "three";

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

  // Data fetching from Neo4j
  useEffect(() => {
    const fetchData = async () => {
      const driver = neo4j.driver(
        "bolt://localhost:7687",
        neo4j.auth.basic("neo4j", "hyperloo")
      );
      const session = driver.session();
      try {
        const nodesResult = await session.run(
          `MATCH (n:Topic) RETURN n.name AS id`
        );
        const nodes = nodesResult.records.map((record) => ({
          id: record.get("id"),
          // You can adjust size based on connection count if desired.
          size: 7, // Increased node size
          connections: 0,
          // Initial positions (will be overridden by DAG layout)
          x: (Math.random() - 0.5) * 500,
          y: (Math.random() - 0.5) * 500,
          z: (Math.random() - 0.5) * 500,
        }));
        const nodesMap = new Map(nodes.map((node) => [node.id, node]));

        const linksResult = await session.run(
          `MATCH (c:Topic)-[r:HAS_SUBTOPIC]->(d:Topic)
           RETURN c.name AS source, d.name AS target`
        );
        const links = linksResult.records.map((record) => {
          const source = record.get("source");
          const target = record.get("target");
          if (nodesMap.has(source)) nodesMap.get(source).connections += 1;
          if (nodesMap.has(target)) nodesMap.get(target).connections += 1;
          return { source, target, value: Math.random() * 1.5 + 0.5 };
        });

        setGraphData({ nodes: Array.from(nodesMap.values()), links });
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        session.close();
        driver.close();
      }
    };
    fetchData();
  }, []);

  // Initial zoom to fit
  useEffect(() => {
    if (graphData.nodes.length && fgRef.current) {
      setTimeout(() => fgRef.current.zoomToFit(400), 500);
    }
  }, [graphData]);

  // Enhanced panning controls
  useEffect(() => {
    if (fgRef.current) {
      const canvas = fgRef.current.renderer().domElement;
      const ROTATION_SPEED = 0.005;

      const onMouseDown = (e) => {
        if (e.button === 2) {
          e.preventDefault();
          dragState.current = {
            startX: e.clientX,
            startY: e.clientY,
          };
        }
      };

      const onMouseMove = (e) => {
        if (!dragState.current) return;
        e.preventDefault();

        const deltaX = e.clientX - dragState.current.startX;
        const deltaY = e.clientY - dragState.current.startY;

        const camera = fgRef.current.camera();
        const controls = fgRef.current.controls();

        controls.rotateLeft(deltaX * ROTATION_SPEED);
        controls.rotateUp(deltaY * ROTATION_SPEED);
        controls.update();

        dragState.current.startX = e.clientX;
        dragState.current.startY = e.clientY;
      };

      const onMouseUp = () => (dragState.current = null);

      canvas.addEventListener("mousedown", onMouseDown);
      canvas.addEventListener("mousemove", onMouseMove);
      canvas.addEventListener("mouseup", onMouseUp);
      canvas.addEventListener("mouseleave", onMouseUp);
      canvas.addEventListener("contextmenu", (e) => e.preventDefault());

      return () => {
        canvas.removeEventListener("mousedown", onMouseDown);
        canvas.removeEventListener("mousemove", onMouseMove);
        canvas.removeEventListener("mouseup", onMouseUp);
        canvas.removeEventListener("mouseleave", onMouseUp);
        canvas.removeEventListener("contextmenu", (e) => e.preventDefault());
      };
    }
  }, [fgRef]);

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
          color: isHighlighted ? "#ffffff" : "#bbbbbb",
          emissive: isHighlighted ? "#222222" : "#000000",
          shininess: 50,
          transparent: true,
          opacity: 0.9,
        })
      );
      group.add(sphere);

      // Glow effect
      const glowMaterial = new THREE.ShaderMaterial({
        uniforms: {
          glowColor: {
            value: new THREE.Color(
              isHighlighted ? "#ff1493" : "#ff69b4"
            ),
          },
          viewVector: { value: new THREE.Vector3(0, 0, 0) },
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
        transparent: true,
      });
      const glow = new THREE.Mesh(
        new THREE.SphereGeometry(node.size * 1.25, 32, 32),
        glowMaterial
      );
      group.add(glow);

      return group;
    },
    [highlightNodes]
  );

  // Engine initialization
  const onEngineInit = useCallback((engine) => {
    // Physics tweaks
    if (engine.d3Force) {
      engine.d3Force("charge").strength(-50); // Adjusted charge strength
      engine.d3Force("link").distance(200); // Increased link distance
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
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;

    // Lighting setup
    engine.scene.add(new THREE.AmbientLight(0xffffff, 0.4));
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
    directionalLight.position.set(50, 50, 50);
    engine.scene.add(directionalLight);
  }, []);

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
        ref={fgRef}
        graphData={graphData}
        dagMode="td" // Arrange nodes top-down so parent (big) topics are on top.
        dagLevelDistance={100} // Reduced vertical spacing between levels.
        backgroundColor="rgba(0,0,0,0)"
        nodeLabel={(node) =>
          `Course: ${node.id}\nConnections: ${node.connections}`
        }
        nodeResolution={32}
        onNodeClick={handleNodeClick}
        onNodeHover={handleNodeHover}
        nodeThreeObject={getNodeObject}
        linkColor={(link) =>
          highlightLinks.has(link) ? "#ff1493" : "#ff69b4"
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
          highlightLinks.has(link) ? "#ff1493" : "#ff69b4"
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