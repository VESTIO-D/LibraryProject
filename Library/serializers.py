from rest_framework import serializers
from LibraryAdmin.models import LibraryBooksDB, LibraryMembersDB
from LibraryAdmin.models import ReviewDB


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBooksDB
        fields = "__all__"
        read_only__fields = ["id"]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ReviewDB
        fields = "__all__"
