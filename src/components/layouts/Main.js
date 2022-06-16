import React from "react";
import { FaBars } from "react-icons/fa";
import {
  Nav,
  NavbarContainer,
  NavLogo,
  MobileIcon,
  NavMenu,
  NavItem,
  NavLinks,
  NavBtn,
  NavBtnBlink,
} from "./NavBar";

import {
  SidebarContainer,
  Icon,
  CloseIcon,
  SideBtnWrap,
  SidebarLink,
  SidebarRoute,
  SidebarWrapper,
  SidebarMenu,
} from "./SideBar";

const Main = () => {
  return (
    <>
      {/* Navbar */}
      <Nav>
        <NavbarContainer>
          <NavLogo to="/">Van Rental</NavLogo>
          <MobileIcon>
            <FaBars />
          </MobileIcon>
          <NavMenu>
            <NavItem>
              <NavLinks to="rent">Rent</NavLinks>
            </NavItem>
            <NavItem>
              <NavLinks to="how">How it works?</NavLinks>
            </NavItem>
            <NavItem>
              <NavLinks to="about">About</NavLinks>
            </NavItem>
            <NavItem>
              <NavLinks to="contact">Contact</NavLinks>
            </NavItem>
          </NavMenu>

          <NavBtn>
            <NavBtnBlink to="/signin">Sign In</NavBtnBlink>
          </NavBtn>
        </NavbarContainer>
      </Nav>

      {/* Sidebar */}
      <SidebarContainer>
        <Icon>
          <CloseIcon />
        </Icon>
        <SidebarWrapper>
          <SidebarMenu>
            <SidebarLink to="rent">Rent</SidebarLink>
            <SidebarLink to="how">How it works?</SidebarLink>
            <SidebarLink to="about">About</SidebarLink>
            <SidebarLink to="contact">Contact</SidebarLink>
          </SidebarMenu>
          <SideBtnWrap>
            <SidebarRoute to="/signin">Sign In</SidebarRoute>
          </SideBtnWrap>
        </SidebarWrapper>
      </SidebarContainer>
    </>
  );
};

export default Main;
