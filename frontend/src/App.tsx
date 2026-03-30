import { useState } from "react";

import { Button } from "@chakra-ui/react";

function App() {
  const [response, setResponse] = useState<string>("");

  const sendMessage = async (): Promise<void> => {
    try {
      const res = await fetch("http://127.0.0.1:8000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: "hello from vite" }),
      });

      const data = await res.json();
      setResponse(JSON.stringify(data));
    } catch (err) {
      console.error(err);
      setResponse("Error connecting to backend");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Vite + FastAPI</h1>

      <Button onClick={sendMessage}>
        Send to backend
      </Button>

      <p>Response: {response}</p>
    </div>
  );
}

export default App;
