# ai_agent/classifiers/query_classifier.py
import re

class IntelligentQueryClassifier:
    def __init__(self):
        # Blockchain-specific indicators
        self.blockchain_indicators = {
            'entities': ['vehicle', 'car', 'land', 'property', 'deed', 'title', 'registration'],
            'actions': ['owns', 'owned', 'registered', 'transferred', 'owner', 'ownership'],
            'identifiers': ['VH', 'LD', 'vehicle id', 'land id', 'registration number'],
            'blockchain_terms': ['blockchain', 'smart contract', 'registry', 'record']
        }
        
        # General query indicators
        self.general_indicators = {
            'market_terms': ['price', 'cost', 'value', 'market', 'buy', 'sell'],
            'information_seeking': ['what is', 'how to', 'define', 'explain', 'guide'],
            'comparative': ['vs', 'versus', 'compare', 'difference', 'better'],
            'general_topics': ['news', 'review', 'specification', 'feature']
        }
    
    def classify_query(self, query):
        query_lower = query.lower()
        blockchain_score = 0
        general_score = 0
        
        # Calculate blockchain relevance score
        for category, terms in self.blockchain_indicators.items():
            for term in terms:
                if term in query_lower:
                    blockchain_score += 1
        
        # Calculate general query score
        for category, terms in self.general_indicators.items():
            for term in terms:
                if term in query_lower:
                    general_score += 1
        
        # Advanced pattern matching
        blockchain_score += self._check_blockchain_patterns(query_lower)
        
        return 'blockchain' if blockchain_score > general_score else 'general'
    
    def _check_blockchain_patterns(self, query):
        patterns = [
            r'who owns?\s+(?:vehicle|car|land)',  # "who owns vehicle"
            r'(?:vehicle|car)\s+[A-Z]{2}[\d\-]+',  # vehicle IDs
            r'transfer.*(?:ownership|title)',      # transfer operations
            r'register.*(?:vehicle|land)',         # registration queries
        ]
        
        score = 0
        for pattern in patterns:
            if re.search(pattern, query):
                score += 2  # Higher weight for specific patterns
        return score
    
    def classify_with_confidence(self, query):
        """Enhanced classification with confidence scoring"""
        classification = self.classify_query(query)
        confidence = self._calculate_confidence(query, classification)
        
        return {
            'classification': classification,
            'confidence': confidence,
            'reasoning': self._get_classification_reasoning(query)
        }
    
    def _calculate_confidence(self, query, classification):
        """Calculate confidence score between 0.0 and 1.0"""
        query_lower = query.lower()
        blockchain_matches = 0
        general_matches = 0
        
        # Count matches for each category
        for category, terms in self.blockchain_indicators.items():
            for term in terms:
                if term in query_lower:
                    blockchain_matches += 1
        
        for category, terms in self.general_indicators.items():
            for term in terms:
                if term in query_lower:
                    general_matches += 1
        
        total_matches = blockchain_matches + general_matches
        if total_matches == 0:
            return 0.5  # Neutral confidence when no clear indicators
        
        if classification == 'blockchain':
            confidence = blockchain_matches / total_matches
        else:
            confidence = general_matches / total_matches
        
        return min(0.95, max(0.55, confidence))  # Clamp between 0.55 and 0.95
    
    def _get_classification_reasoning(self, query):
        """Provide reasoning for the classification decision"""
        query_lower = query.lower()
        reasons = []
        
        # Check for blockchain indicators
        for category, terms in self.blockchain_indicators.items():
            found_terms = [term for term in terms if term in query_lower]
            if found_terms:
                reasons.append(f"Found {category}: {', '.join(found_terms)}")
        
        # Check for general indicators
        for category, terms in self.general_indicators.items():
            found_terms = [term for term in terms if term in query_lower]
            if found_terms:
                reasons.append(f"Found {category}: {', '.join(found_terms)}")
        
        return reasons if reasons else ["No clear classification indicators found"]
