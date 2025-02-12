import React from "react";
import Graph from "./components/Graph";
import SearchBar from "./components/SearchBar";

//username and password is hyperloo

function App() {
  return (
    <div className="h-screen bg-black text-white">
      <div className="flex justify-center">
        <SearchBar />
      </div>
      <Graph />
    </div>
  );
}

export default App;
