import React from "react";
import { Button, Checkbox, Label, TextInput } from "flowbite-react";
// import Link from "next/link";


const ContactForm = () => {
  return (
    <form className="flex flex-col gap-4 bg-white p-4 lg:p-10 rounded-lg">
         <div>
        <div className="mb-2 block font-bold">
          <Label htmlFor="password2" value="Your Name" className="font-bold"/>
        </div>
        <TextInput id="password2" type="name" placeholder="Enter your Name"required shadow />
      </div>
      <div>
        <div className="mb-2 block ">
          <Label htmlFor="email2" value="Your email" className="font-bold" />
        </div>
        <TextInput
          id="email2"
          type="email"
          placeholder="FreeCode@gmail.com"
          required
          shadow
        />
      </div>
     
      <div>
        <div className="mb-2 block">
          <Label  value="Mobile Number" />
        </div>
        <TextInput type="tel" id="mobile" name="mobile" placeholder="Enter your mobile number" pattern="[0-9]{10}" maxlength="10" required/>
      </div>
      <div className="flex items-center gap-2">
        {/* <Checkbox id="agree" /> */}
        <Label htmlFor="agree" className="flex text-xs lg:text-md">
          I agree with the&nbsp;
          <a
            href="#"
            className="text-cyan-600 hover:underline text-xs lg:text-md dark:text-cyan-500"
          >
            terms and conditions
          </a>
        </Label>
      </div>
      <Button type="submit" color="purple" className="lg:mx-40 text-xl">Contact Now</Button>
    </form>
  );
};

export default ContactForm;
