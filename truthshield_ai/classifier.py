class TopicClassifier:
    def __init__(self):
        self.topics = {
            "health": ["vaccine", "doctor", "medicine", "virus", "disease", "covid", "cancer", "health", "diet", "water", "exercise"],
            "farming": ["farm", "crop", "soil", "pesticide", "irrigation", "fertilizer", "seed", "agriculture", "organic", "plant"],
            "environment": ["climate", "pollution", "energy", "warming", "recycle", "waste", "carbon", "nature", "forest", "ozone"]
        }

    def predict(self, text):
        text = text.lower()
        scores = {topic: 0 for topic in self.topics}
        
        for topic, keywords in self.topics.items():
            for word in keywords:
                if word in text:
                    scores[topic] += 1
        
        # Get topic with max keywords found
        best_topic = max(scores, key=scores.get)
        
        if scores[best_topic] > 0:
            return best_topic
        
        return "general"
