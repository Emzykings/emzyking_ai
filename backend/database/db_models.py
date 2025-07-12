from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from backend.database.db_connection import Base


# Represents an AI chat session for tracking messages and memory
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One-to-many relationship with chat messages
    messages = relationship("ChatMessage", back_populates="chat_session", cascade="all, delete-orphan")

    # One-to-many relationship with memory items
    memories = relationship("MemoryStore", back_populates="chat_session", cascade="all, delete-orphan")


# Represents a single user or assistant message in a session
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, ForeignKey("chat_sessions.chat_id"))  # Session reference
    role = Column(String)  # 'user' or 'assistant'
    content = Column(Text)  # Raw message content
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Link back to session
    chat_session = relationship("ChatSession", back_populates="messages")

    # One-to-one: optional reasoning behind AI reply
    thought = relationship("AgentThought", back_populates="message", uselist=False, cascade="all, delete-orphan")

    # One-to-many: tools used within this message (if any)
    tools_used = relationship("ToolUsage", back_populates="message", cascade="all, delete-orphan")

    # One-to-many: feedback entries on this message
    feedback_entries = relationship("AgentFeedback", back_populates="message", cascade="all, delete-orphan")


# Represents internal reasoning or chain-of-thought for a specific message
class AgentThought(Base):
    __tablename__ = "agent_thoughts"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("chat_messages.id"))  # Parent message
    reasoning = Column(Text)  # Chain-of-thought text
    tool_invoked = Column(String, nullable=True)  # Name of tool used (optional)
    observation = Column(Text, nullable=True)  # Observation/result from tool use
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Link to originating message
    message = relationship("ChatMessage", back_populates="thought")


# Represents a tool/API call used by the assistant
class ToolUsage(Base):
    __tablename__ = "tool_usages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("chat_messages.id"))  # Linked to specific message
    tool_name = Column(String)  # Name of tool or function
    input_params = Column(Text)  # Serialized inputs passed to the tool
    output_result = Column(Text)  # Result or output from the tool
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Reference to the triggering message
    message = relationship("ChatMessage", back_populates="tools_used")


# Represents long-term or contextual memory tied to a chat session
class MemoryStore(Base):
    __tablename__ = "memory_store"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, ForeignKey("chat_sessions.chat_id"))  # Linked session
    memory_type = Column(String)  # Category (e.g. 'fact', 'preference', 'task')
    content = Column(Text)  # Stored memory content
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Link to session
    chat_session = relationship("ChatSession", back_populates="memories")


# Capture user feedback on assistant's performance
class AgentFeedback(Base):
    __tablename__ = "agent_feedback"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("chat_messages.id"), nullable=False)  # The assistant's message
    agent_name = Column(String, nullable=False)  # Name of agent who generated the reply
    rating = Column(Integer, nullable=False)  # e.g., 1–5 scale
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to the message
    message = relationship("ChatMessage", back_populates="feedback_entries")
