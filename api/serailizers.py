from rest_framework import serializers
from django.contrib.auth.models import User
from problems.models import ArchiveProblem
from attempts.models import Attempt

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "city", "town", "edu", "image", "bio", "telegramlink", "instagramlink", "isTeacher", "isExpert", "rating", "coins")

class ArchiveProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveProblem
        fields = ("id", "username", "name", "problem", "timelimit", "memorylimit", "difficulty", "category", "allowedlangs", "comment", "infoin", "infoout", "simpletests", "tests", "solution")
    
class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = ("author", "problem", "date", "status", "time", "memory", "code", "language", "lengthcode", "cases", "output")