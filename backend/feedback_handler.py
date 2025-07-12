"""
This module manages feedback from users about agent responses.
Feedback includes approval/disapproval and optional comments, which
can later be used to refine agent routing or retrain models.

Author: Emzyking AI
"""

from sqlalchemy.orm import Session
from backend.database import db_models
from backend.schemas import FeedbackRequest


def save_feedback_from_request(request: FeedbackRequest, db: Session) -> bool:
    """
    Saves user feedback from a validated Pydantic request object.

    Args:
        request (FeedbackRequest): Feedback input including message ID, approval, and comment.
        db (Session): SQLAlchemy database session.

    Returns:
        bool: True if feedback is saved successfully, False otherwise.
    """
    return save_feedback(
        message_id=request.message_id,
        is_approved=request.is_approved,
        user_comment=request.comment,
        db=db
    )


def save_feedback(
    message_id: int,
    is_approved: bool,
    user_comment: str,
    db: Session
) -> bool:
    """
    Saves user feedback for a specific assistant message.

    Args:
        message_id (int): ID of the ChatMessage being reviewed.
        is_approved (bool): Whether the user approved the response.
        user_comment (str): Optional feedback or clarification from the user.
        db (Session): SQLAlchemy session.

    Returns:
        bool: True if feedback saved successfully, False otherwise.
    """
    try:
        feedback = db_models.AgentFeedback(
            message_id=message_id,
            is_approved=is_approved,
            comment=user_comment or ""
        )
        db.add(feedback)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[Feedback Error] {e}")
        return False


def get_feedback_summary(message_id: int, db: Session) -> dict:
    """
    Retrieves all feedback entries for a given message.

    Args:
        message_id (int): The ChatMessage ID for which feedback is needed.
        db (Session): SQLAlchemy session.

    Returns:
        dict: Feedback breakdown including counts and comments.
    """
    feedback_entries = db.query(db_models.AgentFeedback).filter(
        db_models.AgentFeedback.message_id == message_id
    ).all()

    approved = [f for f in feedback_entries if f.is_approved]
    disapproved = [f for f in feedback_entries if not f.is_approved]

    return {
        "message_id": message_id,
        "approved_count": len(approved),
        "disapproved_count": len(disapproved),
        "comments": [f.comment for f in feedback_entries if f.comment]
    }
