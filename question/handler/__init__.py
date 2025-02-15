from question.serializers import QuestionAnswerSerializer
from question.models import Question, QuestionAnswer
from app.error import AppError
from match.models import Match
from datetime import datetime, timedelta
from django.utils import timezone
from typing import List
from users.models import User
from django.db.models import Q


class QuestionHandler:
    @staticmethod
    def find_by_id(id):
        return Question.objects.get(id=id)

    @staticmethod
    def get_by_id(id):
        try:
            question = Question.objects.get(id=id)
            return question
        except Question.DoesNotExist:
            raise AppError(code=404, detail="질문이 존재하지 않습니다")

    @staticmethod
    def get_by_match(match: Match):
        return Question.objects.filter(match=match).order_by("-created_at").first()

    @staticmethod
    def get_last_week_emotions(match: Match):
        now = timezone.now()
        last_week = now - timedelta(days=7)
        husband_minds: List[QuestionAnswer] = list(
            QuestionAnswer.objects.filter(
                writer=match.male, created_at__gte=last_week)
        )
        wife_minds: List[QuestionAnswer] = list(
            QuestionAnswer.objects.filter(
                writer=match.female, created_at__gte=last_week
            )
        )
        return {
            "husband_emotions": QuestionAnswerSerializer.Model(
                husband_minds, many=True
            ).data,
            "wife_emotions": QuestionAnswerSerializer.Model(wife_minds, many=True).data,
        }

    @staticmethod
    def update_voice(question: Question, user: User, file_url: str):
        is_male = user.sex == "M"
        if is_male:
            question.male_audio_url = file_url
        else:
            question.female_audio_url = file_url
        question.save()
        return question


class MindHandler:
    @staticmethod
    def find_by_id(id: int):
        question = QuestionAnswer.objects.filter(id=id).first()
        if not question:
            raise AppError(404, "데이터가 존재하지 않습니다")
        return question

    @staticmethod
    def first_by_user(user: User, question: Question) -> QuestionAnswer | None:
        return (
            QuestionAnswer.objects.filter(writer=user, question=question)
            .order_by("-created_at")
            .first()
        )

    @staticmethod
    def find_by_question(question: Question):
        husband = QuestionAnswer.objects.filter(
            question__match__male=question.match.male
        ).first()
        wife = QuestionAnswer.objects.filter(
            question__match__female=question.match.female
        ).first()
        return {"husband": husband, "wife": wife}
