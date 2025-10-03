import { motion } from "framer-motion";
import Hexcore from "../hexcore"

export default function AnimatedHexcore() {
  return (
    <motion.div
      style={{ display: "inline-block", cursor: "pointer" }}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      animate={{
        rotate: [0, 1440, 1440], 
        y: [0, -10, 10, -10, 0], 
      }}
      transition={{
        rotate: {
          duration: 1,
          times: [0, 0.25, 1],
          repeat: Infinity,
          ease: "easeInOut",
        },
        y: {
          duration: 1,
          repeatDelay: 5,
          repeat: Infinity,
          ease: "easeInOut",
        },
      }}
    >
      <Hexcore color="blue" width={200} height={200} />
    </motion.div>
  );
}