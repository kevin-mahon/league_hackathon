"use client";

import { motion } from "framer-motion";

export default function SvgLoadingCircle() {
  const circleVariants = {
    animate: {
      rotate: 360,
      transition: {
        repeat: Infinity,
        duration: 1,
        ease: "linear",
      },
    },
  };

  const pathVariants = {
    animate: {
      strokeDashoffset: [0, 100, 0],
      transition: {
        repeat: Infinity,
        duration: 1.5,
        ease: "easeInOut",
      },
    },
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "80px",
      }}
    >
      <motion.svg
        width="80px"
        height="80px"
        viewBox="0 0 50 50"
        variants={circleVariants}
        animate="animate"
      >
        <motion.circle
          cx="50"
          cy="50"
          r="40"
          fill="transparent"
          stroke="#3498db"
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray="251.2" // circumference = 2πr ≈ 2*3.14*40
          strokeDashoffset="251.2"
          variants={pathVariants}
          animate="animate"
        />
      </motion.svg>
    </div>
  );
}
