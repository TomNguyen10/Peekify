import pytest
from unittest.mock import Mock, patch, ANY
import pandas as pd
from sqlalchemy.orm import Session
from ..utils.langchain import get_personalize_message
from ..utils.user_listening_activity import get_last_week_listening_activities
from datetime import datetime, timezone
from ..data.postgresql import SessionLocal
from sqlalchemy import text

# Mock data
mock_listening_data = pd.DataFrame({
    'activity_listened_at': ['2024-02-20 10:00:00', '2024-02-20 11:00:00'],
    'track_name': ['Song 1', 'Song 2'],
    'track_duration': [180000, 240000],
    'track_popularity': [80, 70],
    'album_name': ['Album 1', 'Album 2'],
    'album_release_date': ['2023-01-01', '2023-02-01'],
    'album_total_tracks': [12, 15],
    'album_genres': [['pop'], ['rock']],
    'artist_names': [['Artist 1'], ['Artist 2']],
    'artist_genres': [['pop'], ['rock']],
    'artist_popularity': [85, 75]
})


@pytest.fixture
def mock_db():
    mock = Mock(spec=Session)
    mock.query = Mock()
    mock.query.return_value = mock.query
    mock.filter = Mock(return_value=mock.query)
    mock.all = Mock(return_value=[])
    return mock


@pytest.fixture
def mock_chat_openai():
    with patch('app.utils.langchain.ChatOpenAI') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_agent():
    def mock_create_agent(*args, **kwargs):
        mock_agent_instance = Mock()
        mock_agent_instance.invoke.return_value = {
            'output': 'Test personalized message'
        }
        return mock_agent_instance

    with patch('app.utils.langchain.create_pandas_dataframe_agent', side_effect=mock_create_agent) as mock:
        yield mock


def print_user_header(user_id: str, username: str):
    """Print a formatted header for each user's test section."""
    print(f"\n{'-'*80}")
    print(f"User ID: {user_id}")
    print(f"Username: {username}")
    print(f"{'-'*80}")


def print_message_result(message: str):
    """Print the personalized message in a formatted way."""
    print("\nPersonalized Message:")
    print(f"{'*'*40}")
    print(message)
    print(f"{'*'*40}")


def print_status(success: bool, error: str = None):
    """Print the test status with appropriate formatting."""
    if success:
        print("\nStatus: ✅ Success")
    else:
        print(f"\nStatus: ❌ Error")
        if error:
            print(f"Error details: {error}")
    print(f"{'-'*80}")


def test_get_personalize_message_with_all_real_users():
    """Test personalized message generation for all real users in the database."""
    db = SessionLocal()
    try:
        # Get all users from the database
        result = db.execute(text("SELECT id, username FROM users"))
        users = result.fetchall()

        if not users:
            print("\nNo users found in the database")
            return

        print(f"\n{'='*80}")
        print(f"Found {len(users)} users in the database")
        print(f"{'='*80}")

        # Test with each user's data
        for user in users:
            print_user_header(user.id, user.username or "N/A")

            try:
                # Get the personalized message
                result = get_personalize_message(
                    db, user.id, user.username or "User")

                # Print the result
                print_message_result(result)
                print_status(True)

            except Exception as e:
                print_status(False, str(e))

    finally:
        db.close()


def test_get_personalize_message_success(mock_db, mock_agent, mock_chat_openai):
    """Test successful personalized message generation."""
    with patch('app.utils.user_listening_activity.get_last_week_listening_activities') as mock_get_data:
        # Create a real DataFrame for the test
        df = pd.DataFrame({
            'activity_listened_at': ['2024-02-20 10:00:00', '2024-02-20 11:00:00'],
            'track_name': ['Song 1', 'Song 2'],
            'track_duration': [180000, 240000],
            'track_popularity': [80, 70],
            'album_name': ['Album 1', 'Album 2'],
            'album_release_date': ['2023-01-01', '2023-02-01'],
            'album_total_tracks': [12, 15],
            'album_genres': [['pop'], ['rock']],
            'artist_names': [['Artist 1'], ['Artist 2']],
            'artist_genres': [['pop'], ['rock']],
            'artist_popularity': [85, 75]
        })
        mock_get_data.return_value = df

        result = get_personalize_message(mock_db, 'test_user_id', 'Test User')

        assert isinstance(result, str)
        assert len(result) > 0
        assert result == 'Test personalized message'


def test_get_personalize_message_empty_data(mock_db, mock_agent, mock_chat_openai):
    """Test personalized message generation with empty data."""
    with patch('app.utils.user_listening_activity.get_last_week_listening_activities') as mock_get_data:
        mock_get_data.return_value = pd.DataFrame()

        result = get_personalize_message(mock_db, 'test_user_id', 'Test User')

        assert result == 'No listening data available for the past week.'


def test_get_personalize_message_invalid_data(mock_db, mock_agent, mock_chat_openai):
    """Test personalized message generation with invalid data."""
    with patch('app.utils.user_listening_activity.get_last_week_listening_activities') as mock_get_data:
        mock_get_data.return_value = None

        result = get_personalize_message(mock_db, 'test_user_id', 'Test User')

        assert result == 'Sorry, I couldn\'t analyze your listening data at this time.'


def test_get_personalize_message_agent_error(mock_db, mock_agent, mock_chat_openai):
    """Test personalized message generation when agent encounters an error."""
    with patch('app.utils.user_listening_activity.get_last_week_listening_activities') as mock_get_data:
        mock_get_data.return_value = pd.DataFrame({
            'activity_listened_at': ['2024-02-20 10:00:00'],
            'track_name': ['Song 1'],
            'track_duration': [180000],
            'track_popularity': [80],
            'album_name': ['Album 1'],
            'album_release_date': ['2023-01-01'],
            'album_total_tracks': [12],
            'album_genres': [['pop']],
            'artist_names': [['Artist 1']],
            'artist_genres': [['pop']],
            'artist_popularity': [85]
        })

        mock_agent.invoke.side_effect = Exception("Agent error")

        result = get_personalize_message(mock_db, 'test_user_id', 'Test User')

        assert result == 'Sorry, I couldn\'t analyze your listening data at this time.'
