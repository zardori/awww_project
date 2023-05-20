from django.urls import reverse

import compilation_8bit.views as views

#from django.urls import reverse

from django.test import TestCase
from django.contrib.auth.models import User

from compilation_8bit.models import File, Directory

class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        test_user = User.objects.create_user(username='testuser1', password='aasdfafd1&1b')
        test_user.save()

        dir_1 = Directory.objects.create(name="dir_1", owner=test_user)

        dir_1.save()

        file_1 = File.objects.create(name="file_1", content="file_1_content", parent=dir_1,
                                     owner=test_user)

        file_2 = File.objects.create(name="file_2", content="file_2_content", parent=dir_1,
                                     owner=test_user)

        file_1.save()
        file_2.save()

        cls.file_1 = file_1
        cls.file_2 = file_2

    def setUp(self):
        pass


    def test_with_no_files_selected(self):

        self.client.login(username='testuser1', password='aasdfafd1&1b')

        response = self.client.get(reverse("compilation_8bit:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "compilation_8bit/index.html")
        self.assertTrue("content" not in response.context)


    # def test_with_good_file_selected(self):
    #     self.client.login(username='testuser1', password='aasdfafd1&1b')
    #     session = self.client.session
    #
    #     session.update({
    #         "selected_file_id": self.file_1.id
    #     })
    #     session.save()
    #
    #     print(session["selected_file_id"])
    #
    #     # print(self.client.session["selected_file_id"])
    #
    #     response = self.client.get(reverse("compilation_8bit:index"))
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "compilation_8bit/index.html")
    #     self.assertEqual(response.context.get("content"), self.file_1.content)
