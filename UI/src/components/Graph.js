import React, { useEffect, useState, useRef } from "react";
import ForceGraph3D from "react-force-graph-3d";
import syllabusData from "./stem_majors_syllabus.json";
import majorsData from "./stem_majors.json";

const convertMajorsGraphData = (majors) => {
  const nodes = [{ id: "hyperloo", name: "hyperloo" }];
  const links = [];

  majors.forEach((major) => {
    const majorId = `major-${major}`;
    nodes.push({ id: majorId, name: major });
    links.push({ source: "hyperloo", target: majorId });
  });

  return { nodes, links };
};

const convertCoursesGraphDataForMajor = (courses, majorName) => {
  const nodesLookup = {};
  const links = [];

  const addNode = (id, name) => {
    if (!nodesLookup[id]) {
      nodesLookup[id] = { id, name };
    }
  };

  const majorNodeId = `major-${majorName}`;
  addNode(majorNodeId, majorName);

  courses.forEach((course) => {
    const courseNodeId = `course-${course.course_code}`;
    addNode(courseNodeId, `${course.course_code} - ${course.course_name}`);
    links.push({ source: majorNodeId, target: courseNodeId });

    const traverse = (node, parentId) => {
      if (!node?.name) return;
      const nodeId = `${parentId}-${node.name}`;
      addNode(nodeId, node.name);
      links.push({ source: parentId, target: nodeId });
      node.topics?.forEach((child) => traverse(child, nodeId));
    };

    course.tree && traverse(course.tree, courseNodeId);
  });

  return { nodes: Object.values(nodesLookup), links };
};

const GraphComponent = () => {
  const [mode, setMode] = useState("majors");
  const [selectedMajor, setSelectedMajor] = useState(null);
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [searchTerm, setSearchTerm] = useState("");
  const [searchSuggestions, setSearchSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const graphRef = useRef();
  const searchContainerRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchContainerRef.current && !searchContainerRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const loadGraphData = (data) => {
    setGraphData(data);
    setTimeout(() => {
      graphRef.current?.d3ReheatSimulation();
    }, 0);
  };

  useEffect(() => {
    if (mode === "majors") {
      loadGraphData(convertMajorsGraphData(majorsData));
    } else if (mode === "courses" && selectedMajor) {
      const filteredCourses = syllabusData.filter(
        (course) => course.major_name === selectedMajor
      );
      loadGraphData(convertCoursesGraphDataForMajor(filteredCourses, selectedMajor));
    }
    // Reset search state when graph changes
    setSearchTerm('');
    setSearchSuggestions([]);
    setShowSuggestions(false);
  }, [mode, selectedMajor]);

  const handleNodeClick = (node) => {
    if (mode === "majors" && node.id !== "hyperloo") {
      setSelectedMajor(node.name);
      setMode("courses");
    }
  };

  const handleBack = () => {
    setMode("majors");
    setSelectedMajor(null);
  };

  const handleSearch = (node) => {
    if (!node || !graphRef.current) return;

    const nodePosition = {
      x: node.x || Math.random() * 100,
      y: node.y || Math.random() * 100,
      z: node.z || Math.random() * 100,
    };

    const distance = 100;
    const distRatio = 1 + distance / Math.hypot(nodePosition.x, nodePosition.y, nodePosition.z);

    graphRef.current.cameraPosition(
      { x: nodePosition.x * distRatio, y: nodePosition.y * distRatio, z: nodePosition.z * distRatio },
      nodePosition,
      1000
    );
  };

  const handleSearchInput = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    
    if (value.length > 0) {
      const filtered = graphData.nodes.filter(node =>
        node.name.toLowerCase().includes(value.toLowerCase())
      );
      setSearchSuggestions(filtered);
      setShowSuggestions(true);
    } else {
      setSearchSuggestions([]);
      setShowSuggestions(false);
    }
  };

  return (
    <div style={{ width: "100vw", height: "100vh", position: "relative", background: "#1a1a1a" }}>
      {/* Search Container */}
      <div
        ref={searchContainerRef}
        style={{
          position: "absolute",
          zIndex: 1000,
          top: 20,
          right: 20,
          width: "300px",
          backgroundColor: "rgba(30, 30, 30, 0.9)",
          borderRadius: "8px",
          backdropFilter: "blur(4px)",
          boxShadow: "0 2px 8px rgba(0, 0, 0, 0.4)",
        }}
      >
        <div style={{ position: "relative" }}>
          <input
            type="text"
            placeholder="Search nodes..."
            value={searchTerm}
            onChange={handleSearchInput}
            onFocus={() => setShowSuggestions(true)}
            style={{
              width: "100%",
              padding: "12px 16px",
              background: "rgba(40, 40, 40, 0.9)",
              border: "1px solid #333",
              color: "#ffffff",
              fontSize: "14px",
              outline: "none",
              borderRadius: "8px",
            }}
          />
          
          {/* Suggestions Dropdown */}
          {showSuggestions && searchSuggestions.length > 0 && (
            <div style={{
              position: "absolute",
              top: "100%",
              left: 0,
              right: 0,
              maxHeight: "300px",
              overflowY: "auto",
              backgroundColor: "rgba(30, 30, 30, 0.95)",
              borderRadius: "0 0 8px 8px",
              zIndex: 1001,
              boxShadow: "0 4px 12px rgba(0, 0, 0, 0.5)",
            }}>
              {searchSuggestions.map((node, index) => (
                <div
                  key={index}
                  onClick={() => {
                    setSearchTerm(node.name);
                    handleSearch(node);
                    setShowSuggestions(false);
                  }}
                  style={{
                    padding: "10px 16px",
                    color: "#ffffff",
                    cursor: "pointer",
                    borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
                    transition: "background 0.2s",
                    fontSize: "14px",
                  }}
                  onMouseEnter={(e) => e.target.style.backgroundColor = "rgba(255, 255, 255, 0.1)"}
                  onMouseLeave={(e) => e.target.style.backgroundColor = "transparent"}
                >
                  {node.name}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Back Button */}
      {mode === "courses" && (
        <button
          style={{
            position: "absolute",
            zIndex: 1000,
            top: 20,
            left: 20,
            padding: "10px 20px",
            backgroundColor: "rgba(30, 30, 30, 0.9)",
            color: "#ffffff",
            border: "1px solid #333",
            borderRadius: "8px",
            cursor: "pointer",
            backdropFilter: "blur(4px)",
            transition: "all 0.2s",
          }}
          onMouseEnter={(e) => e.target.style.backgroundColor = "rgba(40, 40, 40, 0.9)"}
          onMouseLeave={(e) => e.target.style.backgroundColor = "rgba(30, 30, 30, 0.9)"}
          onClick={handleBack}
        >
          ← Back to Majors
        </button>
      )}

      <ForceGraph3D
        ref={graphRef}
        graphData={graphData}
        nodeAutoColorBy="id"
        linkDirectionalParticles={2}
        linkDirectionalParticleSpeed={0.01}
        nodeLabel="name"
        dagMode={mode === "courses" ? "td" : null}
        dagLevelDistance={mode === "courses" ? 300 : 0}
        onNodeClick={handleNodeClick}
        nodeRelSize={10}
        cooldownTicks={100}
        warmupTicks={10}
        numDimensions={3}
        backgroundColor="#1a1a1a"
        linkColor={() => "rgba(150, 150, 150, 0.3)"}
      />
    </div>
  );
};

export default GraphComponent;