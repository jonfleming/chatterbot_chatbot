from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from spacy.matcher import Matcher
from spacy.util import filter_spans
import spacy

nlp = spacy.load("en_core_web_md")


class FactLogicAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        doc = nlp(statement.text)

        # return True if sentence has a subject, predicate, object - noun, verb, noun
        self.nouns = [chunk.text for chunk in doc.noun_chunks]

        verb_pattern = [{'POS': 'VERB', 'OP': '?'},
                        {'POS': 'ADV', 'OP': '*'},
                        {'POS': 'AUX', 'OP': '*'},
                        {'POS': 'VERB', 'OP': '+'}]

        matcher = Matcher(nlp.vocab)
        matcher.add("Verbs", None, verb_pattern)
        matches = matcher(doc)
        self.verbs = [doc[start:end] for _, start, end in matches]

        if len(self.nouns) > 1 and len(self.verbs) > 0:
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        selected_statement = Statement(
            f'{self.nouns[0]} {self.verbs[0]} {self.nouns[1]}')
        selected_statement.confidence = 1.0
        return selected_statement

    def get_default_response(self, input_statement):
        return 'I did not understand that'

    @property
    def class_name(self):
        return str(self.__class__.__name__)
