import React from "react";
import banner from "../assets/s3.png";
import s12 from "../assets/s12.png";
import { Button } from "flowbite-react";
import Marquee from "react-fast-marquee";
import s20 from "../assets/s20.png";
import s from "../assets/s.png";
import ContactForm from "../utility/ContactForm";

const ContactUs = () => {
  const CurrentYear = new Date().getFullYear();
  return (
    <div className="relative bg-customblue text-white ">
      <img src={s20} className="absolute w-full h-full mix-blend-overlay  " />
      <div className="flex flex-col lg:flex-row  justify-between items-center lg:py-20">
        <img src={s12} className=" xl:h-[400px] h-40 mix-blend-screen" />
        <div className="flex flex-col gap-5 w-full p-4 lg:p-10  ">
          <p className="font-extrabold lg:text-5xl text-2xl text-center ">Contact Us.</p>
          <ContactForm />
        </div>
        <img src={s} className=" xl:h-[400px] h-40 object-contain  mix-blend-screen " />
      </div>
      <div className="flex flex-col items-center justify-center p-4">
        <p className="lg:text-xl font-semibold">
          {" "}
          Crated with 🤍 by Free Code.© {CurrentYear}
        </p>
      </div>
    </div>
  );
};

export default ContactUs;
