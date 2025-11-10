"use client";
//Hooks and State Management
import { useState, useEffect, use } from "react";
import { useStatsStore } from "../store/useStatsStore";
//Components
import Hexcore from "./components/hexcore";
import AnimatedHexcore from "./components/animatedHexcore";
import HexInput from "./components/hexInput";
import Particles from "./components/particles";
//APIs
import getStatsWithLeagueID from "../api/getStatsWithLeagueID";



const DEFAULT_COLOR = "#131474";
const ERROR_COLOR = "#74136A";

const Home: React.FC = () => {

  const [gradientColor, setGradientColor] = useState(DEFAULT_COLOR);
  const [inputError, setInputError] = useState(false);
  const [errorMessage, setErrorMessage] = useState(" ");
  const [isLoading, setIsLoading] = useState(false);
  
  const [inputValue, setInputValue] = useState("");
  //Zustand store to hold api stats globally
  const setApiStats = useStatsStore((state) => state.setApiStats);

  const updateValue = (value: string): void => {
    setInputValue(value);
    setInputError(false);
    setErrorMessage(" ");
    setGradientColor(DEFAULT_COLOR);
  };

  async function submitLeagueID(leagueID: string) {
    if (!/^\d{8}$/.test(leagueID)) {
      setInputError(true);
      setErrorMessage("League ID must be exactly 8 digits.");
      setGradientColor(ERROR_COLOR);
      return;
    }
    else {
      try {
        setIsLoading(true);
        const response = await getStatsWithLeagueID(inputValue, true); 
        console.log(response);
        if (response.status === 200) {
          console.log(response);
          setGradientColor(DEFAULT_COLOR);
          setInputError(false);
          setErrorMessage(" ");

          //setting the global state with api response using Zustand
          setApiStats(response.data);
        }
      } catch (error: any) {
        setInputError(true);
        setErrorMessage("An error occurred.");
        setGradientColor(ERROR_COLOR);
        console.error(error);
        return;
      } finally {
        setIsLoading(false);
      }
    }
  }

  

  return (
    <main
      style={{
        width: "100vw",
        height: "100vh",
        display: "flex",
        gap: "15px",
        justifyContent: "center",
        flexDirection: "column",
        alignItems: "center",
        background: `radial-gradient(circle, ${gradientColor} 0%, black 100%)`,
        transition: "any 0.2s ease",
      }}
    >
      <div style={{ width: '100%', height: '600px', position: 'relative' }}>
        <Particles
          particleColors={['#ffffff', '#ffffff']}
          particleCount={200}
          particleSpread={10}
          speed={0.1}
          particleBaseSize={100}
          moveParticlesOnHover={true}
          alphaParticles={false}
          disableRotation={false}
        />
        <div style={{
          position: 'absolute', 
          top: 0, 
          left: 0, 
          width: '100%', 
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          gap: '20px' 
        }}>
         <AnimatedHexcore color={inputError ? "#FF393C" : "#89EFFF"}/>
      <HexInput
        width={"200px"}
        borderColor="white"
        glowColor={inputError ? "red": "#44A8FF"}
        label="Enter Your League ID"
        fontSize={"25px"}
        placeholder = "e.g. 17822832"
        updateValue={updateValue}
        submitAction={() => submitLeagueID(inputValue)}
        isLoading={isLoading}
      />
      <h2 style={{color: "red"}}>{errorMessage}</h2>
      </div>
      </div>
     
    </main>
  );
};

export default Home;
