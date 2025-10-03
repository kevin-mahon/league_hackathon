"use client";
import LaserFlow from '../components/LaserFlow';
import StarBorder from "../components/starBorder";
import FadeContent from '../components/fadeContent';
import { useRef } from 'react';
import AnimatedHexcore from '../components/animatedHexcore';

export default function Intro() {
    
    return (        
    <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
        <LaserFlow />
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
    }}>
        <FadeContent blur={true} duration={1000} easing="ease-out" initialOpacity={0}>
        
            <AnimatedHexcore color={"#89EFFF"}/>
        </FadeContent>
        <FadeContent blur={true} duration={3000} easing="ease-out" initialOpacity={0}>
            <h1 style={{fontSize: "40px"}}>Click the Hexcore to get started</h1>
        </FadeContent>
    </div>
    </div>
    )
}