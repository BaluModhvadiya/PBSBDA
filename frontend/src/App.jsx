import React, { useState } from "react";
import { Chart } from 'react-charts';

function App() {
  const [query, setQuery] = useState("");
  const [sqlOutput, setSqlOutput] = useState("");
  const [latencyOutput, setLatencyOutput] = useState("");
  const [chartData, setChartData] = useState(null);

  const handleQuery = async () => {
    if (query.trim() === "") return;

    try {
      const response = await fetch("http://localhost:8000/process_query/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: query }),
      });

      const data = await response.json();
      if (data.results) {
        setSqlOutput(data.sql_query);
        setLatencyOutput(
          `SQL Generation Time: ${data.latency.sql_generation_time} sec | SQL Execution Time: ${data.latency.sql_execution_time} sec | Total Query Time: ${data.latency.total_time} sec`
        );
        setChartData(data.results); // Assume this contains chart data
      } else {
        setSqlOutput("Error generating SQL query");
        setLatencyOutput("");
        setChartData(null);
      }
    } catch (error) {
      setSqlOutput("Error fetching results");
      setLatencyOutput("");
      setChartData(null);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Sidebar */}
      <div className="w-1/4 bg-gray-800 p-4 flex flex-col items-center">
        <h2 className="text-2xl font-bold mb-6">Big Data Dashboard</h2>
        <button className="py-2 px-4 mb-2 bg-blue-500 rounded">Dashboard</button>
        <button className="py-2 px-4 mb-2 bg-blue-500 rounded">Analytics</button>
        <button className="py-2 px-4 bg-blue-500 rounded">Settings</button>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col items-center justify-center p-10">
        <h1 className="text-4xl font-bold mb-6">Big Data Query Dashboard</h1>

        {/* Query Input */}
        <div className="flex items-center gap-4 mb-6">
          <input
            type="text"
            placeholder="Enter your natural language query..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-3/4 p-2 bg-gray-700 text-white rounded"
          />
          <button
            onClick={handleQuery}
            className="px-6 py-2 bg-green-500 rounded hover:bg-green-400"
          >
            Submit
          </button>
        </div>

        {/* Query Outputs */}
        <div className="text-center">
          <p className="text-blue-400 mb-2">{sqlOutput}</p>
          <p className="text-red-400">{latencyOutput}</p>
        </div>

        {/* Chart */}
        {chartData ? (
          <div className="w-full mt-6 bg-gray-800 p-6 rounded">
            <Chart
              data={chartData} // Update this according to your chart library's API
              options={{
                x: "product_id", // Assuming these are column names
                y: "total_sales",
                type: "bar", // You can change this to line or scatter
              }}
            />
          </div>
        ) : (
          <p className="mt-6 text-gray-500">No Data Available</p>
        )}
      </div>
    </div>
  );
}

export default App;
