from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from utils.user_listening_activity import get_last_week_listening_activities
from config import OPENAI_API_KEY
from data.postgresql import SessionLocal
import pandas as pd
import json
from sqlalchemy.orm import Session


def get_personalize_message(db: Session, user_spotify_id: str, user_name: str) -> str:
    db = SessionLocal()
    try:
        df = get_last_week_listening_activities(db, user_spotify_id)

        if not isinstance(df, pd.DataFrame):
            raise ValueError(
                "get_last_week_listening_activities did not return a pandas DataFrame")

        if df.empty:
            return "No listening data available for the past week."

        agent = create_pandas_dataframe_agent(
            ChatOpenAI(
                temperature=0.8,
                model="gpt-3.5-turbo-16k",
                api_key=OPENAI_API_KEY
            ),
            df,
            verbose=True,
            agent_type="openai-functions",
            max_iterations=5,
            allow_dangerous_code=True,
            return_intermediate_steps=True,
            handle_parsing_errors=False
        )

        prompt = f"""
        As a data scientist and therapist, analyze your customer {user_name}'s Spotify listening data from the past week. Write a diary-style letter to your customer with the following structure: Top 3 most interesting insights or metrics, and top 3 emotions inferred from the data, as bullet points. Each bullet not gonna exceeds 10 words. End the letter with a wish or a note for the upcoming week infer from the data. The entire letter should not exceed 200 words.
        """

        formatted_prompt = json.dumps(prompt)
        response = agent.invoke(formatted_prompt)
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
