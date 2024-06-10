import React from "react";
import {Heading, Flex} from "@chakra-ui/react";
 
const Header = () => {
    return (
        <Flex
        as= "nav"
        align ="center"
        justify="space-between"
        wrap ="wrap"
        paddingY= "1rem"
        paddingX= "1rem"
        bg= "pink.200"
        color="white"
        boxShadow="0px 2px 4px rgba(0,0,0,0.2)"
        >
            <Flex align= "center" mr={5}>
                <Heading 
                as="h3" 
                size= "lg"
                fontWeight="bold">
                Face Verification and Liveness Check
                </Heading>
            </Flex>
        </Flex>
    );
};

export default Header;