"use client";
import GradualBlur from '../components/GradualBlur';

export default function Stats() {
    return (
        <section style={{position: 'relative',height: '100vh', width: '100vw',overflow: 'hidden'}}>
            <div style={{ height: '100%',overflowY: 'auto',padding: '6rem 2rem' }}>
                <div style={{height: '150vh', background: 'linear-gradient(violet, blue)'}}></div>
            </div>

            <GradualBlur
                target="parent"
                position="bottom"
                height="15vh"
                strength={2}
                divCount={5}
                curve="bezier"
                exponential={true}
                opacity={1}
            />
            </section>
    )
}