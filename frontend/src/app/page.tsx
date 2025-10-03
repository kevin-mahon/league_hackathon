"use client";
import { useState, useEffect } from "react";

import Hexcore from "./components/hexcore";
import AnimatedHexcore from "./components/animatedHexcore";
import HexInput from "./components/hexInput";


const Home: React.FC = () => {
  const DEFAULT_COLOR = "#131474";
  const PRESSED_COLOR = "#74136A";

  const [gradientColor, setGradientColor] = useState(DEFAULT_COLOR);
  const [inputError, setInputError] = useState(false);
  

  return (
    <main
      style={{
        width: "100vw",
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        flexDirection: "column",
        alignItems: "center",
        background: `radial-gradient(circle, ${gradientColor} 0%, black 100%)`,
        transition: "any 0.2s ease",
      }}
    >
      <AnimatedHexcore color="#89EFFF"/>
      <HexInput
        width={"250px"}
        borderColor="white"
        glowColor={inputError ? "red": "#44A8FF"}
        label="Enter Your League ID"
        fontSize={"25px"}
        placeholder = "e.g. 17822832"
      />
    </main>
  );
};

export default Home;
