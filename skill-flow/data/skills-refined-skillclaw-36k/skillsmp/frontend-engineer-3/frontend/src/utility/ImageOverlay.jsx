import React from 'react';
import s3 from "../assets/s3.png"
import bg3 from "../assets/bg3.png"
import freecode from "../assets/FreeCodelogo.png"
const ImageOverlay = () => {
  return (
    <div className="relative w-full h-96 bg-blue-500"> {/* Background color */}
      {/* Overlay */}
      <div className="absolute inset-0 bg-black opacity-50"></div> {/* Semi-transparent overlay */}

      {/* First Image */}
      <img 
        src={s3} 
        alt="Image 1" 
        className="absolute top-0  h-full object-cover z-20" 
      />

      {/* Second Image */}
      <img 
        src={bg3}
        alt="Image 2" 
        className="absolute top-0  h-full object-cover z-30" 
      />

      {/* Third Image */}
      <img 
        src={freecode} 
        alt="Image 3" 
        className="absolute top-0  h-full object-cover bg-opacity-55 z-40" 
      />
    </div>
  );
};

export default ImageOverlay;
