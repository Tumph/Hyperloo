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
  const graphRef = useRef();

  const loadGraphData = (data) => {
    setGraphData(data);
    // Reheat simulation after data loads
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

  return (
    <div style={{ width: "100vw", height: "100vh", overflow: "hidden" }}>
      {mode === "courses" && (
        <button
          style={{
            position: "absolute",
            zIndex: 1,
            top: 10,
            left: 10,
            padding: "8px 16px",
          }}
          onClick={handleBack}
        >
          Back to Majors
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
        // Improved layout configuration
        cooldownTicks={100}
        warmupTicks={10}
        numDimensions={3}
      />
    </div>
  );
};

export default GraphComponent;