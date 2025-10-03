import React from "react";
import { useState } from "react";
import HexcorePaths from "./hexcorepaths";

type HexcoreProps = {
  color?: string;
  width?: number | string;
  height?: number | string;
};

const Hexcore: React.FC<HexcoreProps> = ({ color = "white", width = 409, height = 373 }) => {
    const [pressed, setPressed] = useState(false);

  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 409 373"
      xmlns="http://www.w3.org/2000/svg"
      onMouseDown={() => setPressed(true)}
      onMouseUp={() => setPressed(false)}
      onMouseLeave={() => setPressed(false)} 
      onTouchStart={() => setPressed(true)}
      onTouchEnd={() => setPressed(false)}
      style={{
        color: pressed ? "#FF393C" : color,
        cursor: "pointer",
        transition: "color 0.1s, filter 0.1s",
        filter: pressed ? "drop-shadow(0 0 20px #FF393C)" : "none",
      }}
    >
        <HexcorePaths />
    </svg>
  );
};

export default Hexcore;