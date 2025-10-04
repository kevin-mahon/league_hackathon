import React from "react";
import { motion } from "framer-motion";
import Hexcore from "../hexcore";

type AnimatedHexcoreProps = {
  color?: string;
  width?: number | string;
  height?: number | string;
};

const AnimatedHexcore: React.FC<AnimatedHexcoreProps> = ({
  color = "white",
  width = 200,
  height = 200,
}) => {
  return (
    <motion.div
      style={{ display: "inline-block", cursor: "pointer" }}
      animate={{
        y: [0, -4, 0],        
        scale: [1, 1.05, 1],  
      }}
      transition={{
        duration: 3,
        repeat: Infinity,
        ease: "easeInOut",
      }}
    >
      <Hexcore color={color} width={width} height={height} />
    </motion.div>
  );
};

export default AnimatedHexcore;
