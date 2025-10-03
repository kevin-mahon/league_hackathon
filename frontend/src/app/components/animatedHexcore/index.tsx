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
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      animate={{
        rotate: [0, 1440, 1440], 
        y: [0, 10, 0], 
      }}
      transition={{
        rotate: {
          duration: 1,
          times: [0, 0.25, 1],
          repeat: Infinity,
          repeatDelay: 5,
          ease: "easeInOut",
        },
        y: {
          duration: 1,
          repeat: Infinity,
          ease: "easeInOut",
        },
      }}
    >
      <Hexcore color={color} width={width} height={height} />
    </motion.div>
  );
};

export default AnimatedHexcore;
