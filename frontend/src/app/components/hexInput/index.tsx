"use client";

import { label } from "framer-motion/client";
import SvgLoadingCircle from "../svgLoadingCircle";

type HexInputProps = {
    width?: number | string;
    borderColor?: string;
    glow?: boolean;
    glowColor?: string;
    label?: string;
    fontSize?: number | string;
    fontWeight?: number | string;
    placeholder?: string;
    showButton?: boolean;
    buttonBackgroundColor?: string;
    buttonTextColor?: string;
    buttonInnerText?: string;
    updateValue?: (value: string) => void;
    submitAction?: () => void;
    isLoading?: boolean;
}

const HexInput: React.FC<HexInputProps> = ({
    width = "150px",
    borderColor = "white",
    label = null,
    placeholder = null,
    fontSize = "25px",
    fontWeight = 400,
    updateValue = null,
    showButton = true,
    buttonBackgroundColor = "transparent",
    buttonTextColor = "white",
    buttonInnerText = "→",
    submitAction = null,
    isLoading = false,
    glowColor = null,}) => {

    

    return (
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "10px" }}>
            {label && <label style={{ color: "white", fontSize: fontSize, fontWeight: fontWeight }}>{label}</label>}
            <div style={{ display: "flex", flexDirection: "row", gap: "10px" }}>
            <input 
                type="text"
                placeholder={placeholder ? placeholder : undefined}
                onChange={(e) => updateValue ? updateValue(e.target.value) : null}
                onKeyDown={(e) => {
                    if (e.key === 'Enter' && submitAction && !isLoading) {
                        submitAction()
                    }
                }}
                style={{
                    width: width,
                    padding: "10px 15px",
                    fontSize: "1.2rem",
                    borderRadius: "8px",
                    border: `2px solid ${borderColor}`,
                    outline: "none",
                    color: "white",
                    backgroundColor: "transparent",
                    boxShadow: glowColor ? `0 0 10px ${glowColor}` : "none",
                    transition: "box-shadow 0.2s ease, border-color 0.2s ease",
                }}
            />
            
            { showButton && (
            <button 
                style={{
                padding: "10px 20px",
                fontSize: "1.2rem",
                borderRadius: "8px",
                border: `2px solid ${borderColor}`,
                outline: "none",
                color: buttonTextColor,
                backgroundColor: buttonBackgroundColor,
                boxShadow: glowColor ? `0 0 10px ${glowColor}` : "none",
                cursor: "pointer",
                transition: "box-shadow 0.2s ease, background-color 0.2s ease, border-color 0.2s ease",
                }}
                disabled={isLoading}
                onClick={() => submitAction ? submitAction() : null}
            >
                {isLoading ?  buttonInnerText : "loading"}
            </button>)}
            </div>
        </div>
    );
}

export default HexInput;