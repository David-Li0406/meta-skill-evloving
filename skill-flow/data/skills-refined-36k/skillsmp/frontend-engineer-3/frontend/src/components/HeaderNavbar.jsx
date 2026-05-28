import { Button, Navbar } from "flowbite-react";
import FreeCodelogo from "../assets/FreeCodelogo.png";
const HeaderNavbar = () => {
  return (
    <div className=" px-5 py-1 lg:px-20 ">
      <Navbar>
        <Navbar.Brand href="https://flowbite-react.com">
          <img src={FreeCodelogo} className="h-10 object-fit" />
        </Navbar.Brand>
        <div className="flex md:order-2">
          <Button className="bg-customblue hover:bg-blue-900 hidden lg:inline">Get started</Button>
          <Navbar.Toggle />
        </div>
        <Navbar.Collapse>
          <Navbar.Link href="#" active className="text-xl font-bold">
            Home
          </Navbar.Link>
          <Navbar.Link href="#" className="text-xl font-bold">
            About
          </Navbar.Link>
          <Navbar.Link href="#" className="text-xl font-bold">
            Services
          </Navbar.Link>
          <Navbar.Link href="#" className="text-xl font-bold">
            Contact
          </Navbar.Link>
        </Navbar.Collapse>
      </Navbar>
    </div>
  );
};

export default HeaderNavbar;
