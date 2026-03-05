"""
Data models for VibeLenz
Simplified for Pythonista (no Pydantic)
"""
from datetime import datetime
from typing import Literal, Optional
from enum import Enum

class SenderRole(Enum):
    USER = "USER"
    PARTNER = "PARTNER"

class SafetyFlagType(Enum):
    MONEY_REQUEST = "MONEY_REQUEST"
    EARLY_PRIVATE_MEETING = "EARLY_PRIVATE_MEETING"
    LOVE_BOMBING = "LOVE_BOMBING"

class RiskCategory(Enum):
    SAFE = "SAFE"
    CAUTION = "CAUTION"
    DANGER = "DANGER"
    ABORT_IMMEDIATELY = "ABORT_IMMEDIATELY"


class MessageEvent:
    """Single message in conversation"""
    def __init__(self, sender_role: str, timestamp: str, text: str):
        self.sender_role = SenderRole.USER if sender_role == "USER" else SenderRole.PARTNER
        self.timestamp = self._parse_timestamp(timestamp)
        self.text = text
        
        # Auto-compute features
        self.char_count = len(text)
        self.word_count = len(text.split())
        self.contains_money_terms = self._detect_money_terms(text)
        self.contains_url = 'http' in text.lower()
    
    def _parse_timestamp(self, ts):
        """Parse ISO timestamp or datetime object"""
        if isinstance(ts, datetime):
            return ts
        if isinstance(ts, str):
            # Simple ISO parse (Pythonista compatible)
            ts = ts.replace('Z', '')
            try:
                return datetime.fromisoformat(ts)
            except:
                return datetime.now()
        return datetime.now()
    
    def _detect_money_terms(self, text):
        """Check for money-related keywords"""
        money_keywords = ['$', 'venmo', 'cashapp', 'paypal', 'zelle', 
                         'money', 'cash', 'send me', 'wire', 'transfer']
        text_lower = text.lower()
        return any(word in text_lower for word in money_keywords)


class SafetyFlag:
    """Detected safety risk"""
    def __init__(self, flag_type: SafetyFlagType, severity: str, 
                 details: dict, evidence: str):
        self.type = flag_type
        self.severity = severity
        self.details = details
        self.evidence = evidence
    
    def to_dict(self):
        return {
            'type': self.type.value,
            'severity': self.severity,
            'details': self.details,
            'evidence': self.evidence
        }


class SafetyAnalysisOutput:
    """Safety analysis results"""
    def __init__(self, risk_score: float, risk_category: RiskCategory,
                 abort_flag: bool, flags: list, confidence: float,
                 actions: list, explanation: dict):
        self.safety_risk_score = risk_score
        self.risk_category = risk_category
        self.abort_immediately_recommended = abort_flag
        self.active_flags = flags
        self.confidence = confidence
        self.recommended_actions = actions
        self.explanation = explanation
        self.ghosting_ethically_justified = abort_flag or risk_score > 0.7
        self.analysis_timestamp = datetime.now()
    
    def to_dict(self):
        return {
            'safety_risk_score': self.safety_risk_score,
            'risk_category': self.risk_category.value,
            'abort_immediately_recommended': self.abort_immediately_recommended,
            'active_flags': [f.to_dict() for f in self.active_flags],
            'confidence': self.confidence,
            'recommended_actions': self.recommended_actions,
            'ghosting_ethically_justified': self.ghosting_ethically_justified,
            'explanation': self.explanation,
            'analysis_timestamp': self.analysis_timestamp.isoformat()
        }


class EngagementScore:
    """Engagement metrics"""
    def __init__(self, initiation_ratio: float, engagement_score: float,
                 pattern: str, confidence: float):
        self.initiation_ratio = initiation_ratio
        self.engagement_score = engagement_score
        self.pattern = pattern
        self.confidence = confidence
    
    def to_dict(self):
        return {
            'initiation_ratio': self.initiation_ratio,
            'engagement_score': self.engagement_score,
            'pattern': self.pattern,
            'confidence': self.confidence
        }
