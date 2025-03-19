# flake8: noqa
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Interaction, Games, Developer, Genre

client = APIClient()


class GamesTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(email='admin@test.com', password='12345')
        self.client.login(username='testu', email='admin@test.com', password='12345')

        self.developer = Developer.objects.create(name='testD')
        self.genre = Genre.objects.create(name='Action')


        self.game = Games.objects.create(
            title='Test game',
            description='Test Description',
            developer=self.developer
        )


        self.game.genre.set([self.genre])

        self.interaction = Interaction.objects.create(user=self.user, game=self.game)

    def test_home_page_get(self):
        """ GET запрос на главную страницу."""

        response = self.client.get(reverse('games:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/home.html')
        self.assertIn('genres', response.context)
        self.assertIn('games', response.context)








class InteractionCreateApiViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create(email='admin@test.com', password='12345')
        self.client.force_authenticate(user=self.user)
        self.developer = Developer.objects.create(name='Sony')
        self.games = Games.objects.create(title='test1', description='just game', developer=self.developer)
        self.genre = Genre.objects.create(name='Action')
        self.games.genre.set([self.genre])

        self.valid_payload = {
            'user_id': self.user.id,
            'item_id': 1,
            'interaction_type': 'like'
        }
        self.invalid_payload = {
            'user_id': self.user.id,
            'item_id': 1
        }


    def test_create_interaction(self):
        """Тестируем создание взаимодействия."""

        url = reverse("games:prefer_add")


        data = {
            'rating': 3,
            'game': self.games.id,
            'user': self.user.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['rating'], 3)
        self.assertEqual(response.data['game'], self.games.id)
        self.assertEqual(response.data['user'], self.user.id)

    def test_create_invalid_interaction(self):
        """Тестируем попытку создания предпочтения с невалидными данными."""

        url = reverse("games:prefer_add")
        data = {
            'invalid_field': 'value',
            'rating': 'abc',
            'game': 'invalid_game_id',
            'user': 'invalid_user_id'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rating', response.data)
        self.assertIn('game', response.data)
        self.assertIn('user', response.data)
        self.assertIn('A valid integer is required.', str(response.data['rating'][0]))
        self.assertIn('Incorrect type. Expected pk value, received str.', str(response.data['game'][0]))
        self.assertIn('Incorrect type. Expected pk value, received str.', str(response.data['user'][0]))


class InteractionRetrieveApiViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        User = get_user_model()


        self.user = User.objects.create(email='admin@test.com', password='12345')
        self.client.force_authenticate(user=self.user)
        self.developer = Developer.objects.create(name='Sony')
        self.games = Games.objects.create(title='test1', description='just game', developer=self.developer)
        self.genre = Genre.objects.create(name='Action')
        self.games.genre.set([self.genre])

        self.valid_payload = {
            'user_id': self.user.id,
            'item_id': 1,
            'interaction_type': 'like'
        }
        self.invalid_payload = {
            'user_id': self.user.id,
            'item_id': 1
        }
        self.interaction = Interaction.objects.create(
            game=self.games,
            user=self.user
        )

    def test_games_retrieve(self):
        """Тестируем успешное получение игры."""
        response = self.client.get(reverse('games:games_int', args=[self.interaction.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Interaction.objects.filter(user=self.user, game=self.games).exists())




class NearestNeighborsViewTest(APITestCase):
     def setUp(self):
         self.client = APIClient()
         User = get_user_model()


         self.user1 = User.objects.create(email='user1@test.com', password='12345')
         self.user2 = User.objects.create(email='user2@test.com', password='12345')

         self.client.force_authenticate(user=self.user1)


         self.developer = Developer.objects.create(name='Sony')


         self.game1 = Games.objects.create(title='test1', description='just game', developer=self.developer)
         self.game2 = Games.objects.create(title='test2', description='another game', developer=self.developer)



         self.genre1 = Genre.objects.create(name='Action')
         self.genre2 = Genre.objects.create(name='Adventure')


         self.game1.genre.set([self.genre1, self.genre2])




         self.interaction1 = Interaction.objects.create(
         rating=4.0,
         game=self.game1,
         user=self.user1
         )
         self.interaction2 = Interaction.objects.create(
         rating=5.0,
         game=self.game2,
         user=self.user1
         )


         self.interaction3 = Interaction.objects.create(
         rating=4.0,
         game=self.game1,
         user=self.user2
         )
         self.interaction4 = Interaction.objects.create(
         rating=3.0,
         game=self.game1,
         user=self.user2
         )




     def test_games_retrieve(self):
         """Тестируем нахождение ближайших соседей """

         url = reverse('games:near_neighbor')
         response = self.client.get(url)

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertGreater(len(response.data), 0)



