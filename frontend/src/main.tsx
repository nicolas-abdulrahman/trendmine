import React from "react";
import ReactDOM from "react-dom/client";
import TrendMineGame from "./App";

import { ChakraProvider } from "@chakra-ui/react";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
      <TrendMineGame />
  </React.StrictMode>
);
