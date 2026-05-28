import React from "react";
import banner from "../assets/s3.png";
import s10 from "../assets/s10.png";

import Marquee from "react-fast-marquee";
import s5 from "../assets/s5.png";
import AboutUsPoints from "../utility/AboutUsPoints";

const AboutUs = () => {
  const data = [
    {
      title: "Innovative Solutions",
      description:
        "We stay ahead of the curve, leveraging the latest technologies in AI, machine learning, and web/mobile development to provide solutions that aren’t just current but future-ready.",
    },
    {
      title: "Empower for Your Business",
      description:
        "Your business is unique, and so are our solutions. We don’t believe in one-size-fits-all; we craft custom strategies and products designed to meet your specific needs and goals.",
    },
    {
      title: "User-Centered Design",
      description:
        "Our focus is on creating intuitive, seamless user experiences. From sleek design to smooth functionality, we ensure your digital products are easy to use and engaging for your audience.",
    },
    {
      title: "Commitment to Quality",
      description:
        "We don’t compromise on quality. Every project we undertake is executed with precision, ensuring your business gets the best possible outcome, from performance to security.",
    },
  ];
  return (
    <div className="relative bg-customblue text-white ">
      <img src={s5} className="absolute w-full h-full mix-blend-overlay  " />
      <div className="flex flex-col  lg:flex-row justify-between items-center lg:py-20  xl:py-40 lg:gap-10 lg:pr-5 ">
        <img src={s10} className="h-full w-full lg:w-1/2 " />
        <div className="flex flex-col items-center justify-center gap-5 p-4">
          <p className="font-extrabold  lg:text-5xl text-2xl ">Why Choose Us ?</p>
          {/* <img src={banner} className='absolute bg-opacity-0 h-[500px] w-full'/> */}
          {data.map((item, index) => (
            <AboutUsPoints item={item} index={index} />
          ))}
          {/* {/* <Button color="gray">Get Started</Button> */}
        </div>
      </div>
      <div className="flex flex-col items-center justify-center px-40 "></div>
    </div>
  );
};

export default AboutUs;
