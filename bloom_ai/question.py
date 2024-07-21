from users.models import User
from question.models import Question
from match.models import Match
from typing import List
from .gpt import BloomAI


class BloomQuestionCreator:
    question_creator_template = """
I'm developing a service that provides psychological counseling for infertile couples.
I'm thinking of questions to ask in the service to counsel infertile couples.

I need you to create one question to be delivered to infertile couples in Korean like the example below.
Note: Please answer only in the format below.

Example) Question: (Question content)

I'll provide the following data about husband and wife And below are examples of questions.
Example)
 - Timing of infertility diagnosis:
 - Situation of infertility treatment:
 - Main causes of infertility:
 - Financial burden of infertility treatment:
 - Support from family or others: - Understanding of infertility in the workplace:
 - Communication about fertility issues between the couple:

**Husband**.
 - Timing of infertility diagnosis: {male_age_of_diagnosis}
 - Situation of infertility treatment: {male_fertility_treatment_situation}
 - Main causes of infertility: {male_main_cause_of_infertility}
 - Financial burden of infertility treatment: {male_economic_burden_of_treatment}
 - Support from family or others: {male_support_from_family}
 - Understanding of infertility in the workplace: {male_understanding_in_workplace}
 - Communication about fertility issues between the couple: {male_communication_between_couple}

**wife**.
 - Timing of infertility diagnosis: {female_age_of_diagnosis}
 - Situation of infertility treatment: {female_fertility_treatment_situation}
 - Main causes of infertility: {female_main_cause_of_infertility}
 - Financial burden of infertility treatment: {female_economic_burden_of_treatment}
 - Support from family or others: {female_support_from_family}
 - Understanding of infertility in the workplace: {female_understanding_in_workplace}
 - Communication about fertility issues between the couple: {female_communication_between_couple}

How did you feel when you were diagnosed with infertility?
What was the most difficult moment during your fertility treatment?
What comforting words did you say to each other after a failed treatment?
How do you deal with the stress of infertility?
How was communication between the couple during the treatment process?
What were the biggest conflicts you had with your fertility issues?
What efforts are you making to understand each other's feelings?
How have you talked to people around you about infertility?
How do you share the financial burden of treatment?
What have you said or done that has been the most supportive to each other?
How have you met each other's needs during fertility treatment?
Where do you get information about fertility?
Do you do hobbies to reduce the stress of infertility?
How do you respect each other's feelings?
Have you considered other solutions besides fertility treatment?
What stress-relieving activities do you engage in as a couple?
How has the couple's relationship changed over the course of treatment?
Have your social activities changed because of your fertility issues?
How do you express your support for each other?
What made you decide to try again after a failed treatment?
What kind of future do you envision for each other?
What support was most helpful during your fertility treatment?
Have you ever sought fertility counseling and what was that experience like?
Are you involved in any community activities to address fertility issues?
What are you doing to support each other's health?
What are your mutual commitments to the success of your treatment?
What are your expectations for each other during fertility treatment?
Do you feel like you have enough fertility information and support?
When have you been most grateful for each other?
Do you have any special ways as a couple to cope with infertility?

And please don't think about the questions below because they've already been asked.
{exists_questions}
    """

    def __init__(self, wife: User, husband: User):
        self.wife = wife
        self.husband = husband
        self.bloom_ai = BloomAI()

    def create(self, match: Match):
        try:
            questions: List[Question] = Question.objects.filter(match=match)
        except Question.DoesNotExist:
            questions = []

        question_list = list(map(lambda q: q.content, questions))

        husband_infer = self.get_infertility_details(self.husband)
        wife_infer = self.get_infertility_details(self.wife)

        template = self.assemble_template(
            husband_infer, wife_infer, question_list)
        created_question = self.bloom_ai.query(message=template).replace(
            "Question: ", ""
        )
        print(template)
        return Question.create(content=created_question, match=match)

    def get_infertility_details(self, user: User):
        infer = user.infertility
        return {
            "age_of_diagnosis": infer.period,
            "fertility_treatment_situation": infer.care_status,
            "main_cause_of_infertility": infer.cause,
            "economic_burden_of_treatment": infer.cost,
            "support_from_family": "",
            "understanding_in_workplace": infer.workplace_comprehension,
            "communication_between_couple": infer.communication,
        }

    def assemble_template(self, husband_infer, wife_infer, question_list):
        return self.question_creator_template.format(
            male_age_of_diagnosis=husband_infer["age_of_diagnosis"],
            male_fertility_treatment_situation=husband_infer[
                "fertility_treatment_situation"
            ],
            male_main_cause_of_infertility=husband_infer["main_cause_of_infertility"],
            male_economic_burden_of_treatment=husband_infer[
                "economic_burden_of_treatment"
            ],
            male_support_from_family=husband_infer["support_from_family"],
            male_understanding_in_workplace=husband_infer["understanding_in_workplace"],
            male_communication_between_couple=husband_infer[
                "communication_between_couple"
            ],
            female_age_of_diagnosis=wife_infer["age_of_diagnosis"],
            female_fertility_treatment_situation=wife_infer[
                "fertility_treatment_situation"
            ],
            female_main_cause_of_infertility=wife_infer["main_cause_of_infertility"],
            female_economic_burden_of_treatment=wife_infer[
                "economic_burden_of_treatment"
            ],
            female_support_from_family=wife_infer["support_from_family"],
            female_understanding_in_workplace=wife_infer["understanding_in_workplace"],
            female_communication_between_couple=wife_infer[
                "communication_between_couple"
            ],
            exists_questions=question_list,
        )
