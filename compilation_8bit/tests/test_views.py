from django.urls import reverse

import compilation_8bit.views as views

# from django.urls import reverse

from django.test import TestCase
from django.contrib.auth.models import User

from compilation_8bit.models import File, Directory


class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser1', password='aasdfafd1&1b')
        test_user.save()

        # dir_1 = Directory.objects.create(name="dir_1", owner=test_user)
        #
        # dir_1.save()
        #
        # file_1 = File.objects.create(name="file_1", content="file_1_content", parent=dir_1,
        #                              owner=test_user)
        #
        # file_2 = File.objects.create(name="file_2", content="file_2_content", parent=dir_1,
        #                              owner=test_user)
        #
        # file_1.save()
        # file_2.save()
        #
        # cls.file_1 = file_1
        # cls.file_2 = file_2

    def setUp(self):
        pass

    def test_basic(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')

        response = self.client.get(reverse("compilation_8bit:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "compilation_8bit/index.html")


class DeleteObjectTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='aasdfafd1&1b')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='bbsdfafd1&1b')
        test_user2.save()

        cls.test_user1 = test_user1
        cls.test_user2 = test_user2

    def setUp(self):
        dir_1_usr1 = Directory.objects.create(name="dir_1", owner=self.test_user1)

        dir_1_usr1.save()

        file_1_usr1 = File.objects.create(name="file_1", content="file_1_content", parent=dir_1_usr1,
                                          owner=self.test_user1)

        file_2_usr1 = File.objects.create(name="file_2", content="file_2_content", parent=dir_1_usr1,
                                          owner=self.test_user1)

        file_1_usr1.save()
        file_2_usr1.save()

        self.file_1_usr1 = file_1_usr1
        self.file_2_usr1 = file_2_usr1
        self.dir_1_usr1 = dir_1_usr1


    def testDelFile(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')

        request = reverse("compilation_8bit:del_file") + "?id=" + str(self.file_1_usr1.id)

        print(request)

        response = self.client.get(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(File.objects.get(pk=self.file_1_usr1.id).is_deleted)

    def testDelDir(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')

        response = self.client.get(reverse("compilation_8bit:del_dir") + "?id=" + str(self.dir_1_usr1.id))

        self.assertEqual(response.status_code, 200)

        # now directory and its both files should be marked as deleted
        self.assertTrue(File.objects.get(pk=self.file_1_usr1.id).is_deleted)
        self.assertTrue(File.objects.get(pk=self.file_2_usr1.id).is_deleted)
        self.assertTrue(Directory.objects.get(pk=self.dir_1_usr1.id).is_deleted)


    def testDelFileOfOtherUser(self):
        self.client.login(username='testuser2', password='bbsdfafd1&1b')
        response = self.client.get(reverse("compilation_8bit:del_file") + "?id=" + str(self.file_1_usr1.id))

        self.assertEqual(response.status_code, 400)

        self.assertFalse(self.file_1_usr1.is_deleted)

    def testDelDirOfOtherUser(self):
        self.client.login(username='testuser2', password='bbsdfafd1&1b')
        response = self.client.get(reverse("compilation_8bit:del_dir") + "?id=" + str(self.dir_1_usr1.id))

        self.assertEqual(response.status_code, 400)

        self.assertFalse(self.dir_1_usr1.is_deleted)

    def testDelNotExistingFile(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')
        response = self.client.get(reverse("compilation_8bit:del_file") + "?id=sadfjsfla")

        self.assertEqual(response.status_code, 400)

    def testDelNotExistingDir(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')
        response = self.client.get(reverse("compilation_8bit:del_file") + "?id=sadfjsfla")

        self.assertEqual(response.status_code, 400)


