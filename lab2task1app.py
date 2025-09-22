# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code

from PIL import Image

import random

from src.trivialVacuumEnvironmentClass import TrivialVacuumEnvironment
from src.agents import RandomVacuumAgent

env1={(0, 0): 'Clean', (1, 0): 'Clean'}
env2={(0, 0): 'Clean', (1, 0): 'Dirty'}
env3={(0, 0): 'Dirty', (1, 0): 'Clean'}
env4={(0, 0): 'Dirty', (1, 0): 'Dirty'}



def getImg (agentLoc, envState):
    if agentLoc==(0,0):
        if envState==env1:
            # Load an image
            image = Image.open("imgs/a_clean_Agent__b_clean.jpg") # Replace with your image path
        elif envState==env2:
            image = Image.open("imgs/a_clean_Agent__b_dirty.jpg")
        elif envState==env3:
            image = Image.open("imgs/a_dirty_Agent__b_clean.jpg")
        elif envState==env4:
            image = Image.open("imgs/a_dirty_Agent__b_dirty.jpg")            

    elif agentLoc==(1,0):
        if envState==env1:
            # Load an image
            image = Image.open("imgs/a_clean__b_clean_Agent.jpg") # Replace with your image path
        elif envState==env2:
            image = Image.open("imgs/a_clean__b_dirty_Agent.jpg")
        elif envState==env3:
            image = Image.open("imgs/a_dirty__b_clean_Agent.jpg")
        elif envState==env4:
            image = Image.open("imgs/a_dirty__b_dirty_Agent.jpg")
    
    return image
        
    



def main():
    # Set header title
    st.title('Simple Agents - lab2. Example1')
    
    a1=RandomVacuumAgent()
    st.text(f"{a1} has the initial performance: {a1.performance}")
    
    e1 = TrivialVacuumEnvironment()
    # Check the initial state of the environment
    st.info("State of the Environment: {}.".format(e1.status))
    
    e1.add_thing(a1)
    
    image=getImg(a1.location, e1.status)  
        
    st.image(image, caption="Agent is here", width="content")
    
    if st.button("Run One Agent's Step"):
        if e1.is_agent_alive():
            e1.step()
            st.text("State of the Environment: {}.".format(e1.status))
            st.success("RandomVacuumAgent is located at {}.".format(a1.location))
        else:
            st.error("Agent in location {} and it is dead.".format(a1.location))
        st.info("State of the Environment: {}.".format(e1.status))
        
                
            
    
    
    
    
    
    
if __name__ == '__main__':
    main()
    
    

