from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from utils.user_listening_activity import get_last_week_listening_activities
from config import OPENAI_API_KEY
from data.postgresql import SessionLocal
import pandas as pd
import json
from sqlalchemy.orm import Session


def get_personalize_message(db: Session, user_spotify_id: str, user_name: str) -> str:
    try:
        df = get_last_week_listening_activities(db, user_spotify_id)

        if not isinstance(df, pd.DataFrame):
            raise ValueError(
                "get_last_week_listening_activities did not return a pandas DataFrame")

        if df.empty:
            return "No listening data available for the past week."

        # Convert DataFrame to a format that can be used by the agent
        df = df.copy()
        df['activity_listened_at'] = df['activity_listened_at'].astype(str)

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
            handle_parsing_errors=True  # Enable parsing error handling
        )

        prompt = f"""
        As a data scientist and therapist, analyze your customer {user_name}'s Spotify listening data from the past week. Write a diary-style letter to your customer with the following structure: Top 3 most interesting insights or metrics, and top 3 emotions inferred from the data, as bullet points. Each bullet not gonna exceeds 10 words. End the letter with a wish or a note for the upcoming week infer from the data. The entire letter should not exceed 200 words.
        """

        # Don't JSON encode the prompt, send it directly
        response = agent.invoke(prompt)

        # Handle different response formats
        if isinstance(response, dict):
            if 'output' in response:
                return str(response['output'])
            elif 'intermediate_steps' in response and response['intermediate_steps']:
                # Get the last step's output if available
                last_step = response['intermediate_steps'][-1]
                if isinstance(last_step, tuple) and len(last_step) > 1:
                    return str(last_step[1])
        elif isinstance(response, str):
            return response
        elif isinstance(response, (list, tuple)) and response:
            # If response is a list/tuple, get the last element
            return str(response[-1])

        # If we get here, try to convert the entire response to string
        return str(response)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Try to extract any useful information from the error
        error_msg = str(e)
        if "Could not parse tool input" in error_msg:
            # If there's a parsing error, try to extract the message from the error
            try:
                # Look for the message in the error string
                start_idx = error_msg.find("Dear")
                if start_idx != -1:
                    # Find the end of the message (usually marked by a closing quote)
                    end_idx = error_msg.find("'", start_idx)
                    if end_idx != -1:
                        message = error_msg[start_idx:end_idx]
                        # Clean up the message
                        message = message.replace(
                            "\\n", "\n").replace("\\", "")
                        return message
            except:
                pass
        return "Sorry, I couldn't analyze your listening data at this time."
