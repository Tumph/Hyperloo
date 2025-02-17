import React, { useEffect, useState, useRef } from "react";
import ForceGraph3D from "react-force-graph-3d";
import syllabusData from "./stem_majors_syllabus.json";
import majorsData from "./stem_majors.json";

//These functions convert raw data into a format suitable for the graph.
const convertMajorsGraphData = (majors) => {
  const nodes = [{ id: "Hyperloo", name: "Hyperloo" }];
  const links = [];

  majors.forEach((major) => {
    const majorId = `major-${major}`;
    nodes.push({ id: majorId, name: major });
    links.push({ source: "Hyperloo", target: majorId });
  });

  nodes.forEach((node) => {
    node.links = links.filter((l) => l.source === node || l.target === node);
    node.neighbors = [
      ...new Set([
        ...links.filter((l) => l.source === node).map((l) => l.target),
        ...links.filter((l) => l.target === node).map((l) => l.source),
      ]),
    ];
  });

  return { nodes, links };
};

//These functions convert raw data into a format suitable for the graph.
const convertCoursesGraphDataForMajor = (courses, majorName) => {
  const nodesLookup = {};
  const links = [];

  const addNode = (id, name) => {
    if (!nodesLookup[id]) {
      nodesLookup[id] = { id, name };
    }
    return nodesLookup[id]; // Return node reference
  };

  const majorNode = addNode(`major-${majorName}`, majorName);

  courses.forEach((course) => {
    const courseNode = addNode(
      `course-${course.course_code}`,
      `${course.course_code} - ${course.course_name}`,
    );

    // Create link between major and course using node objects
    links.push({ source: majorNode, target: courseNode });

    const traverse = (node, parentNode) => {
      // Pass parent node object
      if (!node?.name) return;

      const childNode = addNode(`${parentNode.id}-${node.name}`, node.name);

      // Create parent-child link using node objects
      links.push({ source: parentNode, target: childNode });

      node.topics?.forEach((child) => traverse(child, childNode));
    };

    course.tree && traverse(course.tree, courseNode);
  });

  const nodes = Object.values(nodesLookup);

  // Process relationships using actual node references
  nodes.forEach((node) => {
    node.links = links.filter((l) => l.source === node || l.target === node);
    node.neighbors = [
      ...new Set([
        ...links.filter((l) => l.source === node).map((l) => l.target),
        ...links.filter((l) => l.target === node).map((l) => l.source),
      ]),
    ];
  });

  return { nodes, links };
};

//These functions convert raw data into a format suitable for the graph.
const convertCourseGraphDataForCourse = (course) => {
  const nodesLookup = {};
  const links = [];

  const addNode = (id, name) => {
    if (!nodesLookup[id]) {
      nodesLookup[id] = { id, name };
    }
    return nodesLookup[id]; // Return node reference
  };

  const courseNode = addNode(
    `course-${course.course_code}`,
    `${course.course_code} - ${course.course_name}`,
  );

  const traverse = (node, parentNode) => {
    // Pass parent node object
    if (!node?.name) return;

    const childNode = addNode(`${parentNode.id}-${node.name}`, node.name);

    // Create parent-child link using node objects
    links.push({ source: parentNode, target: childNode });

    node.topics?.forEach((child) => traverse(child, childNode));
  };

  course.tree && traverse(course.tree, courseNode);

  const nodes = Object.values(nodesLookup);

  // Process relationships using actual node references
  nodes.forEach((node) => {
    node.links = links.filter((l) => l.source === node || l.target === node);
    node.neighbors = [
      ...new Set([
        ...links.filter((l) => l.source === node).map((l) => l.target),
        ...links.filter((l) => l.target === node).map((l) => l.source),
      ]),
    ];
  });

  return { nodes, links };
};

//This is the main React component that renders the entire graph interface.
const GraphComponent = () => {
  //These declare and initialize state variables used throughout the component.
  const [mode, setMode] = useState("majors");
  const [selectedMajor, setSelectedMajor] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [searchTerm, setSearchTerm] = useState("");
  const [searchSuggestions, setSearchSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlightNodes, setHighlightNodes] = useState(new Set());
  const [highlightLinks, setHighlightLinks] = useState(new Set());
  const [hoverNode, setHoverNode] = useState(null);

  //These create references to DOM elements for direct manipulation.
  const graphRef = useRef();
  const searchContainerRef = useRef(null);

  //This effect handles closing the search suggestions when clicking outside.
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        searchContainerRef.current &&
        !searchContainerRef.current.contains(event.target)
      ) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  //This function loads new graph data and triggers a graph reheat.
  const loadGraphData = (data) => {
    setGraphData(data);
    setTimeout(() => {
      graphRef.current?.d3ReheatSimulation();
    }, 0);
  };

  //This effect updates the graph data when the mode or selected major changes.
  useEffect(() => {
    if (mode === "majors") {
      loadGraphData(convertMajorsGraphData(majorsData));
    } else if (mode === "courses" && selectedMajor) {
      const filteredCourses = syllabusData.filter(
        (course) => course.major_name === selectedMajor,
      );
      loadGraphData(
        convertCoursesGraphDataForMajor(filteredCourses, selectedMajor),
      );
    } else if (mode === "individualCourses" && selectedCourse) {
      const filteredCourses = syllabusData.filter(
        (course) => course.course_code === selectedCourse,
      );
      const filteredCourses1 = filteredCourses.filter(
        (course) => course.major_name === selectedMajor,
      );
      loadGraphData(convertCourseGraphDataForCourse(filteredCourses1[0]));
    }

    // Reset search state when graph changes
    setSearchTerm("");
    setSearchSuggestions([]);
    setShowSuggestions(false);
    setHighlightNodes(new Set());
    setHighlightLinks(new Set());
    setHoverNode(null);
  }, [mode, selectedMajor, selectedCourse]);

  //This function handles clicks on graph nodes.
  const handleNodeClick = (node) => {
    if (mode === "majors" && node.id !== "hyperloo") {
      setSelectedMajor(node.name);
      setMode("courses");
    }
    if (mode === "courses" && node.id.startsWith("course-")) {
      const courseCode = node.id.split("-")[1];
      setSelectedCourse(courseCode);
      setMode("individualCourses");
    }
    if (mode === "individualCourses") {
      const getParentNodes = (node) => {
        const parents = graphData.links
          .filter((link) => link.target === node)
          .map((link) => link.source);
        const parentNames = parents.map((parent) => parent.name);
        const grandParents = parents.flatMap((parent) =>
          getParentNodes(parent),
        );
        return [...parentNames, ...grandParents];
      };

      const text = [node.name, ...getParentNodes(node)].join(", ");
      const perplexityquery = encodeURIComponent(text);
      const fullurl =
        "Here is the name of the course, and all of the larger topics this smaller topic fits into. The last topic is the main topic you need to explain. Explain this topic like I am a 13 year old. " +
        perplexityquery;
      const perplexityurl = `https://www.perplexity.ai/search?q=${fullurl}`;

      window.open(perplexityurl, "_blank").focus();
    }
  };

  const handleNodeRightClick = (node) => {
    if (mode === "individualCourses") {
      const getParentNodes = (node) => {
        const parents = graphData.links
          .filter((link) => link.target === node)
          .map((link) => link.source);
        const parentNames = parents.map((parent) => parent.name);
        const grandParents = parents.flatMap((parent) =>
          getParentNodes(parent),
        );
        return [...parentNames, ...grandParents];
      };

      const text = [node.name, ...getParentNodes(node)].join(", ");

      const chromeurl =
        "http://www.google.com/search?q=" + text + "open course";
      window.open(chromeurl, "_blank");
    }
  };

  // Add hover handlers
  const handleNodeHover = (node) => {
    if (node) {
      const neighbors = new Set([node, ...(node.neighbors || [])]);
      const links = new Set(node.links || []);

      // Add parent nodes (for hierarchical graphs)
      const parents = graphData.links
        .filter((link) => link.target === node)
        .map((link) => link.source);
      parents.forEach((parent) => neighbors.add(parent));

      setHighlightNodes(neighbors);
      setHighlightLinks(links);
      setHoverNode(node);
    } else {
      setHighlightNodes(new Set());
      setHighlightLinks(new Set());
      setHoverNode(null);
    }
  };

  //This function handles the back button click.
  const handleBack = () => {
    if (mode === "courses") {
      setMode("majors");
      setSelectedMajor(null);
    } else if (mode === "individualCourses") {
      setMode("courses");
      setSelectedCourse(null);
    }
  };

  //This function handles searching for and focusing on a specific node.
  const handleSearch = (node) => {
    if (!node || !graphRef.current) return;

    const nodePosition = {
      x: node.x || Math.random() * 100,
      y: node.y || Math.random() * 100,
      z: node.z || Math.random() * 100,
    };

    const distance = 100;
    const distRatio =
      1 + distance / Math.hypot(nodePosition.x, nodePosition.y, nodePosition.z);

    graphRef.current.cameraPosition(
      {
        x: nodePosition.x * distRatio,
        y: nodePosition.y * distRatio,
        z: nodePosition.z * distRatio,
      },
      nodePosition,
      1000,
    );
  };

  //This function handles changes in the search input field.
  const handleSearchInput = (e) => {
    const value = e.target.value;
    setSearchTerm(value);

    if (value.length > 0) {
      const filtered = graphData.nodes.filter((node) =>
        node.name.toLowerCase().includes(value.toLowerCase()),
      );
      setSearchSuggestions(filtered);
      setShowSuggestions(true);
    } else {
      setSearchSuggestions([]);
      setShowSuggestions(false);
    }
  };

  //This is the main render function that returns the JSX for the component.
  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        position: "relative",
        background: "#1a1a1a",
      }}
    >
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
            <div
              style={{
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
              }}
            >
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
                  onMouseEnter={(e) =>
                    (e.target.style.backgroundColor =
                      "rgba(255, 255, 255, 0.1)")
                  }
                  onMouseLeave={(e) =>
                    (e.target.style.backgroundColor = "transparent")
                  }
                >
                  {node.name}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      {/* CoursesBack Button */}
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
          onMouseEnter={(e) =>
            (e.target.style.backgroundColor = "rgba(40, 40, 40, 0.9)")
          }
          onMouseLeave={(e) =>
            (e.target.style.backgroundColor = "rgba(30, 30, 30, 0.9)")
          }
          onClick={handleBack}
        >
          ← Back to Majors
        </button>
      )}
      {/* individualCourses Back Button */}
      {mode === "individualCourses" && (
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
          onMouseEnter={(e) =>
            (e.target.style.backgroundColor = "rgba(40, 40, 40, 0.9)")
          }
          onMouseLeave={(e) =>
            (e.target.style.backgroundColor = "rgba(30, 30, 30, 0.9)")
          }
          onClick={handleBack}
        >
          ← Back to All Courses in Major
        </button>
      )}
      {/* This is the main 3D force graph component that visualizes the data. */}
      <ForceGraph3D
        ref={graphRef}
        graphData={graphData}
        nodeAutoColorBy="id"
        nodeColor={
          (node) =>
            highlightNodes.has(node)
              ? node === hoverNode
                ? "#ff0000"
                : "#ffa500"
              : "#8a68c4" // Use auto-generated color from nodeAutoColorBy
        }
        linkDirectionalParticleSpeed={0.01}
        nodeLabel="name"
        dagMode={
          mode === "courses" ? "td" : mode === "individualCourses" ? "lr" : null
        }
        dagLevelDistance={
          mode === "courses" ? 300 : mode === "individualCourses" ? 100 : 0
        }
        onNodeClick={handleNodeClick}
        onNodeRightClick={handleNodeRightClick}
        nodeRelSize={10}
        cooldownTicks={100}
        warmupTicks={10}
        numDimensions={3}
        backgroundColor="#1a1a1a"
        linkColor={() => "rgba(255, 255, 255, 0.5)"}
        onNodeHover={handleNodeHover}
        controlType="orbit"
        linkWidth={(link) => (highlightLinks.has(link) ? 4 : 1)}
        linkDirectionalParticles={(link) => (highlightLinks.has(link) ? 4 : 0)}
        linkDirectionalParticleWidth={0.8}
      />
    </div>
  );
};

export default GraphComponent;
