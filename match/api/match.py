from rest_framework.views import APIView, Response, Request
from match.serializers import MatchSerializers
from app.error import AppError
from users.models import User
from match.handler import InviteCodeHandler, MatchHandler
from match.models import Match
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from question.provider import QuestionProvider
from question.models import Question
from question.handler import QuestionHandler


class MatchAPI(APIView):
    @swagger_auto_schema(
        operation_summary="매치 찾기 API", responses={"200": MatchSerializers.Integrated()}
    )
    def get(self, req: Request):
        user = req.user
        match = MatchHandler.find_by_user(user)

        if not match:
            return Response(data=None, status=200)

        question = QuestionHandler.get_by_match(match)
        data = get_integrated_match(match, question)

        return Response(data=data, status=200)

    @swagger_auto_schema(
        operation_summary="매치 체결 API",
        manual_parameters=[
            openapi.Parameter(
                "code",
                openapi.IN_QUERY,
                description="매칭 코드",
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def post(self, req: Request):
        query: str = req.GET.get("code")
        if not query:
            raise AppError(400, "초대 코드가 존재하지 않습니다")
        invite_code = InviteCodeHandler.find_by_code(code=query)
        creator: User = invite_code.creator

        validate_create_match(creator, req.user)
        match: Match = MatchHandler.create(creator, req.user)
        first_question = QuestionProvider(match=match).create_question()
        data = get_integrated_match(match, first_question)
        invite_code.delete()

        return Response(data=data, status=201)


def get_integrated_match(match: Match, question: Question):
    return MatchSerializers.Integrated(
        instance=match,
        match_id=match.id,
        husband_instance=match.male,
        wife_instance=match.female,
        question_instance=question,
    ).data


def validate_create_match(u1: User, u2: User):
    if u1.id == u2.id:
        raise AppError(400, "초대자와 요청자가 같습니다")

    if MatchHandler.exists(u1, u2):
        raise AppError(409, "이미 매칭된 사용자입니다")
