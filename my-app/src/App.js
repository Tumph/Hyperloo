import React from "react";
import Graph from "./components/Graph";

//username and password is hyperloo

function App() {
  return (
    <div className="h-screen bg-black text-white">
      <h1 className="text-2xl text-center py-4">University of Waterloo Courses</h1>
      <Graph />
    </div>
  );
}

export default App;
