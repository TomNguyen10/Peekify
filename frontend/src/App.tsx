import React, { useEffect, useState } from "react";

const App: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      setError("Error fetching data. See console for details.");
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="App">
      <h1>React App with TypeScript and FastAPI Backend</h1>
      {error && <p>{error}</p>}
      {data && (
        <pre>
          <code>{JSON.stringify(data, null, 2)}</code>
        </pre>
      )}
    </div>
  );
};

export default App;
