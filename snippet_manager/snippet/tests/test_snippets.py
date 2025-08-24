from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from snippet.models import Snippet

User = get_user_model()

# class SnippetTests(APITestCase):
#     def test_create_and_favorite_snippet(self):
#         user = User.objects.create_user(username="u1", password="pass12345")
#         client = APIClient()
#         tokens = client.post(
#             reverse("auth-login"),
#             {"username": "u1", "password": "pass12345"}
#         ).json()

#         client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

#         s = client.post("/api/snippets/", {
#             "title": "Hello",
#             "content": "print(1)",
#             "language": "python"
#         })

#         self.assertEqual(s.status_code, status.HTTP_201_CREATED)

#         sid = s.json()["id"]
#         fav = client.post(f"/api/snippets/{sid}/favorite/")

#         self.assertEqual(fav.status_code, status.HTTP_201_CREATED)

# class SnippetSearchTests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="u1", password="pass12345")
#         self.client = APIClient()
#         tokens = self.client.post(
#             reverse("auth-login"),
#             {"username": "u1", "password": "pass12345"}
#         ).json()
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

#     def test_create_and_favorite_snippet(self):
#         # ... your existing test ...
#         pass

#     def test_search_snippets(self):
#         # Create a few snippets
#         self.client.post("/api/snippets/", {"title": "Python Snippet", "content": "print('hi')", "language": "python"})
#         self.client.post("/api/snippets/", {"title": "JS Snippet", "content": "console.log(1)", "language": "javascript"})

#         # Search for python
#         res = self.client.get("/api/snippets/search/?q=python")
        
#         print(res.json())

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(res.json()), 1)
#         self.assertEqual(res.json()[0]["language"], "python")

class SnippetSearchPaginationTests(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        # Create snippets
        Snippet.objects.create(
            user=self.user,
            title="Python Snippet",
            content="print('hello')",
            language="python"
        )
        Snippet.objects.create(
            user=self.user,
            title="Django Query Example",
            content="Snippet.objects.all()",
            language="python"
        )
        Snippet.objects.create(
            user=self.user,
            title="JavaScript Code",
            content="console.log('hi')",
            language="javascript"
        )

    def test_pagination(self):
        url = reverse("snippet-list") + "?page=1&page_size=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertLessEqual(len(response.data["results"]), 2)

    def test_filter_by_language(self):
        url = reverse("snippet-list") + "?language=python"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for snippet in response.data["results"]:
            self.assertEqual(snippet["language"], "python")

    def test_search_by_keyword(self):
        url = reverse("snippet-list") + "?search=django"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Django" in s["title"] for s in response.data["results"]))

    def test_ordering_by_created_at(self):
        url = reverse("snippet-list") + "?ordering=-created_at"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        dates = [s["created_at"] for s in results]
        self.assertEqual(dates, sorted(dates, reverse=True))

