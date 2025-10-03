"use client";
import Hexcore from "./components/hexcore";
import AnimatedHexcore from "./components/animatedHexcore";

const Home: React.FC = () => {
  
  return (
    <main>
      <Hexcore color="white" width={200} height={200} />
      <AnimatedHexcore />
    </main>
  )
};

export default Home;
