import React, { useEffect, useState } from "react";
import { ForceGraph3D } from "react-force-graph";
import neo4j from "neo4j-driver";

const Graph = () => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  useEffect(() => {
    const fetchData = async () => {
      const driver = neo4j.driver(
        "bolt://localhost:7687", // Replace with your Neo4j instance
        neo4j.auth.basic("neo4j", "hyperloo") // Replace with your credentials
      );

      const session = driver.session();
      try {
        const result = await session.run(`
          MATCH (c:Course)-[r:PREREQUISITE]->(d:Course)
          RETURN c.course_id AS source, d.course_id AS target
        `);

        const nodes = new Set();
        const links = [];

        result.records.forEach(record => {
          const source = record.get("source");
          const target = record.get("target");

          nodes.add(source);
          nodes.add(target);
          links.push({ source, target });
        });

        setGraphData({
          nodes: Array.from(nodes).map(course => ({ id: course })),
          links: links,
        });
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        session.close();
        driver.close();
      }
    };

    fetchData();
  }, []);

  return (
    <div className="w-full h-screen bg-gray-900">
      <ForceGraph3D
        graphData={graphData}
        nodeAutoColorBy="id"
        linkDirectionalParticles={2}
        linkDirectionalParticleSpeed={0.005}
      />
    </div>
  );
};

export default Graph;
