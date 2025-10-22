import unittest
from app.epistemology_engine import EpistemologyEngine
from app.models import EpistemologyType


class TestEpistemologyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EpistemologyEngine(min_confidence=0.2)

    def test_empirical_quantitative_detection(self):
        text = "The p<0.05 value indicates statistical significance in our measurements."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.EMPIRICAL_QUANTITATIVE for tag in tags))

    def test_oral_intergenerational_detection(self):
        text = "Our elders say that this tradition has been passed down for generations."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.ORAL_INTERGENERATIONAL for tag in tags))

    def test_ritual_ceremonial_detection(self):
        text = "According to ritual practices, this ceremony is essential for spiritual growth."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.RITUAL_CEREMONIAL for tag in tags))

    def test_experiential_personal_detection(self):
        text = "In my experience, I have observed that this approach works well."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.EXPERIENTIAL_PERSONAL for tag in tags))

    def test_technological_instrumental_detection(self):
        text = "The GPS sensor detected unusual activity in this region."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.TECHNOLOGICAL_INSTRUMENTAL for tag in tags))

    def test_ecological_relational_detection(self):
        text = "The ecosystem is interconnected in ways we are just beginning to understand."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.ECOLOGICAL_RELATIONAL for tag in tags))

    def test_historical_documentary_detection(self):
        text = "Historical records show that this event occurred in the 18th century."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.HISTORICAL_DOCUMENTARY for tag in tags))

    def test_philosophical_deductive_detection(self):
        text = "By necessity, if all humans are mortal and Socrates is human, then Socrates is mortal."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.PHILOSOPHICAL_DEDUCTIVE for tag in tags))

    def test_intuitive_inspirational_detection(self):
        text = "I felt a strong intuition that this was the right path to take."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.INTUITIVE_INSPIRATIONAL for tag in tags))

    def test_theological_doctrinal_detection(self):
        text = "Scripture says that we should treat others with kindness and respect."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.THEOLOGICAL_DOCTRINAL for tag in tags))

    def test_artistic_expressive_detection(self):
        text = "Life is like a dance, with its rhythms and movements guiding us."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.ARTISTIC_EXPRESSIVE for tag in tags))

    def test_legal_precedential_detection(self):
        text = "According to law, this regulation must be followed by all citizens."
        tags = self.engine.detect_epistemologies(text)
        self.assertTrue(any(tag.type == EpistemologyType.LEGAL_PRECEDENTIAL for tag in tags))

    def test_fallback_to_experiential_personal(self):
        text = "This is a generic text with no specific epistemological markers."
        tags = self.engine.detect_epistemologies(text)
        # Should have at least one tag (fallback)
        self.assertTrue(len(tags) > 0)
        # First tag should be Experiential-Personal (fallback)
        self.assertEqual(tags[0].type, EpistemologyType.EXPERIENTIAL_PERSONAL)

    def test_confidence_scoring(self):
        text = "The p<0.05 value indicates statistical significance."
        tags = self.engine.detect_epistemologies(text)
        empirical_tag = next((tag for tag in tags if tag.type == EpistemologyType.EMPIRICAL_QUANTITATIVE), None)
        self.assertIsNotNone(empirical_tag)
        # Should have a confidence score greater than the minimum
        self.assertGreater(empirical_tag.confidence, 0.2)

    def test_empty_text(self):
        text = ""
        tags = self.engine.detect_epistemologies(text)
        self.assertEqual(tags, [])

    def test_sorted_tags_by_confidence(self):
        text = "I felt this was a statistical measurement. The p<0.05 value was detected by our sensors."
        tags = self.engine.detect_epistemologies(text)
        # Verify tags are sorted by confidence in descending order
        confidences = [tag.confidence for tag in tags]
        self.assertEqual(confidences, sorted(confidences, reverse=True))


if __name__ == '__main__':
    unittest.main()
