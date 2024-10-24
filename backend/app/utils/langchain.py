from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from utils.user_listening_activity import get_last_week_listening_activities
from config import OPENAI_API_KEY
from data.postgresql import SessionLocal
import pandas as pd
from sqlalchemy.orm import Session


def get_personalize_message(db: Session, user_spotify_id: str):
    db = SessionLocal()
    try:
        df = get_last_week_listening_activities(db, user_spotify_id)

        if not isinstance(df, pd.DataFrame):
            raise ValueError(
                "get_last_week_listening_activities did not return a pandas DataFrame")

        if df.empty:
            return "No listening data available for the past week."

        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo-16k",
                       api_key=OPENAI_API_KEY),
            df,
            verbose=True,
            agent_type="openai-functions",
            max_iterations=5,
            allow_dangerous_code=True,
            return_intermediate_steps=True
        )

        prompt = """
        As a data scientist and therapist, analyze your customer's Spotify listening data from the past week. Write a diary-style letter to your customer with the following structure:

        1. Opening: Briefly summarize the week's listening activities.
        2. Body: Provide a detailed analysis of the data, including:
           - Key metrics 
           - Notable patterns 
           - Interesting insights 
        Please be specific and provide insights that are relevant.
        3. Conclusion: Summarize the week, focusing on emotions or moods inferred from the data.
        4. Recommendations: Write a wish or a note for the upcoming week.
        
        Be creative, thorough, and empathetic in your analysis. Use specific examples from the data to support your insights.
        Limit your response to about 500 words.
        """

        response = agent.invoke(prompt)
        if isinstance(response, dict) and 'output' in response:
            return str(response['output'])
        elif isinstance(response, str):
            return response
        else:
            return str(response)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "Sorry, I couldn't analyze your listening data at this time."

    finally:
        db.close()
