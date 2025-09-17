# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code

from PIL import Image

import random

from src.trivialVacuumEnvironmentClass import TrivialVacuumEnvironment
from src.agents import RandomVacuumAgent



def main():
    # Set header title
    st.title('Simple Agents - lab2. Example1')
    
    a1=RandomVacuumAgent()
    st.text(f"{a1} has the initial performance: {a1.performance}")
    
    e1 = TrivialVacuumEnvironment()
    # Check the initial state of the environment
    st.text("State of the Environment: {}.".format(e1.status))
    
    e1.add_thing(a1)
    
    if a1.location==(0,0):
        # Load an image
        image = Image.open("imgs/a_clean_Agent__b_clean.jpg") # Replace with your image path
    elif a1.location==(1,0):
        # Load an image
        image = Image.open("imgs/a_clean__b_dirty_Agent.jpg") # Replace with your image path
    else:
        st.text("RandomVacuumAgent is located in the universe!!!")
        
    st.image(image, caption="Agent is here", width="content")
    
    if st.button("Run One Agent's Step"):
        e1.step()
        st.text("State of the Environment: {}.".format(e1.status))
        st.text("RandomVacuumAgent is located at {}.".format(a1.location))
        
                
            
    
    
    
    
    
    
if __name__ == '__main__':
    main()
    
    

