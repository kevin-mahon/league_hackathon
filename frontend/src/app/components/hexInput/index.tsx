"use client";

import { label } from "framer-motion/client";

type HexInputProps = {
    width?: number | string;
    borderColor?: string;
    glow?: boolean;
    glowColor?: string;
    label?: string;
    fontSize?: number | string;
    fontWeight?: number | string;
    placeholder?: string;
    updateValue?: (value: string) => void;
}

const HexInput: React.FC<HexInputProps> = ({
    width = 300,
    borderColor = "white",
    label = null,
    placeholder = null,
    fontSize = "25px",
    fontWeight = 400,
    updateValue = null,
    glowColor = null,}) => {

    

    return (
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "10px" }}>
            {label && <label style={{ color: "white", fontSize: fontSize, fontWeight: fontWeight }}>{label}</label>}
            <input 
                type="text"
                placeholder={placeholder ? placeholder : undefined}
                maxLength={7}
                onChange={(e) => updateValue ? updateValue(e.target.value) : null}
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
        </div>
    );
}

export default HexInput;