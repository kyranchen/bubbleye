# bubbleye
A mock web application for managing advertising creatives

# Tech Spec
https://docs.google.com/document/d/1OmtiCgVTu-QbU934h11vM_JOqjDV_icAxYWy2MWF-EE/edit?usp=sharing

https://developer.moloco.cloud/

# How to Run it

1. **Install Dependencies**  
    Download all required packages (including Streamlit and Flask) by running:
    ```
    pip install -r requirements.txt
    ```

2. **Start the Backend Simulator**  
    Open a terminal and run:
    ```
    python3 moloco_simulator.py
    ```

3. **Start the Streamlit App**  
    Open another terminal and run:
    ```
    streamlit run main.py
    ```


# User Flow

1. **Upload Creatives**  
    User uploads individual creative assets to the platform.

2. **Create Creative Groups**  
    User organizes uploaded creatives into creative groups.

3. **Attach Creative Groups to Testing Campaign**  
    User assigns creative groups to a testing campaign for evaluation.

4. **Pause Campaign to View Results**  
    User pauses the testing campaign to analyze performance metrics of each creative group.

5. **Add Well-Performed Groups to Champion Queue**  
    User adds high-performing creative groups to a champion queue for future use.

6. **Replace Underperforming Group in Regular Campaign**  
    If desired, user replaces the lowest-performing creative group in a regular campaign with a group from the champion queue.
